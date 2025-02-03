from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt


class QoSTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Таблица с данными о QoS
        self.qos_table = QTableWidget()
        self.qos_table.setColumnCount(15)  # Количество столбцов согласно файлу
        self.qos_table.setHorizontalHeaderLabels([
            "Application", "CoS=IPP", "Traffic Class", "DSCP", "ToS", "ToS HEX",
            "Drop Precedence", "8th bit", "7th bit", "6th bit", "5th bit", "4th bit", "3rd bit", "2nd bit", "1st bit"
        ])
        self.qos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.qos_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Только для чтения
        self.qos_table.verticalHeader().setVisible(False)  # Убираем номера строк
        self.qos_table.setSelectionBehavior(QTableWidget.SelectRows)  # Выделение целых строк
        self.qos_table.setSelectionMode(QTableWidget.SingleSelection)  # Одиночное выделение

        # Добавляем данные в таблицу
        qos_data = self.generate_qos_data()
        self.qos_table.setRowCount(len(qos_data))
        for row, data_row in enumerate(qos_data):
            for col, value in enumerate(data_row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Запрещаем редактирование
                self.qos_table.setItem(row, col, item)

        layout.addWidget(self.qos_table)

        # Добавляем фильтры под каждым столбцом
        filter_layout = QHBoxLayout()
        self.filter_widgets = []
        for col in range(self.qos_table.columnCount()):
            filter_widget = QLineEdit()
            filter_widget.setPlaceholderText(f"Filter {self.qos_table.horizontalHeaderItem(col).text()}")
            filter_widget.textChanged.connect(lambda text, c=col: self.filter_table(c, text))
            filter_layout.addWidget(filter_widget)
            self.filter_widgets.append(filter_widget)

        layout.addLayout(filter_layout)
        self.setLayout(layout)

    def filter_table(self, column, text):
        """
        Фильтрует таблицу по указанному столбцу и тексту.
        """
        text = text.lower()
        for row in range(self.qos_table.rowCount()):
            item = self.qos_table.item(row, column)
            if item and text in item.text().lower():
                self.qos_table.setRowHidden(row, False)
            else:
                self.qos_table.setRowHidden(row, True)

    def generate_qos_data(self):
        """
        Генерирует данные для таблицы QoS согласно содержимому Excel-файла.
        """
        qos_data = []

        # Сопоставление AF-классов с приложениями
        af_applications = {
            "AF11": ("Low-Priority", "Low"),
            "AF12": ("Low-Priority", "Medium"),
            "AF13": ("Low-Priority", "High"),
            "AF21": ("Business-Critical", "Low"),
            "AF22": ("Business-Critical", "Medium"),
            "AF23": ("Business-Critical", "High"),
            "AF31": ("Interactive", "Low"),
            "AF32": ("Interactive", "Medium"),
            "AF33": ("Interactive", "High"),
            "AF41": ("High-Priority", "Low"),
            "AF42": ("High-Priority", "Medium"),
            "AF43": ("High-Priority", "High"),
        }

        # Функция для расчета ToS Decimal
        def calculate_tos_decimal(ds_field_bin):
            """
            Рассчитывает полное значение ToS Decimal из DS Field Binary.
            Первые 3 бита маппируются на IPP, следующие 3 бита — на Drop Probability.
            """
            ipp = int(ds_field_bin[:3], 2)  # Первые 3 бита DS Field
            drop_probability = int(ds_field_bin[3:], 2)  # Следующие 3 бита DS Field
            return (ipp << 5) | (drop_probability << 2)  # Объединяем значения

        # AF-классы (Assured Forwarding)
        for class_num in range(1, 5):  # Классы AF1–AF4
            for drop_prob in range(1, 4):  # Уровни надежности (1–3)
                dscp_name = f"AF{class_num}{drop_prob}"
                ds_field_dec = (class_num << 3) | (drop_prob << 1)  # Корректная формула
                ds_field_bin = f"{ds_field_dec:06b}"  # Бинарное значение DS Field

                # ToS Decimal (полное значение TOS)
                tos_decimal = calculate_tos_decimal(ds_field_bin)
                tos_hex = f"0x{tos_decimal:02X}"

                # ECN (Explicit Congestion Notification)
                ecn = ds_field_bin[-2:]

                # Application и Drop Precedence
                application, dp = af_applications.get(dscp_name, ("", ""))

                # CoS=IPP для AF-классов всегда равен номеру класса
                cos_ipp = class_num  # IPP = class_num для AF-классов

                # Добавляем данные в таблицу
                qos_data.append([
                    application,  # Application
                    cos_ipp,  # CoS=IPP
                    dscp_name,  # Traffic Class
                    ds_field_dec,  # DSCP
                    tos_decimal,  # ToS
                    tos_hex,  # ToS HEX
                    dp,  # Drop Precedence
                    int(ds_field_bin[0]),  # 8th bit
                    int(ds_field_bin[1]),  # 7th bit
                    int(ds_field_bin[2]),  # 6th bit
                    int(ds_field_bin[3]),  # 5th bit
                    int(ds_field_bin[4]),  # 4th bit
                    int(ds_field_bin[5]),  # 3th bit
                    0,  # 2th bit (ECN)
                    0  # 1th bit (ECN)
                ])

        # Expedited Forwarding (EF)
        ef_dscp = "EF"
        ef_ds_field_bin = "101110"
        ef_ds_field_dec = int(ef_ds_field_bin, 2)

        # ToS Decimal для EF
        ef_tos_decimal = calculate_tos_decimal(ef_ds_field_bin)
        ef_tos_hex = f"0x{ef_tos_decimal:02X}"

        # ECN для EF
        ef_ecn = ef_ds_field_bin[-2:]
        ef_application = "Voice"

        # Добавляем EF в таблицу
        qos_data.append([
            ef_application,  # Application
            5,  # CoS=IPP
            ef_dscp,  # Traffic Class
            ef_ds_field_dec,  # DSCP
            ef_tos_decimal,  # ToS
            ef_tos_hex,  # ToS HEX
            "",  # Drop Precedence
            int(ef_ds_field_bin[0]),  # 8th bit
            int(ef_ds_field_bin[1]),  # 7th bit
            int(ef_ds_field_bin[2]),  # 6th bit
            int(ef_ds_field_bin[3]),  # 5th bit
            int(ef_ds_field_bin[4]),  # 4th bit
            int(ef_ds_field_bin[5]),  # 3th bit
            1,  # 2th bit (ECN)
            0  # 1th bit (ECN)
        ])

        # Best Effort (BE)
        be_dscp = "BE"
        be_ds_field_bin = "000000"
        be_ds_field_dec = int(be_ds_field_bin, 2)

        # ToS Decimal для BE
        be_tos_decimal = calculate_tos_decimal(be_ds_field_bin)
        be_tos_hex = f"0x{be_tos_decimal:02X}"

        # ECN для BE
        be_ecn = be_ds_field_bin[-2:]
        be_application = "Best Effort"

        # Добавляем BE в таблицу
        qos_data.append([
            be_application,  # Application
            0,  # CoS=IPP
            be_dscp,  # Traffic Class
            be_ds_field_dec,  # DSCP
            be_tos_decimal,  # ToS
            be_tos_hex,  # ToS HEX
            "",  # Drop Precedence
            int(be_ds_field_bin[0]),  # 8th bit
            int(be_ds_field_bin[1]),  # 7th bit
            int(be_ds_field_bin[2]),  # 6th bit
            int(be_ds_field_bin[3]),  # 5th bit
            int(be_ds_field_bin[4]),  # 4th bit
            int(be_ds_field_bin[5]),  # 3th bit
            0,  # 2th bit (ECN)
            0  # 1th bit (ECN)
        ])

        # Class Selector (CS)
        for class_num in range(8):  # Классы CS0–CS7
            cs_dscp = f"CS{class_num}"
            cs_ds_field_bin = f"{class_num << 3:06b}"  # Корректная формула
            cs_ds_field_dec = int(cs_ds_field_bin, 2)

            # ToS Decimal для CS
            cs_tos_decimal = calculate_tos_decimal(cs_ds_field_bin)
            cs_tos_hex = f"0x{cs_tos_decimal:02X}"

            # ECN для CS
            cs_ecn = cs_ds_field_bin[-2:]
            cs_application = f"Class Selector {class_num}"

            # Добавляем CS в таблицу
            qos_data.append([
                cs_application,  # Application
                class_num,  # CoS=IPP
                cs_dscp,  # Traffic Class
                cs_ds_field_dec,  # DSCP
                cs_tos_decimal,  # ToS
                cs_tos_hex,  # ToS HEX
                "",  # Drop Precedence
                int(cs_ds_field_bin[0]),  # 8th bit
                int(cs_ds_field_bin[1]),  # 7th bit
                int(cs_ds_field_bin[2]),  # 6th bit
                int(cs_ds_field_bin[3]),  # 5th bit
                int(cs_ds_field_bin[4]),  # 4th bit
                int(cs_ds_field_bin[5]),  # 3th bit
                0,  # 2th bit (ECN)
                0  # 1th bit (ECN)
            ])

        return qos_data