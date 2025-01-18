from netmiko import ConnectHandler
import logging
import yaml
from functools import wraps
import argparse
from contextlib import contextmanager
from typing import Dict, Tuple, Optional, Any, List

# Загрузка конфигурации из YAML-файла
def load_config(config_file: str = 'config.yaml') -> Dict[str, Any]:
    """Загружает конфигурацию из YAML-файла."""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл конфигурации {config_file} не найден: {e}")
    except yaml.YAMLError as e:
        raise ValueError(f"Ошибка при чтении YAML-файла: {e}")

# Настройка логирования
def setup_logging(log_file: str) -> None:
    """Настраивает логирование."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        encoding='utf-8'
    )

# Декоратор для логирования команд
def log_command(func):
    """Декоратор для логирования выполняемых команд."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        command = args[1] if len(args) > 1 else kwargs.get('command')
        logging.info(f"Вводимая команда: {command}")
        print(f"Вводимая команда: {command}")  # Вывод команды в консоль
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
    return f"{rate_mbps * 1000:.2f} Кбит/с" if rate_mbps < 1 else f"{rate_mbps:.2f} Мбит/с"

# Обработка вывода команды monitor
def process_stat_output(output: str) -> Dict[str, int]:
    """Обрабатывает вывод команды monitor и извлекает статистику для ingress и egress."""
    stats = {"ingress": 0, "egress": 0}
    start_analysis = False
    current_direction = None

    for line in output.splitlines():
        if "At time t = 11 sec (Mode: Rate)" in line:
            start_analysis = True
        if start_analysis and "Ingress" in line:
            current_direction = "ingress"
        if start_analysis and "Egress" in line:
            current_direction = "egress"
        if start_analysis and current_direction and "Aggregate Forwarded" in line:
            try:
                stats[current_direction] = int(line.split()[-1])
            except (IndexError, ValueError):
                continue

    return stats

# Извлечение SAP и Service ID из вывода команды
def extract_sap_service_map(output: str, port: str) -> Dict[str, str]:
    """Извлекает SAP и Service ID из вывода команды show service sap-using."""
    return {
        parts[0]: parts[1]  # SAP: Service ID
        for line in output.splitlines()
        if port.lower() in line.lower() and (parts := line.split())
    }

# Сбор статистики для одного SAP
def collect_sap_statistics(ssh: ConnectHandler, sap: str, service_id: str, direction: str = 'both', sap_index: int = 1) -> Dict[str, Tuple[int, float]]:
    """Собирает статистику для одного SAP."""
    stat_command = f'monitor service id {service_id} sap {sap} rate interval 11 repeat 1'
    try:
        stat_output = send_command(ssh, stat_command, expect_string=r"\w{3} \w{3} \d{2} \d{2}:\d{2}:\d{2} \w{3} \d{4}")
        stats = process_stat_output(stat_output)

        result = {}
        if direction in ["ingress", "both"]:
            result["ingress"] = (stats["ingress"], (stats["ingress"] * 8) / 1_000_000)
            print(f"[{sap_index}/1] SAP {sap}: Октеты = {stats['ingress']}, Ingress Rate = {format_rate(result['ingress'][1])}")
        if direction in ["egress", "both"]:
            result["egress"] = (stats["egress"], (stats["egress"] * 8) / 1_000_000)
            print(f"[{sap_index}/2] SAP {sap}: Октеты = {stats['egress']}, Egress Rate = {format_rate(result['egress'][1])}")

        return result
    except Exception as e:
        logging.error(f"Ошибка при выполнении команды для SAP {sap}: {e}")
        return {}

# Вывод топ-N SAP
def print_top_sap(statistics: Dict[str, Dict[str, Tuple[int, float]]], direction: str = 'both', top_n: int = 10, port: str = "") -> None:
    """Выводит топ-N SAP по объему трафика."""
    if not statistics:
        print("Не удалось собрать статистику для SAP.")
        return

    for dir_key in ["ingress", "egress"]:
        if direction in [dir_key, "both"]:
            dir_stats = {sap: data[dir_key] for sap, data in statistics.items() if dir_key in data}
            if dir_stats:
                # Сортировка по убыванию октетов
                sorted_stats = sorted(dir_stats.items(), key=lambda x: x[1][0], reverse=True)[:top_n]
                print(f"\nТоп-{top_n} самых крупных SAP на порту {port} ({dir_key.capitalize()}):")
                for i, (sap, (octets, rate_mbps)) in enumerate(sorted_stats, start=1):
                    print(f"{i}. SAP {sap}: Октеты = {octets}, {dir_key.capitalize()} Rate = {format_rate(rate_mbps)}")
            else:
                print(f"Нет данных для {dir_key.capitalize()} на порту {port}.")

