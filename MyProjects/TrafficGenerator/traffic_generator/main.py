import sys
import asyncio
from qasync import QEventLoop, QApplication
from app import TrafficGeneratorApp  # Импортируем главное окно приложения

def main():
    """
    Основная функция для запуска приложения.
    """
    # Создаем экземпляр приложения PyQt
    app = QApplication(sys.argv)

    # Настраиваем асинхронный цикл событий
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Создаем и показываем главное окно приложения
    window = TrafficGeneratorApp()
    window.show()

    # Запускаем асинхронный цикл событий
    with loop:
        loop.run_forever()

if __name__ == "__main__":
    main()