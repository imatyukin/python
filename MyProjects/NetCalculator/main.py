import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from ipv4_calculator import IPv4Calculator  # Модуль для IPv4
from ipv6_calculator import IPv6Calculator  # Модуль для IPv6
from qos_tab import QoSTab  # Модуль для QoS


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Net Calculator")
        self.setGeometry(100, 100, 800, 600)

        # Создание вкладок
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Вкладка IPv4
        self.ipv4_tab = IPv4Calculator()  # Импортируем класс из ipv4_calculator.py
        self.tab_widget.addTab(self.ipv4_tab, "IPv4")

        # Вкладка IPv6
        self.ipv6_tab = IPv6Calculator()  # Импортируем класс из ipv6_calculator.py
        self.tab_widget.addTab(self.ipv6_tab, "IPv6")

        # Вкладка QoS
        self.qos_tab = QoSTab()  # Импортируем класс из qos_tab.py
        self.tab_widget.addTab(self.qos_tab, "QoS")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())