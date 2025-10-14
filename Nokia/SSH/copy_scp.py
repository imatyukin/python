#!/usr/bin/env python3
"""
Скрипт для автоматизации передачи файлов по SCP с Nokia 7750 SR
Использует paramiko для SSH-подключения и обработки запроса пароля
Протестировано на Windows
"""

import paramiko
import sys
import time
from datetime import datetime

# Конфигурация подключения к Nokia 7750 SR
NOKIA_HOST = "192.168.233.129"  # IP-адрес вашего Nokia 7750 SR
NOKIA_USER = "admin"  # Имя пользователя для входа на Nokia
NOKIA_PASSWORD = "admin"  # Пароль для входа на Nokia

# Конфигурация SCP сервера назначения
SCP_USER = "root"
SCP_HOST = "192.168.233.128"
SCP_PASSWORD = "toor"  # Пароль для SCP-подключения

# Параметры копирования файла
SOURCE_FILE = "cf3:1.txt"  # Файл на Nokia для копирования
DESTINATION = f"scp://{SCP_USER}@{SCP_HOST}:~/"  # Путь назначения

# Настройки таймаутов
TIMEOUT = 30  # Таймаут SSH-подключения в секундах
COMMAND_TIMEOUT = 60  # Таймаут выполнения команды копирования в секундах


def log_message(message):
    """Выводит сообщение с временной меткой"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def connect_to_nokia():
    """Устанавливает SSH-соединение с Nokia 7750 SR"""
    log_message(f"Подключение к Nokia 7750 SR по адресу {NOKIA_HOST}...")

    try:
        # Создаем SSH-клиент
        client = paramiko.SSHClient()
        # Автоматически добавляем SSH ключ хоста (для первого подключения)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        log_message(f"Попытка подключения к {NOKIA_HOST}:22 от имени пользователя '{NOKIA_USER}'...")

        # Выполняем подключение
        client.connect(
            hostname=NOKIA_HOST,
            port=22,
            username=NOKIA_USER,
            password=NOKIA_PASSWORD,
            timeout=TIMEOUT,
            look_for_keys=False,  # Не использовать SSH-ключи
            allow_agent=False,  # Не использовать SSH-агент
            banner_timeout=30
        )

        log_message("Успешное подключение к Nokia 7750 SR")

        # Проверяем активность транспортного соединения
        transport = client.get_transport()
        if transport and transport.is_active():
            log_message("SSH транспорт активен")
        else:
            log_message("ВНИМАНИЕ: SSH транспорт может быть неактивен")

        return client

    except paramiko.AuthenticationException as e:
        log_message(f"ОШИБКА: Не удалось пройти аутентификацию - {e}")
        return None
    except paramiko.SSHException as e:
        log_message(f"ОШИБКА: Ошибка SSH протокола - {e}")
        return None
    except TimeoutError as e:
        log_message(f"ОШИБКА: Превышен таймаут подключения - {e}")
        return None
    except Exception as e:
        log_message(f"ОШИБКА подключения к Nokia: {type(e).__name__}: {e}")
        import traceback
        log_message(f"Трассировка: {traceback.format_exc()}")
        return None


def copy_file_via_scp(client):
    """Выполняет команду копирования по SCP и обрабатывает запрос пароля через интерактивную оболочку"""

    try:
        # Открываем интерактивную оболочку (shell)
        channel = client.invoke_shell()
        channel.settimeout(COMMAND_TIMEOUT)

        # Ждем появления начального приглашения командной строки
        time.sleep(2)
        output = channel.recv(4096).decode('utf-8', errors='ignore')
        log_message(f"Получено начальное приглашение")

        # Формируем и отправляем команду SCP
        scp_command = f'file copy {SOURCE_FILE} {DESTINATION} router-instance "management" force\n'
        log_message(f"Выполняем команду: {scp_command.strip()}")
        channel.send(scp_command)

        # Собираем вывод и ищем запрос пароля
        all_output = ""
        password_sent = False
        max_wait = 60  # Максимальное время ожидания в секундах
        start_time = time.time()

        while time.time() - start_time < max_wait:
            if channel.recv_ready():
                chunk = channel.recv(4096).decode('utf-8', errors='ignore')
                all_output += chunk
                print(chunk, end='', flush=True)  # Выводим в реальном времени

                # Проверяем запрос пароля
                if not password_sent and ('password:' in chunk.lower() or 'Password:' in chunk):
                    log_message("Обнаружен запрос пароля, отправляем пароль SCP...")
                    channel.send(SCP_PASSWORD + '\n')
                    password_sent = True

                # Проверяем запрос подтверждения SSH ключа хоста
                if 'yes/no' in chunk.lower():
                    log_message("Запрос подтверждения SSH ключа, принимаем...")
                    channel.send('yes\n')

                # Проверяем успешное завершение
                if '100%' in chunk or 'copied' in chunk.lower():
                    log_message("Файл успешно скопирован!")
                    time.sleep(1)
                    return True

                # Проверяем наличие ошибок
                if 'error' in chunk.lower() and 'password' not in chunk.lower():
                    log_message(f"Обнаружена ОШИБКА в выводе: {chunk}")
                    return False

            else:
                time.sleep(0.5)

        # Достигнут таймаут
        if password_sent:
            # Если пароль был отправлен, даем дополнительное время на завершение
            time.sleep(3)
            if channel.recv_ready():
                final_output = channel.recv(4096).decode('utf-8', errors='ignore')
                all_output += final_output
                print(final_output, end='', flush=True)

                if '100%' in final_output or 'copied' in final_output.lower():
                    log_message("Файл успешно скопирован!")
                    return True

        log_message("ВНИМАНИЕ: Превышен таймаут ожидания завершения")
        log_message(f"Последний вывод: {all_output[-500:]}")
        return False

    except Exception as e:
        log_message(f"ОШИБКА при копировании по SCP: {e}")
        return False
    finally:
        if 'channel' in locals():
            channel.close()


def main():
    """Main function"""
    log_message("Starting Nokia 7750 SR SCP copy script...")

    # Connect to Nokia
    client = connect_to_nokia()
    if client is None:
        log_message("Failed to connect to Nokia. Exiting.")
        sys.exit(1)

    # Give a moment for connection to stabilize
    time.sleep(1)

    # Execute SCP copy
    success = copy_file_via_scp(client)

    # Cleanup
    client.close()
    log_message("Connection closed")

    if success:
        log_message("Script completed successfully!")
        sys.exit(0)
    else:
        log_message("Script completed with errors!")
        sys.exit(1)


if __name__ == "__main__":
    main()