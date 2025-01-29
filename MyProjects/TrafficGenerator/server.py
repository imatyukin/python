import socket
import sys
import threading
import time
import struct
from PyQt5 import QtWidgets, QtGui, QtCore


class ServerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Combined Server")
        self.setGeometry(100, 100, 600, 400)
        self.running = False
        self.stats = {'tcp_sent': 0, 'tcp_recv': 0, 'icmp_sent': 0, 'icmp_recv': 0}
        self.server_address = None
        self.initUI()

    def initUI(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        self.protocol_type = QtWidgets.QComboBox()
        self.protocol_type.addItems(["TCP", "ICMP"])
        self.protocol_type.setCurrentText("TCP")
        layout.addWidget(QtWidgets.QLabel("Protocol:"))
        layout.addWidget(self.protocol_type)

        self.port_label = QtWidgets.QLabel("Port")
        self.port_input = QtWidgets.QLineEdit()
        self.port_input.setText("5060")

        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)

        self.server_ip_label = QtWidgets.QLabel("Server IP: Not Started")  # Label для IP
        layout.addWidget(self.server_ip_label)

        self.toggle_button = QtWidgets.QPushButton("Start Server")
        self.toggle_button.clicked.connect(self.toggle_server)
        layout.addWidget(self.toggle_button)

        self.stats_text = QtWidgets.QTextEdit()
        self.stats_text.setReadOnly(True)
        layout.addWidget(self.stats_text)

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_stats)
        self.update_timer.start(1000)

    def toggle_server(self):
        if self.running:
            self.stop_server()
        else:
            self.start_server()

    def start_server(self):
        self.running = True
        protocol = self.protocol_type.currentText()
        port = int(self.port_input.text())
        self.toggle_button.setText("Stop Server")
        self.stats_text.clear()
        self.stats = {'tcp_sent': 0, 'tcp_recv': 0, 'icmp_sent': 0, 'icmp_recv': 0}
        self.thread = threading.Thread(target=self.run_server, args=(protocol, port), daemon=True)
        self.thread.start()
        self.statusBar().showMessage(f'{protocol} server started...')

    def stop_server(self):
        self.running = False
        self.toggle_button.setText("Start Server")
        self.server_ip_label.setText("Server IP: Not Started")  # clear IP label
        self.statusBar().showMessage("Server stopped")

    def run_server(self, protocol, port):
        try:
            if protocol == 'TCP':
                self.server_address = self.run_tcp_server(port)
            elif protocol == 'ICMP':
                self.server_address = self.run_icmp_server()

            if self.server_address:
                self.server_ip_label.setText(
                    f"Server IP: {self.server_address[0]}:{self.server_address[1] if protocol == 'TCP' else 'N/A'}")  # update IP label
            else:
                self.server_ip_label.setText(f"Server IP: N/A")  # update IP label
        except Exception as e:
            print(f'Error: {e}')
            self.statusBar().showMessage(f'Error: {e}')
        finally:
            print("Server stopped")

    def run_tcp_server(self, port):
        HOST = '0.0.0.0'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, port))
            s.listen()
            server_address = s.getsockname()
            while self.running:
                try:
                    conn, addr = s.accept()
                    with conn:
                        print(f'TCP Server connected by {addr}')
                        while self.running:
                            data = conn.recv(1024)
                            if not data:
                                break
                            self.stats['tcp_recv'] += len(data)
                            conn.sendall(data)
                            self.stats['tcp_sent'] += len(data)
                except socket.timeout:
                    pass
                except Exception as e:
                    print(f'Error in tcp server {e}')
                    self.statusBar().showMessage(f'Error in tcp server {e}')
                    break
            return server_address

    def run_icmp_server(self):
        try:
            icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            while self.running:
                try:
                    packet, addr = icmp_socket.recvfrom(1024)
                    icmp_header = packet[20:28]
                    icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence = struct.unpack('!BBHHH', icmp_header)
                    print(
                        f"ICMP Received from: {addr}, type: {icmp_type}, code: {icmp_code}, id: {icmp_id}, seq: {icmp_sequence}")

                    self.stats['icmp_recv'] += len(packet)

                    if icmp_type == 8:
                        icmp_type = 0
                        icmp_checksum = 0
                        new_icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id,
                                                      icmp_sequence)

                        icmp_checksum = self.calculate_checksum(new_icmp_header + packet[28:])
                        new_icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id,
                                                      icmp_sequence)

                        reply_packet = new_icmp_header + packet[28:]

                        icmp_socket.sendto(reply_packet, addr)
                        self.stats['icmp_sent'] += len(reply_packet)
                except socket.timeout:
                    pass
                except Exception as e:
                    print(f'Error in icmp server {e}')
                    self.statusBar().showMessage(f'Error in icmp server {e}')
                    break
            return icmp_socket.getsockname()
        except PermissionError:
            print("ICMP server requires root privileges.")
            self.statusBar().showMessage("ICMP server requires root privileges.")
            return None
        except Exception as e:
            print(f"Error in icmp server {e}")
            self.statusBar().showMessage(f'Error in icmp server {e}')
            return None
        finally:
            if 'icmp_socket' in locals() and icmp_socket:
                icmp_socket.close()

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

    def update_stats(self):
        text = f"Server IP: {self.server_address[0] if self.server_address else 'N/A'}:{self.server_address[1] if self.server_address and self.protocol_type.currentText() == 'TCP' else 'N/A'}\n"
        text += "-------\n"
        text += f"TCP Sent: {self.stats['tcp_sent']}\n"
        text += f"TCP Received: {self.stats['tcp_recv']}\n"
        text += "-------\n"
        text += f"ICMP Sent: {self.stats['icmp_sent']}\n"
        text += f"ICMP Received: {self.stats['icmp_recv']}\n"
        self.stats_text.setText(text)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ServerApp()
    window.show()
    sys.exit(app.exec_())