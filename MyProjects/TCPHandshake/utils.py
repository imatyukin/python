# utils.py
import matplotlib.pyplot as plt
import time

# Словарь для отображения типов пакетов
packet_types = {
    'SYN': 'SYN',
    'SYN_ACK': 'SYN-ACK',
    'ACK': 'ACK',
    'FIN': 'FIN',
    'FIN_ACK': 'FIN-ACK',
    'PSH_ACK': 'PSH-ACK'
}

# Глобальные переменные для графика
events = []
event_times = []

def log_event(event_type, direction='Client -> Server', timestamp=None):
    """
    Записывает событие для графического представления.
    :param event_type: Тип события (например, 'SYN', 'ACK')
    :param direction: Направление (например, 'Client -> Server' или 'Server -> Client')
    :param timestamp: Временная метка события
    """
    global events, event_times
    if timestamp is None:
        timestamp = time.time()
    events.append((event_type, direction))
    event_times.append(timestamp)

def visualize_tcp_handshake():
    """
    Визуализирует процесс TCP handshake с использованием matplotlib.
    """
    plt.figure(figsize=(10, 6))

    # Определяем координаты для клиентских и серверных событий
    client_x = [i for i, (event, direction) in enumerate(events) if 'Client' in direction]
    server_x = [i for i, (event, direction) in enumerate(events) if 'Server' in direction]

    client_y = [1] * len(client_x)
    server_y = [0] * len(server_x)

    # Рисуем точки для событий
    plt.scatter(client_x, client_y, color='blue', label='Client Event', zorder=5)
    plt.scatter(server_x, server_y, color='red', label='Server Event', zorder=5)

    # Рисуем стрелки для событий
    for i, (event, direction) in enumerate(events):
        if 'Client -> Server' in direction:
            plt.arrow(i, 1, 0, -0.8, head_width=0.1, head_length=0.1, fc='blue', ec='blue', length_includes_head=True)
        elif 'Server -> Client' in direction:
            plt.arrow(i, 0, 0, 0.8, head_width=0.1, head_length=0.1, fc='red', ec='red', length_includes_head=True)

    # Добавляем аннотации для событий
    for i, (event, _) in enumerate(events):
        plt.text(i, 1.2 if 'Client' in events[i][1] else -0.2, packet_types[event], ha='center', fontsize=10)

    # Настройка осей и легенды
    plt.yticks([0, 1], ['Server', 'Client'])
    plt.xlabel('События по времени')
    plt.title('Процесс TCP Handshake')
    plt.legend()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Показываем график
    plt.show()