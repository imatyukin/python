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
        self.qos_table.setColumnCount(12)  # 12 столбцов
        self.qos_table.setHorizontalHeaderLabels([
            "DSCP Name", "DS Field Binary", "DS Field Decimal", "DS Hex",
            "TOS Precedence (dec)", "ToS Hexadecimal", "ToS Decimal", "ToS Binary",
            "ToS Name", "Service Class Name", "MPLS EXP", "MPLS EXP Binary"
        ])
        self.qos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.qos_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Только для чтения
        self.qos_table.verticalHeader().setVisible(False)  # Убираем номера строк
        self.qos_table.setSortingEnabled(True)  # Включаем сортировку

        # Добавляем данные в таблицу
        qos_data = self.generate_qos_data()
        qos_data.sort(key=lambda x: int(x[2]))  # Сортируем по DS Field Decimal (третий элемент кортежа)
        self.qos_table.setRowCount(len(qos_data))
        for row, data_row in enumerate(qos_data):
            for col, value in enumerate(data_row):
                self.qos_table.setItem(row, col, QTableWidgetItem(value))

        # Добавляем фильтры под таблицей
        filter_layout = QHBoxLayout()
        self.filter_widgets = []
        for col in range(self.qos_table.columnCount()):
            filter_widget = QLineEdit()
            filter_widget.setPlaceholderText(f"Filter by {self.qos_table.horizontalHeaderItem(col).text()}")
            filter_widget.textChanged.connect(self.filter_table)
            filter_layout.addWidget(filter_widget)
            self.filter_widgets.append(filter_widget)

        layout.addWidget(self.qos_table)
        layout.addLayout(filter_layout)
        self.setLayout(layout)

    def filter_table(self):
        for row in range(self.qos_table.rowCount()):
            match = True
            for col in range(self.qos_table.columnCount()):
                filter_text = self.filter_widgets[col].text().lower()
                item = self.qos_table.item(row, col)
                if item and filter_text:
                    if filter_text not in item.text().lower():
                        match = False
                        break
            self.qos_table.setRowHidden(row, not match)

    def generate_qos_data(self):
        """
        Генерирует данные для таблицы QoS согласно RFC 2474, RFC 2475 и спецификации MPLS EXP.
        Включает AF-классы (AF11–AF43), EF, BE и CS-классы (CS0–CS7).
        """
        qos_data = []

        # Функции для преобразования значений
        def tos_to_hex(tos_decimal):
            return f"0x{tos_decimal:02X}"

        def tos_to_binary(tos_decimal):
            return format(tos_decimal, '08b')

        def mpls_exp_to_binary(exp_decimal):
            return format(exp_decimal, '03b')

        def calculate_tos_decimal(ds_field_bin):
            """
            Рассчитывает полное значение ToS Decimal из DS Field Binary.
            Первые 3 бита маппируются на TOS Precedence, остальные 5 битов заполняются нулями.
            """
            tos_precedence = int(ds_field_bin[:3], 2)  # Первые 3 бита DS Field
            return tos_precedence << 5  # Сдвигаем на 5 битов влево

        # AF-классы (Assured Forwarding)
        for class_num in range(1, 5):  # Классы AF1–AF4
            for drop_prob in range(0, 3):  # Уровни надежности (0-2)
                dscp_name = f"AF{class_num}{drop_prob + 1}"
                ds_field_dec = (class_num << 3) + (drop_prob << 1)  # **Correct Formula**
                ds_field_bin = f"{ds_field_dec:06b}"
                ds_field_hex = f"0x{ds_field_dec:02X}"  # Шестнадцатеричное значение DS Field

                # TOS Precedence (первые 3 бита из DS Field)
                tos_precedence = (class_num - 1) * 8  # Преобразование класса в приоритет TOS
                tos_hex = tos_to_hex(tos_precedence)
                tos_dec = tos_precedence
                tos_bin = tos_to_binary(tos_precedence)

                # ToS Decimal (полное значение TOS)
                tos_full_decimal = calculate_tos_decimal(ds_field_bin)
                tos_full_bin = format(tos_full_decimal, '08b')
                tos_full_hex = tos_to_hex(tos_full_decimal)

                # ToS Name和服务 Class Name
                tos_name = f"Precedence {class_num - 1}"
                service_class_name = "Assured Forwarding"

                # MPLS EXP (первые 3 бита DS Field)
                mpls_exp = (ds_field_dec >> 3) & 0b111  # Извлекаем первые 3 бита для MPLS EXP
                mpls_exp_bin = mpls_exp_to_binary(mpls_exp)

                qos_data.append((
                    dscp_name, ds_field_bin, str(ds_field_dec), ds_field_hex,
                    str(tos_precedence), tos_hex, str(tos_full_decimal), tos_full_bin,
                    tos_name, service_class_name, str(mpls_exp), mpls_exp_bin
                ))
        # Expedited Forwarding (EF)
        ef_dscp = "EF"
        ef_ds_field_bin = "101110"
        ef_ds_field_dec = int(ef_ds_field_bin, 2)
        ef_ds_field_hex = f"0x{ef_ds_field_dec:02X}"

        # TOS Precedence для EF (первые 3 бита DS Field)
        ef_tos_precedence = (ef_ds_field_dec >> 5) & 0b111  # Первые 3 бита DS Field
        ef_tos_hex = tos_to_hex(ef_tos_precedence)
        ef_tos_dec = ef_tos_precedence
        ef_tos_bin = tos_to_binary(ef_tos_precedence)

        # ToS Decimal (полное значение TOS)
        ef_tos_full_decimal = calculate_tos_decimal(ef_ds_field_bin)
        ef_tos_full_bin = format(ef_tos_full_decimal, '08b')
        ef_tos_full_hex = tos_to_hex(ef_tos_full_decimal)

        ef_tos_name = "Expedited Forwarding"
        ef_service_class_name = "Expedited Forwarding"
        ef_mpls_exp = (ef_ds_field_dec >> 3) & 0b111  # Извлекаем MPLS EXP
        ef_mpls_exp_bin = mpls_exp_to_binary(ef_mpls_exp)

        qos_data.append((
            ef_dscp, ef_ds_field_bin, str(ef_ds_field_dec), ef_ds_field_hex,
            str(ef_tos_precedence), ef_tos_hex, str(ef_tos_full_decimal), ef_tos_full_bin,
            ef_tos_name, ef_service_class_name, str(ef_mpls_exp), ef_mpls_exp_bin
        ))

        # Best Effort (BE)
        be_dscp = "BE"
        be_ds_field_bin = "000000"
        be_ds_field_dec = int(be_ds_field_bin, 2)
        be_ds_field_hex = f"0x{be_ds_field_dec:02X}"

        # TOS Precedence для BE
        be_tos_precedence = 0  # Приоритет TOS для BE
        be_tos_hex = tos_to_hex(be_tos_precedence)
        be_tos_dec = be_tos_precedence
        be_tos_bin = tos_to_binary(be_tos_precedence)

        # ToS Decimal (полное значение TOS)
        be_tos_full_decimal = calculate_tos_decimal(be_ds_field_bin)
        be_tos_full_bin = format(be_tos_full_decimal, '08b')
        be_tos_full_hex = tos_to_hex(be_tos_full_decimal)

        be_tos_name = "Best Effort"
        be_service_class_name = "Best Effort"
        be_mpls_exp = (be_ds_field_dec >> 3) & 0b111  # Извлекаем MPLS EXP
        be_mpls_exp_bin = mpls_exp_to_binary(be_mpls_exp)

        qos_data.append((
            be_dscp, be_ds_field_bin, str(be_ds_field_dec), be_ds_field_hex,
            str(be_tos_precedence), be_tos_hex, str(be_tos_full_decimal), be_tos_full_bin,
            be_tos_name, be_service_class_name, str(be_mpls_exp), be_mpls_exp_bin
        ))

        # CS-классы (Class Selector)
        for class_num in range(8):  # Классы CS0–CS7
            cs_dscp = f"CS{class_num}"
            cs_ds_field_bin = f"{class_num << 3:06b}"  # Бинарное значение DS Field (6 бит)
            cs_ds_field_dec = int(cs_ds_field_bin, 2)  # Десятичное значение DS Field
            cs_ds_field_hex = f"0x{cs_ds_field_dec:02X}"  # Шестнадцатеричное значение DS Field

            # TOS Precedence (равно первым 3 битам DS Field)
            tos_precedence = class_num * 8
            tos_hex = tos_to_hex(tos_precedence)
            tos_dec = tos_precedence
            tos_bin = tos_to_binary(tos_precedence)

            # ToS Decimal (полное значение TOS)
            tos_full_decimal = calculate_tos_decimal(cs_ds_field_bin)
            tos_full_bin = format(tos_full_decimal, '08b')
            tos_full_hex = tos_to_hex(tos_full_decimal)

            # ToS Name和服务 Class Name
            tos_name = f"Class Selector {class_num}"
            service_class_name = "Class Selector"

            # MPLS EXP (первые 3 бита DS Field)
            mpls_exp = class_num  # Для CS, EXP равен номеру класса
            mpls_exp_bin = mpls_exp_to_binary(mpls_exp)

            qos_data.append((
                cs_dscp, cs_ds_field_bin, str(cs_ds_field_dec), cs_ds_field_hex,
                str(tos_precedence), tos_hex, str(tos_full_decimal), tos_full_bin,
                tos_name, service_class_name, str(mpls_exp), mpls_exp_bin
            ))

        return qos_data