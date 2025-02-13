from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import socket
import time
import os
import yaml
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import ipaddress
import struct
import asyncio
from qasync import QEventLoop, asyncSlot, QApplication
import threading


class TrafficGeneratorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Traffic Generator v.2.0")
        self.setGeometry(100, 100, 1000, 800)
        self.running = False
        self.generator = None
        self.stats = {'sent': 0, 'errors': 0, 'bytes': 0}
        self.history = {'time': [], 'pps': [], 'mbps': []}
        self.start_time = 0
        self.protocol = 'UDP'  # Default protocol
        self.last_stats_text = ""
        self.saved_ip_prec = 0
        self.real_source_address = None
        self.real_source_port = None
        self.real_destination_address = None
        self.real_destination_port = None
        self.initUI()

    def initUI(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)

        settings_group = QtWidgets.QGroupBox("Settings")
        settings_layout = QtWidgets.QGridLayout()
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        self.traffic_type = QtWidgets.QComboBox()
        self.traffic_type.addItems(["unicast", "broadcast", "multicast"])
        settings_layout.addWidget(QtWidgets.QLabel("Traffic Type:"), 0, 0)
        settings_layout.addWidget(self.traffic_type, 0, 1)
        self.traffic_type.currentIndexChanged.connect(self.update_destination_label)

        self.protocol_type = QtWidgets.QComboBox()
        self.protocol_type.addItems(["UDP", "ICMP"])
        settings_layout.addWidget(QtWidgets.QLabel("Protocol:"), 1, 0)
        settings_layout.addWidget(self.protocol_type, 1, 1)
        self.protocol_type.currentIndexChanged.connect(self.update_protocol)

        self.source_ip = QtWidgets.QLineEdit()
        self.source_port = QtWidgets.QLineEdit()
        self.destination_ip = QtWidgets.QLineEdit()
        self.dest_port = QtWidgets.QLineEdit()
        self.packet_size = QtWidgets.QLineEdit()
        self.threads = QtWidgets.QLineEdit()
        self.dscp = QtWidgets.QLineEdit()
        self.ip_prec = QtWidgets.QLineEdit()
        self.ecn = QtWidgets.QLineEdit()

        self.destination_label = QtWidgets.QLabel("Destination IP:")

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

        self.protocol_fields = {
            "udp": ["Source IP:", "Source Port:", "Destination IP:", "Destination Port:", "Packet Size:", "Threads:",
                    "DSCP (0-63):", "IP Precedence (0-7):", "ECN (0-3):"],
            "icmp": ["Source IP:", "Destination IP:", "Packet Size:", "Threads:", "DSCP (0-63):",
                     "IP Precedence (0-7):", "ECN (0-3):"]
        }

        self.field_widgets = {}
        row_counter = 2
        for label_text, widget in self.all_fields.items():
            label = QtWidgets.QLabel(label_text)
            settings_layout.addWidget(label, row_counter, 0)
            settings_layout.addWidget(widget, row_counter, 1)
            self.field_widgets[label_text] = (label, widget)
            row_counter += 1

        self.speed_mode = QtWidgets.QComboBox()
        self.speed_mode.addItems(["kbps", "mbps", "pps", "interval"])
        self.speed_mode.setCurrentText("mbps")
        self.speed_value = QtWidgets.QLineEdit()

        settings_layout.addWidget(QtWidgets.QLabel("Speed Mode:"), row_counter, 0)
        settings_layout.addWidget(self.speed_mode, row_counter, 1)
        row_counter += 1
        settings_layout.addWidget(QtWidgets.QLabel("Speed Value:"), row_counter, 0)
        settings_layout.addWidget(self.speed_value, row_counter, 1)

        self.update_visible_fields()

        self.toggle_button = QtWidgets.QPushButton("Start")
        self.toggle_button.clicked.connect(self.toggle_traffic)
        layout.addWidget(self.toggle_button)

        self.load_button = QtWidgets.QPushButton("Load Config")
        self.load_button.clicked.connect(self.load_config)
        layout.addWidget(self.load_button)

        self.save_button = QtWidgets.QPushButton("Save Config")
        self.save_button.clicked.connect(self.save_config)
        layout.addWidget(self.save_button)

        self.figure, (self.ax2, self.ax1) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.ax2.plot([], [], label='Mbps', color='orange')
        self.ax1.plot([], [], label='PPS')
        self.ax1.legend()
        self.ax2.legend()
        self.canvas.draw()

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

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_stats)
        self.update_timer.start(1000)

    def update_protocol(self):
        self.protocol = self.protocol_type.currentText()
        self.update_visible_fields()

    def update_visible_fields(self):
        current_protocol = self.protocol_type.currentText().lower()
        for label_text, (label, widget) in self.field_widgets.items():
            if label_text in self.protocol_fields.get(current_protocol, []):
                label.setVisible(True)
                if widget:
                    widget.setVisible(True)
            else:
                label.setVisible(False)
                if widget:
                    widget.setVisible(False)

    def update_destination_label(self):
        if self.traffic_type.currentText() == 'multicast':
            self.field_widgets["Destination IP:"][0].setText('Group IP:')
        else:
            self.field_widgets["Destination IP:"][0].setText('Destination IP:')

    def update_real_values(self, real_source_address, real_source_port, real_destination_address,
                           real_destination_port):
        self.real_source_address = real_source_address
        self.real_source_port = real_source_port
        self.real_destination_address = real_destination_address
        self.real_destination_port = real_destination_port

    @asyncSlot()
    async def toggle_traffic(self):
        if self.running:
            await self.stop_traffic()
        else:
            await self.start_traffic()

    @asyncSlot()
    async def start_traffic(self):
        try:
            self.running = True
            self.start_time = time.time()
            self.stats = {'sent': 0, 'errors': 0, 'bytes': 0}
            self.history = {'time': [], 'pps': [], 'mbps': []}

            config = {
                'traffic_type': self.traffic_type.currentText(),
                'source_address': self.source_ip.text(),
                'source_port': self.validate_port(self.source_port.text()) if self.protocol == 'UDP' else 0,
                'destination_address': self.destination_ip.text(),
                'destination_port': self.validate_port(self.dest_port.text()) if self.protocol == 'UDP' else 0,
                'packet_size': self.validate_packet_size(self.packet_size.text()),
                'threads': self.validate_threads(self.threads.text()),
                'speed_mode': self.speed_mode.currentText(),
                'speed_value': float(self.speed_value.text() or 1.0),
                'qos': {
                    'dscp': self.validate_dscp(self.dscp.text()),
                    'ip_precedence': self.validate_ip_prec(self.ip_prec.text()),
                    'ecn': self.validate_ecn(self.ecn.text())
                }
            }

            if config['qos']['ip_precedence'] is not None:
                self.saved_ip_prec = config['qos']['ip_precedence']
            else:
                self.saved_ip_prec = 0

            self.validate_ip_address(config.get('source_address'))
            self.validate_ip_address(config.get('destination_address'))

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
            return  # Прерываем выполнение метода в случае ошибки

    @asyncSlot()
    async def stop_traffic(self):
        self.running = False
        if self.generator:
            self.generator.running = False
            if hasattr(self.generator, 'threads') and self.generator.threads:
                for thread in self.generator.threads:
                    thread.join()
        self.toggle_button.setText("Start")
        self.statusBar.showMessage("Ready")

    def update_stats(self):
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

            # Формируем строку Traffic Flow
            text = f"<b>Traffic Flow:</b> {self.protocol} {self.real_source_address if self.real_source_address else '0.0.0.0'}"

            # Если протокол не ICMP, добавляем порт источника
            if self.protocol != "ICMP":
                text += f":{self.real_source_port if self.real_source_port else '0'}"

            text += " -> "

            # Адрес назначения
            if self.real_destination_address:
                text += f"{self.real_destination_address}"
            else:
                text += f"{self.generator.config['destination_address']}"

            # Если протокол UDP, добавляем порт назначения
            if self.protocol == 'UDP':
                text += f":{self.real_destination_port if self.real_destination_port else self.generator.config['destination_port']}"

            text += "<br>"

            # QoS параметры
            if self.generator.config['qos']['dscp'] is not None and self.generator.config['qos']['dscp'] > 0:
                text += f"<b>DSCP:</b> {self.generator.config['qos']['dscp']}<br>"
            if self.generator.config['qos']['ip_precedence'] is not None and self.generator.config['qos'][
                'ip_precedence'] > 0:
                text += f"<b>IP Precedence:</b> {self.saved_ip_prec}<br>"
            if self.generator.config['qos']['ecn'] is not None and self.generator.config['qos']['ecn'] > 0:
                text += f"<b>ECN:</b> {self.generator.config['qos']['ecn']}<br>"

            # Статистика трафика
            text += f"<b>Packets Sent:</b> {self.stats['sent']}<br>"
            text += f"<b>Total Bytes:</b> {self.stats['bytes']}<br>"
            text += f"<b>Average Mbps:</b> {mbps:.2f}<br>"
            text += f"<b>Average PPS:</b> {pps:.2f}<br>"
            text += f"<b>Errors:</b> {self.stats['errors']}"

            # Обновляем только если данные изменились
            if text != self.last_stats_text:
                self.stats_text.setText(text)
                self.last_stats_text = text

    def save_config(self):
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
        try:
            self.validate_ip_address(config.get('source_address'))
            self.validate_ip_address(config.get('destination_address'))
            if config.get('protocol') == 'UDP':
                self.validate_port(config.get('destination_port'))
                self.validate_port(config.get('source_port'))

            self.validate_packet_size(config.get('packet_size'))
            self.validate_threads(config.get('threads'))
            float(config.get('speed_value'))

            dscp = config.get('qos', {}).get('dscp')
            if dscp:
                self.validate_dscp(dscp)

            ip_prec = config.get('qos', {}).get('ip_precedence')
            if ip_prec:
                self.validate_ip_prec(ip_prec)

            ecn = config.get('qos', {}).get('ecn')
            if ecn:
                self.validate_ecn(ecn)
            return True
        except Exception as e:
            self.statusBar.showMessage(f"Error in config: {e}")
            return False

    def validate_dscp(self, value):
        if not value:
            return None
        if not isinstance(value, str) or not value.isdigit():
            self.statusBar.showMessage(f"Error: Invalid DSCP value {value}. Must be an integer")
            return None
        val = int(value)
        if 0 <= val <= 63:
            return val
        else:
            self.statusBar.showMessage(f"Error: Invalid DSCP value {val}. Must be between 0 and 63")
            return None

    def validate_ip_prec(self, value):
        if not value:
            return None
        if not isinstance(value, str) or not value.isdigit():
            self.statusBar.showMessage(f"Error: Invalid IP Precedence value {value}. Must be an integer")
            return None
        val = int(value)
        if 0 <= val <= 7:
            return val
        else:
            self.statusBar.showMessage(f"Error: Invalid IP Precedence value {val}. Must be between 0 and 7")
            return None

    def validate_ecn(self, value):
        if not value:
            return None
        if not isinstance(value, str) or not value.isdigit():
            self.statusBar.showMessage(f"Error: Invalid ECN value {value}. Must be an integer")
            return None
        val = int(value)
        if 0 <= val <= 3:
            return val
        else:
            self.statusBar.showMessage(f"Error: Invalid ECN value {val}. Must be between 0 and 3")
            return None

    def validate_ip_address(self, ip_str):
        try:
            ipaddress.ip_address(ip_str)
            return ip_str
        except ValueError:
            self.statusBar.showMessage(f"Error: invalid IP address {ip_str}")
            raise

    def validate_port(self, port_str):
        if port_str is None or not isinstance(port_str, str) or port_str == "":
            return 0
        try:
            port = int(port_str)
            if 0 <= port <= 65535:
                return port
            else:
                self.statusBar.showMessage(f"Error: Invalid port number {port_str}. Must be between 0 and 65535")
                raise ValueError("Invalid port number")
        except ValueError as e:
            self.statusBar.showMessage(f"Error: Invalid port number {port_str}. Must be an integer. {e}")
            raise

    def validate_packet_size(self, packet_size_str):
        if packet_size_str is None or not isinstance(packet_size_str, str):
            self.statusBar.showMessage("Error: Packet size must be a string")
            raise ValueError("Invalid packet size")
        try:
            packet_size = int(packet_size_str)
            if 1 <= packet_size <= 65507:
                return packet_size
            else:
                self.statusBar.showMessage(f"Error: Invalid packet size {packet_size_str}. Must be between 1 and 65507")
                raise ValueError("Invalid packet size")
        except ValueError:
            self.statusBar.showMessage(f"Error: Invalid packet size {packet_size_str}. Must be an integer")
            raise

    def validate_threads(self, threads_str):
        try:
            threads = int(threads_str)
            if 1 <= threads <= 100:
                return threads
            else:
                self.statusBar.showMessage(f"Error: Invalid thread count {threads_str}. Must be between 1 and 100")
                raise ValueError("Invalid thread count")
        except ValueError:
            self.statusBar.showMessage(f"Error: Invalid thread count {threads_str}. Must be an integer")
            raise

    def validate_range(self, value, min_val, max_val):
        if not value:
            return None
        if not isinstance(value, int):
            self.statusBar.showMessage(f"Error: Invalid value {value}. Must be an integer")
            return None
        val = int(value)
        if min_val <= val <= max_val:
            return val
        else:
            self.statusBar.showMessage(f"Error: Invalid value {val}. Must be between {min_val} and {max_val}")
            return None

    def load_config(self):
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


