import socket
import threading
import time


class TCPServer:
    def __init__(self, host="0.0.0.0", port=9999):
        self.host = host
        self.port = port
        self.running = True
        self.total_bytes_received = 0
        self.total_packets_received = 0
        self.start_time = time.time()

    def handle_client(self, client_socket, address):
        print(f"[+] Connection from {address}")

        while self.running:
            try:
                data = client_socket.recv(4096)  # Принимаем до 4 KB за раз
                if not data:
                    break  # Клиент закрыл соединение
                self.total_bytes_received += len(data)
                self.total_packets_received += 1
            except ConnectionResetError:
                print(f"[-] Connection reset by {address}")
                break
            except Exception as e:
                print(f"[-] Error: {e}")
                break

        client_socket.close()
        print(f"[-] Connection closed: {address}")

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)  # Очередь из 5 соединений
        print(f"[*] Listening on {self.host}:{self.port}")

        # Поток для вывода статистики
        threading.Thread(target=self.print_stats, daemon=True).start()

        try:
            while self.running:
                client_socket, address = server.accept()
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address), daemon=True)
                client_handler.start()
        except KeyboardInterrupt:
            print("\n[*] Shutting down server...")
        finally:
            self.running = False
            server.close()

    def print_stats(self):
        """Выводит статистику каждые 5 секунд."""
        while self.running:
            elapsed_time = time.time() - self.start_time
            mbps = (self.total_bytes_received * 8) / (elapsed_time * 1_000_000) if elapsed_time > 0 else 0
            print(
                f"[STATS] Packets: {self.total_packets_received}, Bytes: {self.total_bytes_received}, Speed: {mbps:.2f} Mbps")
            time.sleep(5)


if __name__ == "__main__":
    server = TCPServer(port=9999)  # Указываем порт, который должен совпадать с TrafficGenerator
    server.start()
