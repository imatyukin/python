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
        self.last_stats_text = ""  # add
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
        self.destination_ip = QtWidgets.QLineEdit()
        self.source_port = QtWidgets.QLineEdit()
        self.dest_port = QtWidgets.QLineEdit()
        self.packet_size = QtWidgets.QLineEdit()
        self.threads = QtWidgets.QLineEdit()
        self.dscp = QtWidgets.QLineEdit()
        self.ip_prec = QtWidgets.QLineEdit()
        self.ecn = QtWidgets.QLineEdit()

        self.destination_label = QtWidgets.QLabel("Destination IP:")

        fields = [("Source IP:", self.source_ip),
                  (self.destination_label, self.destination_ip),
                  ("Source Port:", self.source_port),
                  ("Destination Port:", self.dest_port),
                  ("Packet Size:", self.packet_size),
                  ("Threads:", self.threads),
                  ("DSCP (0-63):", self.dscp),
                  ("IP Precedence (0-7):", self.ip_prec),
                  ("ECN (0-3):", self.ecn)
                  ]

        for i, (label, widget) in enumerate(fields, start=2):
            if isinstance(label, QtWidgets.QLabel):
                settings_layout.addWidget(label, i, 0)
                settings_layout.addWidget(widget, i, 1)
            else:
                settings_layout.addWidget(QtWidgets.QLabel(label), i, 0)
                settings_layout.addWidget(widget, i, 1)

        self.speed_mode = QtWidgets.QComboBox()
        self.speed_mode.addItems(["kbps", "mbps", "pps", "interval"])
        self.speed_mode.setCurrentText("mbps")
        self.speed_value = QtWidgets.QLineEdit()

        settings_layout.addWidget(QtWidgets.QLabel("Speed Mode:"), len(fields) + 2, 0)
        settings_layout.addWidget(self.speed_mode, len(fields) + 2, 1)
        settings_layout.addWidget(QtWidgets.QLabel("Speed Value:"), len(fields) + 3, 0)
        settings_layout.addWidget(self.speed_value, len(fields) + 3, 1)

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
        self.stats_text.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)  # Add word wrap

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

    def update_destination_label(self):
        if self.traffic_type.currentText() == 'multicast':
            self.destination_label.setText('Group IP:')
        else:
            self.destination_label.setText('Destination IP:')

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
                'source_port': self.validate_port(self.source_port.text()),
                'destination_address': self.destination_ip.text(),
                'destination_port': self.validate_port(self.dest_port.text()),
                'packet_size': self.validate_packet_size(self.packet_size.text()),
                'threads': self.validate_threads(self.threads.text()),
                'speed_mode': self.speed_mode.currentText(),
                'speed_value': float(self.speed_value.text() or 1.0),
                'qos': {
                    'dscp': int(self.dscp.text()) if self.dscp.text() else None,
                    'ip_precedence': int(self.ip_prec.text()) if self.ip_prec.text() else None,
                    'ecn': int(self.ecn.text()) if self.ecn.text() else None
                }
            }

            self.validate_ip_address(config.get('source_address'))
            self.validate_ip_address(config.get('destination_address'))

            print("Starting Traffic Generator with config:", config)
            self.generator = TrafficGenerator(config, self.stats, self.protocol)
            self.thread = threading.Thread(target=self.generator.run, daemon=True)
            self.thread.start()


            self.toggle_button.setText("Stop")
            self.statusBar.showMessage("Generating traffic...")
        except Exception as e:
            self.statusBar.showMessage(f"Error: {e}")
            self.running = False

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

            text = f"<b>Traffic Flow:</b> {self.protocol} {self.generator.real_source_address}:{self.generator.real_source_port} -> {self.generator.real_destination_address}:{self.generator.real_destination_port}<br>"

            if self.generator.config['qos']['dscp'] is not None and self.generator.config['qos']['dscp'] > 0:
                text += f"<b>DSCP:</b> {self.generator.config['qos']['dscp']}<br>"
            if self.generator.config['qos']['ip_precedence'] is not None and self.generator.config['qos'][
                'ip_precedence'] > 0:
                text += f"<b>IP Precedence:</b> {self.generator.config['qos']['ip_precedence']}<br>"
            if self.generator.config['qos']['ecn'] is not None and self.generator.config['qos']['ecn'] > 0:
                text += f"<b>ECN:</b> {self.generator.config['qos']['ecn']}<br>"
            text += f"<b>Packets Sent:</b> {self.stats['sent']}<br>"
            text += f"<b>Total Bytes:</b> {self.stats['bytes']}<br>"
            text += f"<b>Average Mbps:</b> {mbps:.2f}<br>"
            text += f"<b>Average PPS:</b> {pps:.2f}<br>"
            text += f"<b>Errors:</b> {self.stats['errors']}"

            if text != self.last_stats_text:  # if it changes
                self.stats_text.setText(text)
                self.last_stats_text = text

    def save_config(self):
        config = {
            'protocol': self.protocol,
            'traffic_type': self.traffic_type.currentText(),
            'source_address': self.source_ip.text(),
            'source_port': self.source_port.text(),
            'destination_address': self.destination_ip.text(),
            'destination_port': self.dest_port.text(),
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
            self.validate_port(config.get('source_port'))
            self.validate_port(config.get('destination_port'))
            self.validate_packet_size(config.get('packet_size'))
            self.validate_threads(config.get('threads'))
            float(config.get('speed_value'))

            dscp = config.get('qos', {}).get('dscp')
            if dscp:
                self.validate_range(dscp, 0, 63)
            ip_prec = config.get('qos', {}).get('ip_precedence')
            if ip_prec:
                self.validate_range(ip_prec, 0, 7)
            ecn = config.get('qos', {}).get('ecn')
            if ecn:
                self.validate_range(ecn, 0, 3)
            return True
        except Exception as e:
            self.statusBar.showMessage(f"Error in config: {e}")
            return False

    def validate_ip_address(self, ip_str):
        try:
            ipaddress.ip_address(ip_str)
            return ip_str
        except ValueError:
            self.statusBar.showMessage(f"Error: invalid IP address {ip_str}")
            raise

    def validate_port(self, port_str):
        try:
            port = int(port_str)
            if 0 <= port <= 65535:
                return port
            else:
                self.statusBar.showMessage(f"Error: Invalid port number {port_str}. Must be between 0 and 65535")
                raise ValueError("Invalid port number")
        except ValueError:
            self.statusBar.showMessage(f"Error: Invalid port number {port_str}. Must be an integer")
            raise

    def validate_packet_size(self, packet_size_str):
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
        if not value.isdigit():
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
                    self.destination_ip.setText(config.get('destination_address', ''))
                    self.source_port.setText(str(config.get('source_port', '0')))
                    self.dest_port.setText(str(config.get('destination_port', '0')))
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
    def __init__(self, config, stats, protocol):
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

    def run(self):
        self.running = True
        start_time = time.time()
        if self.config['speed_mode'] == 'interval':
            self.interval_time = 1 / self.config['speed_value']

        for _ in range(self.config['threads']):
            thread = threading.Thread(target=self.send_packet, daemon=True)
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

    def stats_update(self, current_time, pps, mbps):
        if isinstance(current_time, float) and isinstance(pps, (int, float)) and isinstance(mbps, (int, float)):
            if current_time >= 0:
                window.history['time'].append(current_time)
                window.history['pps'].append(pps)
                window.history['mbps'].append(mbps)

    def send_packet(self):
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

                if self.config['source_address'] == '0.0.0.0':
                    sock.bind(('0.0.0.0', 0))
                    self.real_source_address, self.real_source_port = sock.getsockname()
                else:
                    self.real_source_address = self.config['source_address']
                    self.real_source_port = self.config['source_port']

                self.real_destination_address = destination_address
                self.real_destination_port = self.config['destination_port']

                message = os.urandom(self.config['packet_size'])

            elif self.protocol == "ICMP":
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                if self.config['source_address'] == '0.0.0.0':
                    sock.bind(('0.0.0.0', 0))
                    self.real_source_address, self.real_source_port = sock.getsockname()
                else:
                    self.real_source_address = self.config['source_address']
                    self.real_source_port = self.config['source_port']

                self.real_destination_address = self.config['destination_address']
                self.real_destination_port = self.config['destination_port']

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

        except Exception as e:
            with self.lock:
                self.stats['errors'] += 1
            print(f"Error sending packet: {e}")
            window.statusBar.showMessage(f"Error sending packet: {e}")
        finally:
            if sock:
                sock.close()

    def create_icmp_packet(self, packet_size):
        icmp_type = 8  # ICMP Echo Request
        icmp_code = 0
        icmp_checksum = 0
        icmp_id = 12345
        icmp_sequence = 0

        header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence)
        data = os.urandom(packet_size - len(header))
        icmp_checksum = self.calculate_checksum(header + data)
        header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence)
        return header + data

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