class TrafficGenerator:
    def __init__(self, config, stats, protocol, app_instance):
        self.config = config
        self.stats = stats
        self.running = False
        self.interval_time = 0
        self.real_source_address = None
        self.real_source_port = None
        self.real_destination_address = None
        self.real_destination_port = None
        self.protocol = protocol
        self.lock = threading.Lock()
        self.threads = []
        self.last_send_time = 0
        self.tcp_tasks = []
        self.app_instance = app_instance
        self.sockets = []

    def run(self):
        self.running = True
        start_time = time.time()
        if self.config['speed_mode'] == 'interval':
            self.interval_time = 1 / self.config['speed_value']

        # Создаем и биндим сокеты для каждого потока
        for _ in range(self.config['threads']):
            sock = self.create_and_bind_socket()
            if sock:
                self.sockets.append(sock)
            else:
                self.running = False
                return

        # Обновление реальных значений в UI перед запуском потоков
        if self.sockets:
            self.real_source_address, self.real_source_port = self.sockets[0].getsockname()
            self.app_instance.update_real_values(
                self.real_source_address, self.real_source_port,
                self.real_destination_address, self.real_destination_port
            )

        # Запускаем потоки
        for i in range(self.config['threads']):
            thread = threading.Thread(target=self.send_packet, args=(self.sockets[i],), daemon=True)
            self.threads.append(thread)
            thread.start()

        try:
            while self.running:
                current_time = time.time() - start_time
                pps = 0
                mbps = 0

                if current_time > 0:
                    with self.lock:
                        pps = self.stats['sent'] / current_time
                        mbps = (self.stats['bytes'] / 1000000.0) / current_time

                self.stats_update(current_time, pps, mbps)
                time.sleep(0.1)
        except Exception as e:
            print(f"Error in generator: {e}")
        finally:
            print("Generator stopped.")
            for sock in self.sockets:
                if sock:
                    sock.close()

    def stats_update(self, current_time, pps, mbps):
        if isinstance(current_time, float) and isinstance(pps, (int, float)) and isinstance(mbps, (int, float)):
            if current_time >= 0:
                self.app_instance.history['time'].append(current_time)
                self.app_instance.history['pps'].append(pps)
                self.app_instance.history['mbps'].append(mbps)

    def create_and_bind_socket(self):
        sock = None
        try:
            if self.protocol == "UDP":
                if self.config['traffic_type'] == 'broadcast':
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    destination_address = '<broadcast>'
                elif self.config['traffic_type'] == 'multicast':
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    destination_address = self.config['destination_address']
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    destination_address = self.config['destination_address']

                source_port = int(self.config.get('source_port', 0))
                source_address = self.config.get('source_address', '0.0.0.0')

                try:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.bind((source_address, source_port))
                    self.real_source_address, self.real_source_port = sock.getsockname()
                except OSError as e:
                    self.app_instance.statusBar.showMessage(
                        f"Warning: Could not bind to {source_address}:{source_port}, letting OS choose. Error: {e}")
                    sock.close()
                    return None

                self.real_destination_address = self.config['destination_address']
                self.real_destination_port = self.config['destination_port']

                return sock
            elif self.protocol == "ICMP":
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                if self.config['source_address'] == '0.0.0.0':
                    sock.bind(('0.0.0.0', 0))
                    self.real_source_address, self.real_source_port = sock.getsockname()
                else:
                    sock.bind((self.config['source_address'], 0))
                    self.real_source_address, self.real_source_port = sock.getsockname()
                self.real_destination_address = self.config['destination_address']
                self.real_destination_port = self.config['destination_port']
                return sock
        except Exception as e:
            self.app_instance.statusBar.showMessage(f"Error creating and binding socket: {e}")
            return None

    def send_packet(self, sock):
        try:
            message = None
            if self.protocol == "UDP":
                message = os.urandom(self.config['packet_size'])
            elif self.protocol == "ICMP":
                message = self.create_icmp_packet(self.config['packet_size'])

            # Расчет времени ожидания для скорости
            if self.config['speed_mode'] == 'mbps':
                packet_size_bytes = self.config['packet_size']
                mbps = self.config['speed_value']
                bytes_per_second = mbps * 125000  # 1 Mbps = 125000 bytes/sec
                time_wait = packet_size_bytes / bytes_per_second
            elif self.config['speed_mode'] == 'kbps':
                packet_size_bytes = self.config['packet_size']
                kbps = self.config['speed_value']
                bytes_per_second = kbps * 1000  # 1 Kbps = 1000 bytes/sec
                time_wait = packet_size_bytes / bytes_per_second
            elif self.config['speed_mode'] == 'interval':
                time_wait = self.interval_time
            else:
                time_wait = 0  # Без задержки

            start_time = time.time()

            while self.running:
                if self.protocol == "UDP":
                    sock.sendto(message, (self.real_destination_address, self.config['destination_port']))
                elif self.protocol == "ICMP":
                    sock.sendto(message, (self.real_destination_address, 0))

                with self.lock:
                    self.stats['sent'] += 1
                    self.stats['bytes'] += len(message)

                if time_wait > 0:
                    time.sleep(time_wait)

                start_time = time.time()
            self.app_instance.update_real_values(self.real_source_address, self.real_source_port,
                                                 self.real_destination_address, self.real_destination_port)
        except Exception as e:
            with self.lock:
                self.stats['errors'] += 1
            print(f"Error sending packet: {e}")
            self.app_instance.statusBar.showMessage(f"Error sending packet: {e}")

    def create_icmp_packet(self, packet_size):
        icmp_type = 8  # ICMP Echo Request
        icmp_code = 0
        icmp_checksum = 0
        icmp_id = 12345
        icmp_sequence = 0

        # Формируем TOS (DSCP + IP Precedence + ECN)
        dscp = self.config['qos']['dscp'] or 0
        ip_prec = self.config['qos']['ip_precedence'] or 0
        ecn = self.config['qos']['ecn'] or 0
        tos = (ip_prec << 5) | (dscp << 2) | ecn  # Корректный расчет

        # Создаем IP-заголовок
        ip_header = struct.pack("!BBHHHBBH4s4s",
                                0x45, tos, 20 + packet_size, 12345, 0, 64, 1,
                                0,  # Checksum (будет рассчитан позже)
                                socket.inet_aton(self.config['source_address']),
                                socket.inet_aton(self.config['destination_address'])
                                )

        # Добавляем контрольную сумму для IP-заголовка (необязательно на Windows)
        ip_checksum = self.calculate_checksum(ip_header)
        ip_header = struct.pack("!BBHHHBBH4s4s",
                                0x45, tos, 20 + packet_size, 12345, 0, 64, 1,
                                ip_checksum,
                                socket.inet_aton(self.config['source_address']),
                                socket.inet_aton(self.config['destination_address'])
                                )

        # Создаем ICMP-заголовок
        header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence)
        data = os.urandom(packet_size - len(header) - len(ip_header))

        # Вычисляем ICMP-чек-сумму
        icmp_checksum = self.calculate_checksum(header + data)
        header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence)

        return ip_header + header + data

    def calculate_checksum(self, data):
        s = 0
        n = len(data) % 2
        for i in range(0, len(data) - n, 2):
            s += data[i] + (data[i + 1] << 8)
        if n:
            s += data[len(data) - 1]
        while (s >> 16):
            s = (s & 0xFFFF) + (s >> 16)
        s = ~s & 0xffff
        return s


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = TrafficGeneratorApp()
    window.show()
    with loop:
        loop.run_forever()