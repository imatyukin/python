import socket
import time
import os
import struct
import threading
from utils import calculate_checksum  # Импортируем функцию для расчета контрольной суммы

class TrafficGenerator:
    def __init__(self, config, stats, protocol, app_instance):
        """
        Инициализация генератора трафика.

        :param config: Конфигурация генератора (словарь с настройками).
        :param stats: Словарь для хранения статистики.
        :param protocol: Протокол (UDP или ICMP).
        :param app_instance: Экземпляр приложения для обновления UI.
        """
        self.config = config
        self.stats = stats
        self.running = False
        self.interval_time = 0
        self.real_source_address = None
        self.real_source_port = None
        self.real_destination_address = None
        self.real_destination_port = None
        self.protocol = protocol
        self.lock = threading.Lock()  # Блокировка для потокобезопасности
        self.threads = []  # Список потоков
        self.last_send_time = 0
        self.app_instance = app_instance  # Ссылка на главное окно приложения
        self.sockets = []  # Список сокетов для каждого потока

    def run(self):
        """
        Основной метод запуска генератора трафика.
        """
        self.running = True
        start_time = time.time()

        # Если режим скорости - интервал, вычисляем время ожидания
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

        # Обновляем реальные значения в UI перед запуском потоков
        if self.sockets:
            self.real_source_address, self.real_source_port = self.sockets[0].getsockname()
            self.app_instance.update_real_values(
                self.real_source_address, self.real_source_port,
                self.real_destination_address, self.real_destination_port
            )

        # Запускаем потоки для отправки пакетов
        for i in range(self.config['threads']):
            thread = threading.Thread(target=self.send_packet, args=(self.sockets[i],), daemon=True)
            self.threads.append(thread)
            thread.start()

        try:
            # Основной цикл генератора
            while self.running:
                current_time = time.time() - start_time
                pps = 0
                mbps = 0

                # Рассчитываем статистику
                if current_time > 0:
                    with self.lock:
                        pps = self.stats['sent'] / current_time
                        mbps = (self.stats['bytes'] / 1000000.0) / current_time

                # Обновляем статистику в UI
                self.stats_update(current_time, pps, mbps)
                time.sleep(0.1)  # Небольшая задержка для снижения нагрузки на CPU
        except Exception as e:
            print(f"Error in generator: {e}")
        finally:
            print("Generator stopped.")
            # Закрываем все сокеты
            for sock in self.sockets:
                if sock:
                    sock.close()

    def stats_update(self, current_time, pps, mbps):
        """
        Обновление статистики в UI.

        :param current_time: Текущее время работы генератора.
        :param pps: Пакетов в секунду.
        :param mbps: Мегабит в секунду.
        """
        if isinstance(current_time, float) and isinstance(pps, (int, float)) and isinstance(mbps, (int, float)):
            if current_time >= 0:
                self.app_instance.history['time'].append(current_time)
                self.app_instance.history['pps'].append(pps)
                self.app_instance.history['mbps'].append(mbps)

    def create_and_bind_socket(self):
        """
        Создание и привязка сокета в зависимости от протокола и типа трафика.

        :return: Сокет или None в случае ошибки.
        """
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
        """
        Отправка пакетов в цикле.

        :param sock: Сокет для отправки пакетов.
        """
        try:
            message = None
            if self.protocol == "UDP":
                message = os.urandom(self.config['packet_size'])  # Генерация случайных данных
            elif self.protocol == "ICMP":
                message = self.create_icmp_packet(self.config['packet_size'])  # Создание ICMP пакета

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

            # Основной цикл отправки пакетов
            while self.running:
                if self.protocol == "UDP":
                    sock.sendto(message, (self.real_destination_address, self.config['destination_port']))
                elif self.protocol == "ICMP":
                    sock.sendto(message, (self.real_destination_address, 0))

                # Обновляем статистику
                with self.lock:
                    self.stats['sent'] += 1
                    self.stats['bytes'] += len(message)

                # Задержка для соблюдения скорости
                if time_wait > 0:
                    time.sleep(time_wait)

                start_time = time.time()
        except Exception as e:
            with self.lock:
                self.stats['errors'] += 1
            print(f"Error sending packet: {e}")
            self.app_instance.statusBar.showMessage(f"Error sending packet: {e}")

    def create_icmp_packet(self, packet_size):
        """
        Создание ICMP пакета.

        :param packet_size: Размер пакета.
        :return: Байты ICMP пакета.
        """
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

        # Добавляем контрольную сумму для IP-заголовка
        ip_checksum = calculate_checksum(ip_header)
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
        icmp_checksum = calculate_checksum(header + data)
        header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence)

        return ip_header + header + data