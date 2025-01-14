from netmiko import ConnectHandler
import logging
import yaml
from functools import wraps
import argparse
from contextlib import contextmanager
from typing import Dict, Tuple, Optional, Any

# Загрузка конфигурации из YAML-файла
def load_config(config_file: str = 'config.yaml') -> Dict[str, Any]:
    """Загружает конфигурацию из YAML-файла."""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл конфигурации {config_file} не найден.")
    except yaml.YAMLError as e:
        raise ValueError(f"Ошибка при чтении YAML-файла: {e}")

# Настройка логирования с указанием кодировки UTF-8
def setup_logging(log_file: str) -> None:
    """Настраивает логирование."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        encoding='utf-8'  # Указываем кодировку UTF-8
    )

# Декоратор для логирования команд
def log_command(func):
    """Декоратор для логирования выполняемых команд."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        command = args[1] if len(args) > 1 else kwargs.get('command')
        logging.info(f"Вводимая команда: {command}")
        print(f"Вводимая команда: {command}")
        return func(*args, **kwargs)
    return wrapper

# Функция для выполнения команд
@log_command
def send_command(ssh: ConnectHandler, command: str, expect_string: Optional[str] = None, read_timeout: int = 120) -> str:
    """Отправляет команду на устройство."""
    return ssh.send_command(command, expect_string=expect_string, read_timeout=read_timeout)

# Форматирование скорости
def format_rate(rate_mbps: float) -> str:
    """Форматирует скорость: если меньше 1 Мбит/с, переводит в Кбит/с."""
    if rate_mbps < 1:
        return f"{rate_mbps * 1000:.2f} Кбит/с"
    return f"{rate_mbps:.2f} Мбит/с"

# Обработка вывода команды monitor
def process_stat_output(output: str) -> int:
    """Обрабатывает вывод команды monitor и извлекает статистику."""
    egress_octets = 0
    start_analysis = False
    egress_found = False

    for line in output.splitlines():
        if "At time t = 11 sec (Mode: Rate)" in line:
            start_analysis = True  # Начинаем анализ с этой строки
        if start_analysis and "Egress" in line:
            egress_found = True  # Найдена строка Egress
        if start_analysis and egress_found and "Aggregate Forwarded" in line:
            try:
                # Пример строки: "Aggregate Forwarded   : 100                     853855"
                parts = line.split()
                egress_octets = int(parts[-1])  # Извлекаем последнее значение (октеты)
                break  # Прекращаем поиск после извлечения данных
            except (IndexError, ValueError):
                egress_octets = 0  # Если не удалось извлечь значение, используем 0
                break

    return egress_octets

# Извлечение SAP и Service ID из вывода команды
def extract_sap_service_map(output: str, port: str) -> Dict[str, str]:
    """Извлекает SAP и Service ID из вывода команды show service sap-using."""
    sap_service_map = {}
    for line in output.splitlines():
        if port.lower() in line.lower():
            parts = line.split()
            sap = parts[0]  # SAP (например, lag-11:648.1796)
            service_id = parts[1]  # Service ID (например, 118600001)
            sap_service_map[sap] = service_id
    return sap_service_map

# Сбор статистики для одного SAP
def collect_sap_statistics(ssh: ConnectHandler, sap: str, service_id: str) -> Tuple[int, float]:
    """Собирает статистику для одного SAP."""
    stat_command = f'monitor service id {service_id} sap {sap} rate interval 11 repeat 1'
    try:
        stat_output = send_command(ssh, stat_command, expect_string=r"\w{3} \w{3} \d{2} \d{2}:\d{2}:\d{2} \w{3} \d{4}")
        egress_octets = process_stat_output(stat_output)
        egress_rate_mbps = (egress_octets * 8) / 1000000  # Убрано деление на 11
        return egress_octets, egress_rate_mbps
    except Exception as e:
        print(f"Ошибка при выполнении команды для SAP {sap}: {str(e)}")
        logging.error(f"Ошибка при выполнении команды для SAP {sap}: {str(e)}")
        return 0, 0.0

# Вывод топ-10 клиентов
def print_top_clients(statistics: Dict[str, Tuple[int, float]]) -> None:
    """Выводит топ-10 клиентов по объему трафика."""
    if statistics:
        sorted_statistics = sorted(statistics.items(), key=lambda x: x[1][0], reverse=True)[:10]
        print("\nТоп-10 самых крупных клиентов:")
        logging.info("Топ-10 самых крупных клиентов:")
        for i, (sap, (octets, rate_mbps)) in enumerate(sorted_statistics, start=1):
            print(f"{i}. SAP {sap}: Октеты за 11 сек = {octets}, Egress Rate = {format_rate(rate_mbps)}")
            logging.info(f"{i}. SAP {sap}: Октеты за 11 сек = {octets}, Egress Rate = {format_rate(rate_mbps)}")
    else:
        print("Не удалось собрать статистику для SAP.")
        logging.info("Не удалось собрать статистику для SAP.")