# Сбор статистики для всех SAP на указанных портах
def collect_statistics_for_ports(ssh: ConnectHandler, ports: List[str], service_id: str, direction: str) -> None:
    """Собирает статистику для всех SAP на указанных портах."""
    for port in ports:
        print(f"\nСбор статистики для порта {port}:")
        if service_id != 'none':
            # Режим сбора статистики для конкретного service_id
            collect_service_sap_statistics(ssh, service_id, port, direction)
        else:
            # Основной режим: сбор статистики для всех SAP на порту
            output = send_command(ssh, 'show service sap-using')
            sap_service_map = extract_sap_service_map(output, port)

            if not sap_service_map:
                print(f"SAP, относящиеся к {port}, не найдены.")
                continue

            print(f"Найдено {len(sap_service_map)} SAP, относящихся к {port}: {sap_service_map}")

            # Сбор статистики для каждого SAP
            statistics = {
                sap: collect_sap_statistics(ssh, sap, service_id, direction, sap_index=index + 1)
                for index, (sap, service_id) in enumerate(sap_service_map.items())
            }

            # Вывод топ-10 SAP
            print_top_sap(statistics, direction, port=port)

# Функция для сбора статистики SAP в конкретном сервисе
def collect_service_sap_statistics(ssh: ConnectHandler, service_id: str, port: str, direction: str = 'both') -> None:
    """Собирает статистику SAP в указанном сервисе."""
    # Команда для поиска всех SAP, относящихся к порту в сервисе
    command = f'show service id {service_id} sap'
    output = send_command(ssh, command)

    # Извлекаем SAP, относящиеся к порту
    sap_list = [line.split()[0] for line in output.splitlines() if port.lower() in line.lower()]

    if not sap_list:
        print(f"SAP, относящиеся к {port} в сервисе {service_id}, не найдены.")
        logging.info(f"SAP, относящиеся к {port} в сервисе {service_id}, не найдены.")
        return

    print(f"Найдено {len(sap_list)} SAP, относящихся к {port}: {sap_list}")

    # Сбор статистики для каждого SAP
    statistics: Dict[str, Dict[str, Tuple[int, float]]] = {}
    for index, sap in enumerate(sap_list, start=1):
        stats = collect_sap_statistics(ssh, sap, service_id, direction, sap_index=index)
        statistics[sap] = stats

    # Вывод топ-10 SAP
    print_top_sap(statistics, direction, port=port)

# Контекстный менеджер для SSH-соединения
@contextmanager
def ssh_connection(device: Dict[str, Any]) -> ConnectHandler:
    """Контекстный менеджер для управления SSH-соединением."""
    print(f"Попытка подключения к устройству с IP: {device['ip']}...")
    ssh = ConnectHandler(**device)
    try:
        yield ssh
    finally:
        ssh.disconnect()
        print("Соединение закрыто.")

# Основная функция
def main(config_file: str = 'config.yaml') -> None:
    """Основная логика программы."""
    try:
        # Загрузка конфигурации
        config = load_config(config_file)
        setup_logging(config['log_file'])

        with ssh_connection(config['device']) as ssh:
            hostname = send_command(ssh, 'show system information | match Name').split(':')[-1].strip()
            print(f"Подключение успешно установлено. Hostname устройства: {hostname}")

            send_command(ssh, "environment no more")
            send_command(ssh, "environment time-stamp")

            # Получаем service_id и преобразуем его в строку
            service_id = config.get('service_id', 'none')
            if service_id != 'none':
                service_id = str(service_id)  # Преобразуем в строку
                print(f"Работа в режиме сбора статистики для service id = {service_id}")

            # Обрабатываем каждый порт из списка
            ports = config['port'].split()  # Разделяем строку с портами на список
            collect_statistics_for_ports(ssh, ports, service_id, config.get('direction', 'both'))

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        print(f"Ошибка: {e}")

# Запуск программы
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Сбор статистики SAP на Nokia 7750SR.")
    parser.add_argument('--config', type=str, default='config.yaml', help="Путь к конфигурационному файлу")
    args = parser.parse_args()

    main(config_file=args.config)