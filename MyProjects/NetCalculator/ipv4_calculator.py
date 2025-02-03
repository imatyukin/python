import socket  # Добавляем импорт модуля socket

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QApplication
)
from PyQt5.QtCore import Qt
from ipaddress import IPv4Address, IPv4Network


def ipv4_hex(ip_str):
    """Функция для преобразования IP-адреса в 16-ричный формат."""
    return ".".join(format(int(x), '02X') for x in ip_str.split("."))


def ipv4_binary(ip_str, prefix):
    """
    Функция для преобразования IP-адреса в бинарный формат с разделителем '|'.
    Разделитель ставится между сетевой и хостовой частями.
    """
    binary_parts = [format(int(x), '08b') for x in ip_str.split(".")]
    if prefix == 32:
        return ".".join(binary_parts)  # Без разделителя для /32

    # Разделение на сетевую и хостовую части
    network_bits = prefix // 8  # Количество целых байт, принадлежащих сети
    remaining_bits = prefix % 8  # Оставшиеся биты в неполном байте

    # Собираем бинарное представление с разделителем
    if remaining_bits > 0:
        binary_value = ".".join(binary_parts[:network_bits])  # Сетевая часть
        binary_value += "." + binary_parts[network_bits][:remaining_bits] + " | " + binary_parts[network_bits][remaining_bits:]
        if network_bits < 3:
            binary_value += "." + ".".join(binary_parts[network_bits + 1:])  # Хостовая часть
    else:
        binary_value = ".".join(binary_parts[:network_bits]) + " | "
        if network_bits <= 3:
            binary_value += ".".join(binary_parts[network_bits:])  # Хостовая часть

    # Убираем лишнюю точку в начале строки
    if binary_value.startswith("."):
        binary_value = binary_value[1:]

    return binary_value


