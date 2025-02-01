from PyQt5 import QtWidgets, QtGui, QtCore
import time
import yaml
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from qasync import asyncSlot
import threading
from generator import TrafficGenerator  # Импортируем класс генератора трафика
from utils import (  # Импортируем вспомогательные функции
    validate_ip_address, validate_port, validate_packet_size,
    validate_threads, validate_range
)

class TrafficGeneratorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Traffic Generator v.2.0")
        self.setGeometry(100, 100, 1000, 800)
        self.running = False  # Флаг для отслеживания состояния генератора
        self.generator = None  # Экземпляр генератора трафика
        self.stats = {'sent': 0, 'errors': 0, 'bytes': 0}  # Статистика
        self.history = {'time': [], 'pps': [], 'mbps': []}  # История для графиков
        self.start_time = 0  # Время начала генерации
        self.protocol = 'UDP'  # Протокол по умолчанию
        self.last_stats_text = ""  # Последний текст статистики
        self.saved_ip_prec = 0  # Сохраненное значение IP Precedence
        self.real_source_address = None  # Реальный IP-адрес источника
        self.real_source_port = None  # Реальный порт источника
        self.real_destination_address = None  # Реальный IP-адрес назначения
        self.real_destination_port = None  # Реальный порт назначения
        self.initUI()  # Инициализация интерфейса

    def initUI(self):
        """
        Инициализация графического интерфейса.
        """
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Строка состояния
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)

        # Группа настроек
        settings_group = QtWidgets.QGroupBox("Settings")
        settings_layout = QtWidgets.QGridLayout()
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Выбор типа трафика
        self.traffic_type = QtWidgets.QComboBox()
        self.traffic_type.addItems(["unicast", "broadcast", "multicast"])
        settings_layout.addWidget(QtWidgets.QLabel("Traffic Type:"), 0, 0)
        settings_layout.addWidget(self.traffic_type, 0, 1)
        self.traffic_type.currentIndexChanged.connect(self.update_destination_label)

        # Выбор протокола
        self.protocol_type = QtWidgets.QComboBox()
        self.protocol_type.addItems(["UDP", "ICMP"])
        settings_layout.addWidget(QtWidgets.QLabel("Protocol:"), 1, 0)
        settings_layout.addWidget(self.protocol_type, 1, 1)
        self.protocol_type.currentIndexChanged.connect(self.update_protocol)

        # Поля для ввода данных
        self.source_ip = QtWidgets.QLineEdit()
        self.source_port = QtWidgets.QLineEdit()
        self.destination_ip = QtWidgets.QLineEdit()
        self.dest_port = QtWidgets.QLineEdit()
        self.packet_size = QtWidgets.QLineEdit()
        self.threads = QtWidgets.QLineEdit()
        self.dscp = QtWidgets.QLineEdit()
        self.ip_prec = QtWidgets.QLineEdit()
        self.ecn = QtWidgets.QLineEdit()

        # Словарь для управления видимостью полей
        self.all_fields = {
            "Source IP:": self.source_ip,
            "Source Port:": self.source_port,
            "Destination IP:": self.destination_ip,
            "Destination Port:": self.dest_port,
            "Packet Size:": self.packet_size,
            "Threads:": self.threads,
            "DSCP (0-63):": self.dscp,
            "IP Precedence (0-7):": self.ip_prec,
            "ECN (0-3):": self.ecn
        }

        # Видимые поля для каждого протокола
        self.protocol_fields = {
            "udp": ["Source IP:", "Source Port:", "Destination IP:", "Destination Port:", "Packet Size:", "Threads:",
                    "DSCP (0-63):", "IP Precedence (0-7):", "ECN (0-3):"],
            "icmp": ["Source IP:", "Destination IP:", "Packet Size:", "Threads:", "DSCP (0-63):",
                     "IP Precedence (0-7):", "ECN (0-3):"]
        }

        # Добавление полей в интерфейс
        self.field_widgets = {}
        row_counter = 2
        for label_text, widget in self.all_fields.items():
            label = QtWidgets.QLabel(label_text)
            settings_layout.addWidget(label, row_counter, 0)
            settings_layout.addWidget(widget, row_counter, 1)
            self.field_widgets[label_text] = (label, widget)
            row_counter += 1

        # Выбор режима скорости
        self.speed_mode = QtWidgets.QComboBox()
        self.speed_mode.addItems(["kbps", "mbps", "pps", "interval"])
        self.speed_mode.setCurrentText("mbps")
        self.speed_value = QtWidgets.QLineEdit()

        settings_layout.addWidget(QtWidgets.QLabel("Speed Mode:"), row_counter, 0)
        settings_layout.addWidget(self.speed_mode, row_counter, 1)
        row_counter += 1
        settings_layout.addWidget(QtWidgets.QLabel("Speed Value:"), row_counter, 0)
        settings_layout.addWidget(self.speed_value, row_counter, 1)

        self.update_visible_fields()  # Обновление видимых полей

        # Кнопки управления
        self.toggle_button = QtWidgets.QPushButton("Start")
        self.toggle_button.clicked.connect(self.toggle_traffic)
        layout.addWidget(self.toggle_button)

        self.load_button = QtWidgets.QPushButton("Load Config")
        self.load_button.clicked.connect(self.load_config)
        layout.addWidget(self.load_button)

        self.save_button = QtWidgets.QPushButton("Save Config")
        self.save_button.clicked.connect(self.save_config)
        layout.addWidget(self.save_button)

        # Графики
        self.figure, (self.ax2, self.ax1) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.ax2.plot([], [], label='Mbps', color='orange')
        self.ax1.plot([], [], label='PPS')
        self.ax1.legend()
        self.ax2.legend()
        self.canvas.draw()

        # Текстовое поле для статистики
        self.stats_text = QtWidgets.QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)

        initial_stats_text = "<b>Traffic Flow:</b><br>"
        initial_stats_text += "<b>Packets Sent:</b> 0<br>"
        initial_stats_text += "<b>Total Bytes:</b> 0<br>"
        initial_stats_text += "<b>Average Mbps:</b> 0.00<br>"
        initial_stats_text += "<b>Average PPS:</b> 0.00<br>"
        initial_stats_text += "<b>Errors:</b> 0<br>"

        self.stats_text.setText(initial_stats_text)
        layout.addWidget(self.stats_text)

        # Таймер для обновления статистики
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_stats)
        self.update_timer.start(1000)

    def update_protocol(self):
        """
        Обновление протокола и видимых полей.
        """
        self.protocol = self.protocol_type.currentText()
        self.update_visible_fields()

    def update_visible_fields(self):
        """
        Обновление видимости полей в зависимости от выбранного протокола.
        """
        current_protocol = self.protocol_type.currentText().lower()
        for label_text, (label, widget) in self.field_widgets.items():
            if label_text in self.protocol_fields.get(current_protocol, []):
                label.setVisible(True)
                widget.setVisible(True)
            else:
                label.setVisible(False)
                widget.setVisible(False)

    def update_destination_label(self):
        """
        Обновление метки назначения в зависимости от типа трафика.
        """
        if self.traffic_type.currentText() == 'multicast':
            self.field_widgets["Destination IP:"][0].setText('Group IP:')
        else:
            self.field_widgets["Destination IP:"][0].setText('Destination IP:')

    def update_real_values(self, real_source_address, real_source_port, real_destination_address, real_destination_port):
        """
        Обновление реальных значений IP и портов.
        """
        self.real_source_address = real_source_address
        self.real_source_port = real_source_port
        self.real_destination_address = real_destination_address
        self.real_destination_port = real_destination_port

    @asyncSlot()
    async def toggle_traffic(self):
        """
        Переключение между запуском и остановкой генерации трафика.
        """
        if self.running:
            await self.stop_traffic()
        else:
            await self.start_traffic()

    @asyncSlot()
    async def start_traffic(self):
        """
        Запуск генерации трафика.
        """
        try:
            self.running = True
            self.start_time = time.time()
            self.stats = {'sent': 0, 'errors': 0, 'bytes': 0}
            self.history = {'time': [], 'pps': [], 'mbps': []}

            # Сбор конфигурации
            config = {
                'traffic_type': self.traffic_type.currentText(),
                'source_address': self.source_ip.text(),
                'source_port': validate_port(self.source_port.text()) if self.protocol == 'UDP' else 0,
                'destination_address': self.destination_ip.text(),
                'destination_port': validate_port(self.dest_port.text()) if self.protocol == 'UDP' else 0,
                'packet_size': validate_packet_size(self.packet_size.text()),
                'threads': validate_threads(self.threads.text()),
                'speed_mode': self.speed_mode.currentText(),
                'speed_value': float(self.speed_value.text() or 1.0),
                'qos': {
                    'dscp': validate_range(self.dscp.text(), 0, 63),
                    'ip_precedence': validate_range(self.ip_prec.text(), 0, 7),
                    'ecn': validate_range(self.ecn.text(), 0, 3)
                }
            }

            if config['qos']['ip_precedence'] is not None:
                self.saved_ip_prec = config['qos']['ip_precedence']
            else:
                self.saved_ip_prec = 0

            validate_ip_address(config.get('source_address'))
            validate_ip_address(config.get('destination_address'))

            print("Starting Traffic Generator with config:", config)
            self.generator = TrafficGenerator(config, self.stats, self.protocol, self)
            self.thread = threading.Thread(target=self.generator.run, daemon=True)
            self.thread.start()

            self.real_source_address = self.generator.real_source_address
            self.real_source_port = self.generator.real_source_port
            self.real_destination_address = self.generator.real_destination_address
            self.real_destination_port = self.generator.real_destination_port

            self.toggle_button.setText("Stop")
            self.statusBar.showMessage("Generating traffic...")
        except Exception as e:
            self.statusBar.showMessage(f"Error: {e}")
            self.running = False

    @asyncSlot()
    async def stop_traffic(self):
        """
        Остановка генерации трафика.
        """
        self.running = False
        if self.generator:
            self.generator.running = False
            if hasattr(self.generator, 'threads') and self.generator.threads:
                for thread in self.generator.threads:
                    thread.join()
        self.toggle_button.setText("Start")
        self.statusBar.showMessage("Ready")

    def update_stats(self):
        """
        Обновление статистики и графиков.
        """
        if self.running and self.generator:
            self.ax1.clear()
            self.ax2.clear()
            self.ax2.plot(self.history['time'], self.history['mbps'], label='Mbps', color='orange')
            self.ax1.plot(self.history['time'], self.history['pps'], label='PPS')
            self.ax1.legend()
            self.ax2.legend()
            self.canvas.draw()

            total_time = time.time() - self.start_time
            pps = 0
            mbps = 0
            if total_time > 0:
                pps = self.stats['sent'] / total_time
                mbps = (self.stats['bytes'] / 1000000.0) / total_time

            # Формирование текста статистики
            text = f"<b>Traffic Flow:</b> {self.protocol} {self.real_source_address if self.real_source_address else '0.0.0.0'}"
            if self.protocol != "ICMP":
                text += f":{self.real_source_port if self.real_source_port else '0'}"
            text += " -> "
            if self.real_destination_address:
                text += f"{self.real_destination_address}"
            else:
                text += f"{self.generator.config['destination_address']}"
            if self.protocol == 'UDP':
                text += f":{self.real_destination_port if self.real_destination_port else self.generator.config['destination_port']}"
            text += "<br>"

            if self.generator.config['qos']['dscp'] is not None and self.generator.config['qos']['dscp'] > 0:
                text += f"<b>DSCP:</b> {self.generator.config['qos']['dscp']}<br>"
            if self.generator.config['qos']['ip_precedence'] is not None and self.generator.config['qos']['ip_precedence'] > 0:
                text += f"<b>IP Precedence:</b> {self.saved_ip_prec}<br>"
            if self.generator.config['qos']['ecn'] is not None and self.generator.config['qos']['ecn'] > 0:
                text += f"<b>ECN:</b> {self.generator.config['qos']['ecn']}<br>"

            text += f"<b>Packets Sent:</b> {self.stats['sent']}<br>"
            text += f"<b>Total Bytes:</b> {self.stats['bytes']}<br>"
            text += f"<b>Average Mbps:</b> {mbps:.2f}<br>"
            text += f"<b>Average PPS:</b> {pps:.2f}<br>"
            text += f"<b>Errors:</b> {self.stats['errors']}"

            if text != self.last_stats_text:
                self.stats_text.setText(text)
                self.last_stats_text = text

    def save_config(self):
        """
        Сохранение конфигурации в YAML файл.
        """
        config = {
            'protocol': self.protocol,
            'traffic_type': self.traffic_type.currentText(),
            'source_address': self.source_ip.text(),
            'source_port': self.source_port.text() if self.protocol == 'UDP' else None,
            'destination_address': self.destination_ip.text(),
            'destination_port': self.dest_port.text() if self.protocol == 'UDP' else None,
            'packet_size': self.packet_size.text(),
            'threads': self.threads.text(),
            'speed_mode': self.speed_mode.currentText(),
            'speed_value': self.speed_value.text(),
            'qos': {
                'dscp': self.dscp.text(),
                'ip_precedence': self.ip_prec.text(),
                'ecn': self.ecn.text()
            }
        }

        if not self.validate_config(config):
            return

        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save YAML Config", "",
                                                             "YAML Files (*.yaml);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w', encoding="utf-8") as file:
                    yaml.dump(config, file, indent=2)
                self.statusBar.showMessage(f"Config saved to {file_name}")
            except Exception as e:
                self.statusBar.showMessage(f"Error saving config {e}")

    def validate_config(self, config):
        """
        Валидация конфигурации.
        """
        try:
            validate_ip_address(config.get('source_address'))
            validate_ip_address(config.get('destination_address'))
            if config.get('protocol') == 'UDP':
                validate_port(config.get('destination_port'))
                validate_port(config.get('source_port'))

            validate_packet_size(config.get('packet_size'))
            validate_threads(config.get('threads'))
            float(config.get('speed_value'))

            dscp = config.get('qos', {}).get('dscp')
            if dscp:
                validate_range(dscp, 0, 63)

            ip_prec = config.get('qos', {}).get('ip_precedence')
            if ip_prec:
                validate_range(ip_prec, 0, 7)

            ecn = config.get('qos', {}).get('ecn')
            if ecn:
                validate_range(ecn, 0, 3)
            return True
        except Exception as e:
            self.statusBar.showMessage(f"Error in config: {e}")
            return False

    def load_config(self):
        """
        Загрузка конфигурации из YAML файла.
        """
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open YAML Config", "",
                                                             "YAML Files (*.yaml);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    config = yaml.safe_load(file)
                    if not config:
                        raise ValueError("Empty or invalid YAML file.")
                    if not self.validate_config(config):
                        return
                    print("Loaded config:", config)
                    self.protocol_type.setCurrentText(config.get('protocol', 'UDP'))
                    self.update_protocol()
                    self.traffic_type.setCurrentText(config.get('traffic_type', 'unicast'))
                    self.update_destination_label()
                    self.source_ip.setText(config.get('source_address', '0.0.0.0'))
                    self.source_port.setText(str(config.get('source_port', '0')))
                    self.destination_ip.setText(config.get('destination_address', ''))
                    if config.get('protocol', 'UDP') == 'UDP':
                        self.dest_port.setText(str(config.get('destination_port', '0')))
                    else:
                        self.dest_port.setText("")
                    self.packet_size.setText(str(config.get('packet_size', '512')))
                    self.threads.setText(str(config.get('threads', '1')))
                    self.speed_mode.setCurrentText(config.get('speed_mode', 'mbps'))
                    self.speed_value.setText(str(config.get('speed_value', '1.0')))

                    qos = config.get('qos', {})
                    self.dscp.setText(str(qos.get('dscp', '')))
                    self.ip_prec.setText(str(qos.get('ip_precedence', '')))
                    self.ecn.setText(str(qos.get('ecn', '')))
            except Exception as e:
                self.statusBar.showMessage(f"Failed to load config: {e}")