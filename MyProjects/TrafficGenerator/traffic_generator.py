import yaml
import socket
import threading
import time
import os
import math
from ipaddress import IPv4Address, ip_address


class TrafficGenerator:
    def __init__(self, config_path):
        with open(config_path, encoding='utf-8') as f:  # Явно указываем кодировку
            self.config = yaml.safe_load(f)

        # Установка значений по умолчанию
        defaults = {
            'source_address': '0.0.0.0',
            'source_port': 0,
            'destination_port': 12345,
            'packet_size': 512,
            'threads': 1,
            'duration': 0,
            'target_speed_pps': None,
            'target_speed_mbps': None,
            'interval': None,
            'qos': {
                'dscp': None,
                'ip_precedence': None,
                'ecn': None
            }
        }

        # Рекурсивная установка значений по умолчанию
        for key, value in defaults.items():
            if isinstance(value, dict):
                self.config.setdefault(key, {})
                for sub_key, sub_value in value.items():
                    self.config[key].setdefault(sub_key, sub_value)
            else:
                self.config.setdefault(key, value)

        self.validate_config()
        self.calculate_parameters()
        self.running = False
        self.stats = {'sent': 0, 'errors': 0, 'bytes': 0}
        self.lock = threading.Lock()
        self.start_time = time.time()

    def validate_config(self):
        # Проверка типа трафика
        traffic_types = ['unicast', 'broadcast', 'multicast']
        if self.config['traffic_type'] not in traffic_types:
            raise ValueError(f"Invalid traffic type: {self.config['traffic_type']}")

        # Валидация IP-адресов
        try:
            socket.inet_aton(self.config['source_address'])
        except socket.error:
            raise ValueError("Invalid source IP address")

        if self.config['traffic_type'] == 'multicast':
            if 'group_address' not in self.config:
                raise ValueError("Missing group_address for multicast")
            if not IPv4Address(self.config['group_address']).is_multicast:
                raise ValueError("Invalid multicast group address")
        else:
            try:
                ip_address(self.config['destination_address'])
            except ValueError:
                raise ValueError("Invalid destination IP address")

        # Проверка портов
        if not (0 <= self.config['source_port'] <= 65535):
            raise ValueError("Invalid source port")
        if not (0 < self.config['destination_port'] <= 65535):
            raise ValueError("Invalid destination port")

        # Проверка параметров скорости
        speed_params = sum([
            self.config['target_speed_pps'] is not None,
            self.config['target_speed_mbps'] is not None,
            self.config['interval'] is not None
        ])

        if speed_params > 1:
            raise ValueError("Use only one of: target_speed_pps, target_speed_mbps, interval")

        # Валидация QoS-параметров
        qos = self.config['qos']
        if qos['dscp'] is not None and not (0 <= qos['dscp'] <= 63):
            raise ValueError("DSCP value must be between 0 and 63")

        if qos['ip_precedence'] is not None and not (0 <= qos['ip_precedence'] <= 7):
            raise ValueError("IP Precedence must be between 0 and 7")

        if qos['ecn'] is not None and not (0 <= qos['ecn'] <= 3):
            raise ValueError("ECN must be between 0 and 3")

        if qos['dscp'] is not None and qos['ip_precedence'] is not None:
            raise ValueError("Use either DSCP or IP Precedence, not both")

    def calculate_parameters(self):
        if self.config['target_speed_pps']:
            interval = 1.0 / self.config['target_speed_pps']
            self.config['interval'] = interval / self.config['threads']

        elif self.config['target_speed_mbps']:
            bits_per_packet = (self.config['packet_size'] + 42) * 8  # Ethernet overhead
            packets_per_second = (self.config['target_speed_mbps'] * 1e6) / bits_per_packet
            interval = 1.0 / packets_per_second
            self.config['interval'] = interval / self.config['threads']

        if self.config['interval'] is not None:
            self.config['interval'] = max(self.config['interval'], 0.0001)
        else:
            self.config['interval'] = 0

    def create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Настройка QoS
        qos = self.config['qos']
        tos = 0

        if qos['dscp'] is not None:
            tos |= (qos['dscp'] << 2)
        elif qos['ip_precedence'] is not None:
            tos |= (qos['ip_precedence'] << 5)

        if qos['ecn'] is not None:
            tos |= qos['ecn']

        if tos > 0:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, tos)

        # Настройки типа трафика
        if self.config['traffic_type'] == 'broadcast':
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        elif self.config['traffic_type'] == 'multicast':
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        try:
            sock.bind((self.config['source_address'], self.config['source_port']))
        except OSError as e:
            raise RuntimeError(f"Failed to bind socket: {e}")

        return sock

    def get_destination(self):
        if self.config['traffic_type'] == 'multicast':
            return (self.config['group_address'], self.config['destination_port'])
        return (self.config['destination_address'], self.config['destination_port'])

    def sender_loop(self):
        try:
            sock = self.create_socket()
        except Exception as e:
            with self.lock:
                self.stats['errors'] += 1
            print(f"\nThread error: {e}")
            return

        dest = self.get_destination()
        data = os.urandom(self.config['packet_size'])
        bytes_per_packet = len(data)
        end_time = time.time() + self.config['duration'] if self.config['duration'] > 0 else None
        next_send = time.time()

        while self.running and (end_time is None or time.time() < end_time):
            try:
                if self.config['interval'] > 0:
                    next_send += self.config['interval']
                    sleep_time = next_send - time.time()
                    if sleep_time > 0:
                        time.sleep(sleep_time)

                sock.sendto(data, dest)
                with self.lock:
                    self.stats['sent'] += 1
                    self.stats['bytes'] += bytes_per_packet
            except Exception as e:
                with self.lock:
                    self.stats['errors'] += 1
                print(f"\nSend error: {e}")

        sock.close()

    def start(self):
        self.running = True
        threads = []

        for _ in range(self.config['threads']):
            t = threading.Thread(target=self.sender_loop)
            threads.append(t)
            t.start()

        try:
            prev_stats = {'sent': 0, 'bytes': 0}
            while any(t.is_alive() for t in threads):
                time.sleep(1)
                elapsed = time.time() - self.start_time

                with self.lock:
                    current_sent = self.stats['sent']
                    current_bytes = self.stats['bytes']
                    delta_sent = current_sent - prev_stats['sent']
                    delta_bytes = current_bytes - prev_stats['bytes']
                    prev_stats = {'sent': current_sent, 'bytes': current_bytes}

                pps = delta_sent
                mbps = (delta_bytes * 8) / 1e6
                total_mbps = (current_bytes * 8) / 1e6 / elapsed if elapsed > 0 else 0

                stats_str = (
                    f"\r[+] PPS: {pps:.1f}/s | "
                    f"Speed: {mbps:.2f} Mbps (current) / {total_mbps:.2f} Mbps (avg) | "
                    f"Total: {current_sent} packets | "
                    f"Errors: {self.stats['errors']}"
                )
                print(stats_str.ljust(120), end="")

        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self.running = False
            for t in threads:
                t.join()

        total_time = time.time() - self.start_time
        print("\n\n=== Traffic generation summary ===")
        print(f"Duration:           {total_time:.2f} seconds")
        print(f"Total packets sent: {self.stats['sent']}")
        print(f"Total data sent:    {(self.stats['bytes'] / 1e6):.2f} MB")
        print(f"Average speed:      {(self.stats['bytes'] * 8 / 1e6 / total_time):.2f} Mbps")
        print(f"Errors occurred:    {self.stats['errors']}")


if __name__ == "__main__":
    try:
        generator = TrafficGenerator("config.yaml")
        generator.start()
    except Exception as e:
        print(f"Fatal error: {e}")