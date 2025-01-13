import subprocess

# Путь к основному скрипту
script_path = "sap_monitor_stats.py"

# Аргументы для запуска
args = ["python", script_path, "--test", "--service-id", "318608115"]

# Запуск основного скрипта с потоковым выводом
try:
    print(f"Запуск основного скрипта с service_id = 318608115...")
    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,  # Захватываем стандартный вывод
        stderr=subprocess.PIPE,  # Захватываем стандартный вывод ошибок
        text=True,               # Вывод в виде текста (а не байтов)
        encoding="utf-8"         # Указываем кодировку UTF-8
    )

    # Чтение вывода в реальном времени
    while True:
        output = process.stdout.readline()  # Читаем одну строку вывода
        if output == "" and process.poll() is not None:
            break  # Если вывод закончился и процесс завершился, выходим из цикла
        if output:
            print(output.strip())  # Выводим строку (убираем лишние пробелы)

        # Чтение ошибок в реальном времени
        error = process.stderr.readline()
        if error:
            print(error.strip())  # Выводим ошибку (убираем лишние пробелы)

    # Ожидание завершения процесса
    process.wait()

    # Проверка кода завершения
    if process.returncode == 0:
        print("Скрипт успешно выполнен.")
    else:
        print(f"Скрипт завершился с ошибкой (код: {process.returncode}).")

except Exception as e:
    print(f"Ошибка при выполнении скрипта: {str(e)}")