class IPv4Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Создаем сетку для размещения элементов
        grid_layout = QGridLayout()

        # IP-адрес
        self.ip_input = QLineEdit()
        self.ip_label = QLabel("IP адрес:")
        grid_layout.addWidget(self.ip_label, 0, 0)
        grid_layout.addWidget(self.ip_input, 0, 1)

        # Автоматическая вставка IP-адреса системы
        try:
            host_ip = socket.gethostbyname(socket.gethostname())  # Получаем IP-адрес хоста
            self.ip_input.setText(host_ip)  # Вставляем его в поле ввода
        except Exception as e:
            print(f"Ошибка при получении IP-адреса: {e}")

        # Маска
        self.mask_combo = QComboBox()
        masks = [
            (0, "0.0.0.0"),
            (1, "128.0.0.0"),
            (2, "192.0.0.0"),
            (3, "224.0.0.0"),
            (4, "240.0.0.0"),
            (5, "248.0.0.0"),
            (6, "252.0.0.0"),
            (7, "254.0.0.0"),
            (8, "255.0.0.0"),
            (9, "255.128.0.0"),
            (10, "255.192.0.0"),
            (11, "255.224.0.0"),
            (12, "255.240.0.0"),
            (13, "255.248.0.0"),
            (14, "255.252.0.0"),
            (15, "255.254.0.0"),
            (16, "255.255.0.0"),
            (17, "255.255.128.0"),
            (18, "255.255.192.0"),
            (19, "255.255.224.0"),
            (20, "255.255.240.0"),
            (21, "255.255.248.0"),
            (22, "255.255.252.0"),
            (23, "255.255.254.0"),
            (24, "255.255.255.0"),
            (25, "255.255.255.128"),
            (26, "255.255.255.192"),
            (27, "255.255.255.224"),
            (28, "255.255.255.240"),
            (29, "255.255.255.248"),
            (30, "255.255.255.252"),
            (31, "255.255.255.254"),
            (32, "255.255.255.255")
        ]
        for prefix, netmask in masks:
            self.mask_combo.addItem(f"{prefix} - {netmask}")

        self.mask_label = QLabel("Маска:")
        grid_layout.addWidget(self.mask_label, 1, 0)
        grid_layout.addWidget(self.mask_combo, 1, 1)

        # Кнопка "Подсчитать"
        self.calculate_button = QPushButton("Подсчитать →")
        self.calculate_button.clicked.connect(self.calculate_ipv4)
        grid_layout.addWidget(self.calculate_button, 0, 2, 2, 1)

        # Добавляем сетку в основной макет
        layout.addLayout(grid_layout)

        # Таблица результатов
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Имя", "Значение", "16-ричный код", "Бинарное значение"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.result_table.setSelectionBehavior(QTableWidget.SelectItems)
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.result_table.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.result_table)

        # Информационная панель под таблицей
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)  # Включаем автоматический перенос текста
        layout.addWidget(self.info_label)

        # Подсказка о формате ввода
        self.input_hint_label = QLabel("В поле IP адреса можно так же вводить данные в формате IP/mask, например 192.168.0.1/16")
        self.input_hint_label.setWordWrap(True)  # Включаем перенос текста
        layout.addWidget(self.input_hint_label)  # Добавляем подсказку в макет

        self.setLayout(layout)

    def calculate_ipv4(self):
        try:
            ip_input = self.ip_input.text().strip()  # Получаем текст из поля ввода

            # Проверяем, содержит ли ввод маску (/prefix)
            if "/" in ip_input:
                ip, prefix_str = ip_input.split("/", 1)  # Разделяем IP и маску
                prefix = int(prefix_str.strip())  # Преобразуем маску в число
                mask_text = f"{prefix} - {IPv4Network(f'0.0.0.0/{prefix}', strict=False).netmask}"  # Находим соответствующую маску
            else:
                ip = ip_input
                mask_text = self.mask_combo.currentText()  # Используем выбранную маску из выпадающего списка
                prefix = int(mask_text.split(" - ")[0])  # Получаем префикс из выбранной маски

            # Создаем сеть
            network = IPv4Network(f"{ip}/{prefix}", strict=False)
            netmask = network.netmask
            wildcard = IPv4Address(~int(netmask) & 0xFFFFFFFF)

            # Вычисляем общее количество хостов
            if prefix == 32:  # Для /32
                total_hosts = 1
                hostmin = str(network.network_address)
                hostmax = str(network.broadcast_address)
            elif prefix == 31:  # Для /31
                total_hosts = 2
                hostmin = str(network.network_address)
                hostmax = str(network.broadcast_address)
            else:  # Для остальных масок
                total_hosts = 2 ** (32 - prefix) - 2
                if prefix < 31:
                    hostmin = str(network.network_address + 1)
                    hostmax = str(network.broadcast_address - 1)
                else:
                    hostmin = ""
                    hostmax = ""

            # Подготовка данных для таблицы
            data = [
                ("Адрес", ip, ipv4_hex(ip), ipv4_binary(ip, prefix)),
                ("Bitmask", str(prefix), "", ""),
                ("Netmask", str(netmask), ipv4_hex(str(netmask)), ipv4_binary(str(netmask), prefix)),
                ("Wildcard", str(wildcard), ipv4_hex(str(wildcard)), ipv4_binary(str(wildcard), prefix)),
                ("Network", str(network.network_address), ipv4_hex(str(network.network_address)), ipv4_binary(str(network.network_address), prefix)),
                ("Broadcast", str(network.broadcast_address), ipv4_hex(str(network.broadcast_address)), ipv4_binary(str(network.broadcast_address), prefix)),
                ("Hostmin", hostmin, ipv4_hex(hostmin) if hostmin else "", ipv4_binary(hostmin, prefix) if hostmin else ""),
                ("Hostmax", hostmax, ipv4_hex(hostmax) if hostmax else "", ipv4_binary(hostmax, prefix) if hostmax else ""),
                ("Hosts", f"{total_hosts:,}" if total_hosts >= 0 else "0", "", "")
            ]

            # Заполнение таблицы результатов
            self.result_table.setRowCount(len(data))
            for row, (name, value, hex_code, binary) in enumerate(data):
                self.result_table.setItem(row, 0, QTableWidgetItem(name))
                self.result_table.setItem(row, 1, QTableWidgetItem(value))
                self.result_table.setItem(row, 2, QTableWidgetItem(hex_code))
                self.result_table.setItem(row, 3, QTableWidgetItem(binary))

            # Расчет диапазона байтов
            byte_range_info = "N/A"
            if 1 <= prefix <= 30:  # Только для масок /1–/30
                last_byte_mask = int(netmask.exploded.split(".")[-1])  # Последний байт маски
                step = 2 ** (8 - (prefix % 8)) if prefix % 8 != 0 else 256  # Размер каждого диапазона
                if step < 256:
                    byte_ranges = [f"{i}-{i + step - 1}" for i in range(0, 256, step)]
                    byte_range_info = ", ".join(byte_ranges)

            # Отображение информации о диапазоне байтов
            self.info_label.setText(f"Right byte range for netmask {str(netmask)}:\n{byte_range_info}")

        except Exception as e:
            print(f"Ошибка: {e}")
            self.info_label.setText(f"Ошибка: {str(e)}")

    def show_context_menu(self, pos):
        """
        Показывает контекстное меню при правом клике на таблице.
        Позволяет скопировать содержимое выбранной ячейки.
        """
        menu = QMenu(self)
        copy_action = menu.addAction("Копировать")
        action = menu.exec_(self.result_table.mapToGlobal(pos))
        if action == copy_action:
            selected_item = self.result_table.itemAt(pos)
            if selected_item:
                QApplication.clipboard().setText(selected_item.text())


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = IPv4Calculator()
    window.setWindowTitle("IPv4 Calculator")
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())