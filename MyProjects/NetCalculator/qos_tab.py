from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView


class QoSTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        qos_data = [
            ("TOS", "DSCP", "Class", "Drop Probability"),
            ("0x00", "CS0", "Best Effort", "Low"),
            ("0x10", "AF11", "Assured Forwarding", "Medium"),
            ("0x20", "AF21", "Assured Forwarding", "Medium"),
            ("0x30", "AF31", "Assured Forwarding", "Medium"),
            ("0x40", "AF41", "Assured Forwarding", "Medium"),
            ("0x50", "EF", "Expedited Forwarding", "High"),
        ]

        qos_table = QTableWidget()
        qos_table.setColumnCount(len(qos_data[0]))
        qos_table.setHorizontalHeaderLabels(qos_data[0])
        qos_table.setRowCount(len(qos_data) - 1)

        for row, (tos, dscp, qos_class, drop_prob) in enumerate(qos_data[1:]):
            qos_table.setItem(row, 0, QTableWidgetItem(tos))
            qos_table.setItem(row, 1, QTableWidgetItem(dscp))
            qos_table.setItem(row, 2, QTableWidgetItem(qos_class))
            qos_table.setItem(row, 3, QTableWidgetItem(drop_prob))

        qos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        qos_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Только для чтения
        qos_table.setSelectionBehavior(QTableWidget.SelectRows)  # Выделение строк

        layout.addWidget(qos_table)
        self.setLayout(layout)