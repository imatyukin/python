import ipaddress

def validate_ip_address(ip_str):
    """
    Валидация IP-адреса.

    :param ip_str: Строка с IP-адресом.
    :return: Валидный IP-адрес.
    :raises ValueError: Если IP-адрес невалидный.
    """
    try:
        ipaddress.ip_address(ip_str)
        return ip_str
    except ValueError:
        raise ValueError(f"Invalid IP address: {ip_str}")

def validate_port(port_str):
    """
    Валидация порта.

    :param port_str: Строка с номером порта.
    :return: Валидный номер порта (0-65535).
    :raises ValueError: Если порт невалидный.
    """
    if port_str is None or not isinstance(port_str, str) or port_str == "":
        return 0
    try:
        port = int(port_str)
        if 0 <= port <= 65535:
            return port
        else:
            raise ValueError(f"Invalid port number: {port_str}. Must be between 0 and 65535")
    except ValueError:
        raise ValueError(f"Invalid port number: {port_str}. Must be an integer.")

def validate_packet_size(packet_size_str):
    """
    Валидация размера пакета.

    :param packet_size_str: Строка с размером пакета.
    :return: Валидный размер пакета (1-65507).
    :raises ValueError: Если размер пакета невалидный.
    """
    if packet_size_str is None or not isinstance(packet_size_str, str):
        raise ValueError("Packet size must be a string")
    try:
        packet_size = int(packet_size_str)
        if 1 <= packet_size <= 65507:
            return packet_size
        else:
            raise ValueError(f"Invalid packet size: {packet_size_str}. Must be between 1 and 65507")
    except ValueError:
        raise ValueError(f"Invalid packet size: {packet_size_str}. Must be an integer.")

def validate_threads(threads_str):
    """
    Валидация количества потоков.

    :param threads_str: Строка с количеством потоков.
    :return: Валидное количество потоков (1-100).
    :raises ValueError: Если количество потоков невалидное.
    """
    try:
        threads = int(threads_str)
        if 1 <= threads <= 100:
            return threads
        else:
            raise ValueError(f"Invalid thread count: {threads_str}. Must be between 1 and 100")
    except ValueError:
        raise ValueError(f"Invalid thread count: {threads_str}. Must be an integer.")

def validate_range(value, min_val, max_val):
    """
    Валидация значения в диапазоне.

    :param value: Значение для проверки.
    :param min_val: Минимальное допустимое значение.
    :param max_val: Максимальное допустимое значение.
    :return: Валидное значение.
    :raises ValueError: Если значение невалидное.
    """
    if not value:
        return None
    if not isinstance(value, int):
        raise ValueError(f"Invalid value: {value}. Must be an integer")
    val = int(value)
    if min_val <= val <= max_val:
        return val
    else:
        raise ValueError(f"Invalid value: {val}. Must be between {min_val} and {max_val}")

def calculate_checksum(data):
    """
    Расчет контрольной суммы для пакетов.

    :param data: Данные для расчета контрольной суммы.
    :return: Контрольная сумма.
    """
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