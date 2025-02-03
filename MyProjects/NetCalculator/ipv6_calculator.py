from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class IPv6Calculator(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("IPv6 Calculator (Coming Soon!)"))
        self.setLayout(layout)