# Функция для тестирования SAP в конкретном сервисе
def test_service_sap(ssh: ConnectHandler, service_id: str, port: str) -> None:
    """Тестирует SAP в указанном сервисе."""
    print(f"\nТестирование SAP в сервисе {service_id}...")

    # Команда для поиска всех SAP, относящихся к порту в сервисе
    command = f'show service id {service_id} sap'
    output = send_command(ssh, command)

    # Извлекаем SAP, относящиеся к порту
    sap_list = [line.split()[0] for line in output.splitlines() if port.lower() in line.lower()]

    if not sap_list:
        print(f"SAP, относящиеся к {port} в сервисе {service_id}, не найдены.")
        logging.info(f"SAP, относящиеся к {port} в сервисе {service_id}, не найдены.")
        return

    print(f"Найдено {len(sap_list)} SAP, относящихся к {port} в сервисе {service_id}: {sap_list}")

    # Сбор статистики для каждого SAP
    statistics: Dict[str, Tuple[int, float]] = {}
    for index, sap in enumerate(sap_list, start=1):
        print(f"[{index}/{len(sap_list)}] Сбор статистики для SAP: {sap} (Service ID: {service_id})")
        egress_octets, egress_rate_mbps = collect_sap_statistics(ssh, sap, service_id)
        statistics[sap] = (egress_octets, egress_rate_mbps)
        print(f"[{index}/{len(sap_list)}] SAP {sap}: Октеты за 11 сек = {egress_octets}, Egress Rate = {format_rate(egress_rate_mbps)}")

    # Вывод топ-10 клиентов
    print_top_clients(statistics)

# Контекстный менеджер для SSH-соединения
@contextmanager
def ssh_connection(device: Dict[str, Any]) -> ConnectHandler:
    """Контекстный менеджер для управления SSH-соединением."""
    print(f"Попытка подключения к устройству с IP: {device['ip']}...", flush=True)  # Сообщение о попытке подключения
    ssh = ConnectHandler(**device)
    try:
        yield ssh
    finally:
        ssh.disconnect()
        print("Соединение закрыто.")

# Основная функция
def main(test_mode: bool = False, service_id: Optional[str] = None, config_file: str = 'config.yaml') -> None:
    """Основная логика программы."""
    try:
        # Загрузка конфигурации
        config = load_config(config_file)
        device = config['device']
        port = config['port']  # Используем переменную port вместо lag_interface
        log_file = config['log_file']

        # Настройка логирования
        setup_logging(log_file)

        # Устанавливаем SSH-соединение с использованием контекстного менеджера
        with ssh_connection(device) as ssh:
            # Получаем hostname устройства
            hostname = send_command(ssh, 'show system information | match Name').split(':')[-1].strip()
            print(f"Подключение успешно установлено. Hostname устройства: {hostname}")

            # Включаем временные метки и отключаем постраничный вывод
            send_command(ssh, "environment no more")
            send_command(ssh, "environment time-stamp")

            # Если включен тестовый режим, запускаем тестирование
            if test_mode and service_id:
                test_service_sap(ssh, service_id, port)
            else:
                # Основная логика программы
                command = 'show service sap-using'
                output = send_command(ssh, command)

                # Извлекаем SAP и Service ID из вывода
                sap_service_map = extract_sap_service_map(output, port)

                if not sap_service_map:
                    print(f"SAP, относящиеся к {port}, не найдены.")
                    logging.info(f"SAP, относящиеся к {port}, не найдены.")
                    return

                print(f"Найдено {len(sap_service_map)} SAP, относящихся к {port}: {sap_service_map}")

                # Сбор статистики для каждого SAP
                statistics: Dict[str, Tuple[int, float]] = {}
                for index, (sap, service_id) in enumerate(sap_service_map.items(), start=1):
                    print(f"[{index}/{len(sap_service_map)}] Сбор статистики для SAP: {sap} (Service ID: {service_id})")
                    egress_octets, egress_rate_mbps = collect_sap_statistics(ssh, sap, service_id)
                    statistics[sap] = (egress_octets, egress_rate_mbps)
                    print(f"[{index}/{len(sap_service_map)}] SAP {sap}: Октеты за 11 сек = {egress_octets}, Egress Rate = {format_rate(egress_rate_mbps)}")

                # Вывод топ-10 клиентов
                print_top_clients(statistics)

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        logging.error(f"Ошибка: {str(e)}")

# Запуск программы
if __name__ == "__main__":
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Сбор статистики SAP на Nokia 7750SR.")
    parser.add_argument('--test', action='store_true', help="Включить тестовый режим")
    parser.add_argument('--service-id', type=str, help="Service ID для тестирования")
    parser.add_argument('--config', type=str, default='config.yaml', help="Путь к конфигурационному файлу")
    args = parser.parse_args()

    # Запуск основной программы
    main(test_mode=args.test, service_id=args.service_id, config_file=args.config)