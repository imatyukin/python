from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import socket
import threading
import time
import os
import yaml
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import ipaddress
import subprocess


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
        self.tcp_server_process = None
        self.icmp_server_process = None
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

        self.source_ip = QtWidgets.QLineEdit()
        self.destination_ip = QtWidgets.QLineEdit()
        self.source_port = QtWidgets.QLineEdit()
        self.dest_port = QtWidgets.QLineEdit()
        self.packet_size = QtWidgets.QLineEdit()
        self.threads = QtWidgets.QLineEdit()

        self.destination_label = QtWidgets.QLabel("Destination IP:")

        fields = [("Source IP:", self.source_ip),
                  (self.destination_label, self.destination_ip),
                  ("Source Port:", self.source_port),
                  ("Destination Port:", self.dest_port),
                  ("Packet Size:", self.packet_size),
                  ]

        for i, (label, widget) in enumerate(fields, start=1):
            if isinstance(label, QtWidgets.QLabel):
                settings_layout.addWidget(label, i, 0)
                settings_layout.addWidget(widget, i, 1)
            else:
                settings_layout.addWidget(QtWidgets.QLabel(label), i, 0)
                settings_layout.addWidget(widget, i, 1)

        self.protocol_type = QtWidgets.QComboBox()
        self.protocol_type.addItems(["UDP", "TCP", "ICMP"])
        self.protocol_type.setCurrentText("UDP")
        self.protocol_type.currentIndexChanged.connect(self.update_protocol)
        settings_layout.addWidget(QtWidgets.QLabel("Protocol:"), len(fields) + 1, 0)
        settings_layout.addWidget(self.protocol_type, len(fields) + 1, 1)

        self.speed_mode = QtWidgets.QComboBox()
        self.speed_mode.addItems(["kbps", "mbps", "pps", "interval"])
        self.speed_mode.setCurrentText("mbps")
        self.speed_value = QtWidgets.QLineEdit()

        settings_layout.addWidget(QtWidgets.QLabel("Speed Mode:"), len(fields) + 2, 0)
        settings_layout.addWidget(self.speed_mode, len(fields) + 2, 1)
        settings_layout.addWidget(QtWidgets.QLabel("Speed Value:"), len(fields) + 3, 0)
        settings_layout.addWidget(self.speed_value, len(fields) + 3, 1)

        settings_layout.addWidget(QtWidgets.QLabel("Threads:"), len(fields) + 4, 0)
        settings_layout.addWidget(self.threads, len(fields) + 4, 1)

        self.toggle_button = QtWidgets.QPushButton("Start")
        self.toggle_button.clicked.connect(self.toggle_traffic)
        layout.addWidget(self.toggle_button)

        self.load_button = QtWidgets.QPushButton("Load Config")
        self.load_button.clicked.connect(self.load_config)
        layout.addWidget(self.load_button)

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

        initial_stats_text = "Protocol: UDP\n"
        initial_stats_text += "Source IP: \n"
        initial_stats_text += "Source Port: \n"
        initial_stats_text += "Destination IP: \n"
        initial_stats_text += "Destination Port: \n"
        initial_stats_text += "Packets Sent: 0\n"
        initial_stats_text += "Errors: 0\n"
        initial_stats_text += "Total Bytes: 0\n"
        initial_stats_text += "Average PPS: 0.00\n"
        initial_stats_text += "Average Mbps: 0.00"
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

    def toggle_traffic(self):
        if self.running:
            self.stop_traffic()

        else:
            self.start_traffic()

    def start_servers(self, protocol, dest_port):
        if protocol == 'TCP':
            if self.tcp_server_process is None:
                try:
                    self.tcp_server_process = subprocess.Popen([sys.executable, 'tcp_server.py', str(dest_port)])
                    self.statusBar.showMessage(f"TCP server started on port {dest_port}")
                except Exception as e:
                    self.statusBar.showMessage(f"Error starting TCP server: {e}")
                    self.tcp_server_process = None
        elif protocol == 'ICMP':
            if self.icmp_server_process is None:
                try:
                    self.icmp_server_process = subprocess.Popen([sys.executable, 'icmp_server.py'])
                    self.statusBar.showMessage(f"ICMP server started")
                except Exception as e:
                    self.statusBar.showMessage(f"Error starting ICMP server: {e}")
                    self.icmp_server_process = None

    def stop_servers(self, protocol):
        if protocol == 'TCP':
            if self.tcp_server_process:
                self.tcp_server_process.terminate()
                self.tcp_server_process = None
                self.statusBar.showMessage("TCP server stopped")
        elif protocol == 'ICMP':
            if self.icmp_server_process:
                self.icmp_server_process.terminate()
                self.icmp_server_process = None
                self.statusBar.showMessage("ICMP server stopped")

    def start_traffic(self):
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
                'speed_value': float(self.speed_value.text() or 1.0)
            }

            self.validate_ip_address(config.get('source_address'))
            self.validate_ip_address(config.get('destination_address'))

            self.start_servers(self.protocol, config['destination_port'])

            print("Starting Traffic Generator with config:", config)
            self.generator = TrafficGenerator(config, self.stats, self.protocol)
            self.thread = threading.Thread(target=self.generator.run, daemon=True)
            self.thread.start()

            self.toggle_button.setText("Stop")
            self.statusBar.showMessage("Generating traffic...")
        except Exception as e:
            self.statusBar.showMessage(f"Error: {e}")
            self.running = False

    def stop_traffic(self):
        self.running = False
        if self.generator:
            self.generator.running = False
        self.stop_servers(self.protocol)
        self.toggle_button.setText("Start")
        self.statusBar.showMessage("Ready")

    def update_stats(self):
        if self.running:
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

            text = f"Protocol: {self.protocol}\n"
            text += f"Source IP: {self.generator.real_source_address}\n"
            text += f"Source Port: {self.generator.real_source_port}\n"
            text += f"Destination IP: {self.generator.real_destination_address}\n"
            text += f"Destination Port: {self.generator.real_destination_port}\n"
            text += f"Packets Sent: {self.stats['sent']}\n"
            text += f"Errors: {self.stats['errors']}\n"
            text += f"Total Bytes: {self.stats['bytes']}\n"
            text += f"Average PPS: {pps:.2f}\n"
            text += f"Average Mbps: {mbps:.2f}"

            self.stats_text.setText(text)

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

                    print("Loaded config:", config)
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

    def run(self):
        self.running = True
        start_time = time.time()
        if self.config['speed_mode'] == 'interval':
            self.interval_time = 1 / self.config['speed_value']
        try:
            while self.running:
                self.send_packet()
                if self.config['speed_mode'] == 'pps':
                    time_wait = 1 / self.config['speed_value']
                    time.sleep(time_wait)
                elif self.config['speed_mode'] == 'mbps':
                    packet_size_bytes = self.config['packet_size']
                    mbps = self.config['speed_value']
                    bytes_per_second = mbps * 125000
                    time_wait = packet_size_bytes / bytes_per_second
                    time.sleep(time_wait)
                elif self.config['speed_mode'] == 'kbps':
                    packet_size_bytes = self.config['packet_size']
                    kbps = self.config['speed_value']
                    bytes_per_second = kbps * 1000
                    time_wait = packet_size_bytes / bytes_per_second
                    time.sleep(time_wait)
                elif self.config['speed_mode'] == 'interval':
                    time.sleep(self.interval_time)

                current_time = time.time() - start_time
                pps = 0
                mbps = 0

                if current_time > 0:
                    pps = self.stats['sent'] / current_time
                    mbps = (self.stats['bytes'] / 1000000.0) / current_time

                self.stats_update(current_time, pps, mbps)
        except Exception as e:
            print(f"Error in generator: {e}")
        finally:
            print("Generator stopped.")

    def send_packet(self):
        sock = None
        try:
            if self.protocol == 'TCP':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if self.config['source_address'] == '0.0.0.0':
                    sock.bind(('0.0.0.0', 0))
                else:
                    sock.bind((self.config['source_address'], 0))
                self.real_source_address, self.real_source_port = sock.getsockname()
                sock.connect((self.config['destination_address'], self.config['destination_port']))
                message = os.urandom(self.config['packet_size'])
                sock.sendall(message)
            elif self.protocol == 'ICMP':
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                if self.config['source_address'] == '0.0.0.0':
                    sock.bind(('0.0.0.0', 0))
                else:
                    sock.bind((self.config['source_address'], 0))

                self.real_source_address, self.real_source_port = sock.getsockname()

                # Собираем ICMP пакет вручную
                icmp_type = 8  # ICMP Echo Request
                icmp_code = 0
                icmp_checksum = 0
                icmp_identifier = os.getpid() & 0xFFFF
                icmp_sequence = self.stats['sent'] & 0xFFFF

                icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_identifier, icmp_sequence)
                message = os.urandom(self.config['packet_size'] - len(icmp_header))
                icmp_checksum = self.calculate_checksum(icmp_header + message)
                icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_identifier, icmp_sequence)

                packet = icmp_header + message
                sock.sendto(packet, (self.config['destination_address'], 0))
            else:  # UDP
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

                message = os.urandom(self.config['packet_size'])
                sock.sendto(message, (destination_address, self.config['destination_port']))

            self.real_destination_address = self.config['destination_address']
            self.real_destination_port = self.config['destination_port']

            self.stats['sent'] += 1
            self.stats['bytes'] += len(message)


        except Exception as e:
            self.stats['errors'] += 1
            print(f"Error sending packet: {e}")
            window.statusBar.showMessage(f"Error sending packet: {e}")
        finally:
            if sock:
                sock.close()

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

    def stats_update(self, current_time, pps, mbps):
        if isinstance(current_time, float) and isinstance(pps, (int, float)) and isinstance(mbps, (int, float)):
            if current_time >= 0:
                window.history['time'].append(current_time)
                window.history['pps'].append(pps)
                window.history['mbps'].append(mbps)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrafficGeneratorApp()
    window.show()
    sys.exit(app.exec_())