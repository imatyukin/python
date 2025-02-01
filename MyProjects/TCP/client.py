# client.py
from scapy.layers.inet import IP, TCP, RandShort
from scapy.packet import Raw
from scapy.sendrecv import sr1, send
from utils import log_event, visualize_tcp_handshake  # Импортируем функции из utils.py

def start_client(host='127.0.0.1', port=65432):
    print(f"Попытка подключения к {host}:{port}")
    ip = IP(dst=host)
    tcp_syn = TCP(sport=RandShort(), dport=port, flags='S', seq=1000)

    # Отправляем SYN пакет
    log_event('SYN', 'Client -> Server')
    syn_ack_pkt = sr1(ip / tcp_syn, timeout=2)
    if syn_ack_pkt and syn_ack_pkt.haslayer(TCP) and syn_ack_pkt[TCP].flags & 0x12:  # SYN-ACK
        log_event('SYN_ACK', 'Server -> Client')
        print(f"Получен SYN-ACK пакет от {host}:{port}")

        # Отправляем ACK
        my_ack = syn_ack_pkt[TCP].seq + 1
        tcp_ack = TCP(sport=syn_ack_pkt[TCP].dport, dport=port, flags='A', seq=syn_ack_pkt[TCP].ack, ack=my_ack)
        send(ip / tcp_ack)
        log_event('ACK', 'Client -> Server')
        print(f"Отправлен ACK пакет на {host}:{port}")
        print("TCP-соединение установлено")

        # Отправляем данные
        message = "Привет, сервер!"
        tcp_data = TCP(sport=syn_ack_pkt[TCP].dport, dport=port, flags='PA', seq=syn_ack_pkt[TCP].ack, ack=my_ack)
        send(ip / tcp_data / Raw(load=message))
        log_event('PSH_ACK', 'Client -> Server')
        print(f"Отправлен PSH-ACK пакет с данными на {host}:{port}: {message}")

        # Получаем ACK для данных
        ack_pkt = sr1(
            ip / TCP(sport=syn_ack_pkt[TCP].dport, dport=port, flags='A', seq=tcp_data.seq + len(message), ack=my_ack),
            timeout=2
        )
        if ack_pkt and ack_pkt.haslayer(TCP) and ack_pkt[TCP].flags & 0x10:  # ACK
            log_event('ACK', 'Server -> Client')
            print(f"Получен ACK пакет для данных от {host}:{port}")

        # Отправляем FIN пакет
        tcp_fin = TCP(sport=syn_ack_pkt[TCP].dport, dport=port, flags='F', seq=ack_pkt[TCP].ack, ack=my_ack)
        fin_ack_pkt = sr1(ip / tcp_fin, timeout=2)
        log_event('FIN', 'Client -> Server')
        print(f"Отправлен FIN пакет на {host}:{port}")

        if fin_ack_pkt and fin_ack_pkt.haslayer(TCP) and fin_ack_pkt[TCP].flags & 0x11:  # FIN-ACK
            log_event('FIN_ACK', 'Server -> Client')
            print(f"Получен FIN-ACK пакет от {host}:{port}")

            # Отправляем ACK для FIN-ACK
            final_ack = TCP(sport=syn_ack_pkt[TCP].dport, dport=port, flags='A', seq=fin_ack_pkt[TCP].ack,
                            ack=fin_ack_pkt[TCP].seq + 1)
            send(ip / final_ack)
            log_event('ACK', 'Client -> Server')
            print(f"Отправлен окончательный ACK пакет на {host}:{port}")
            print("Соединение закрыто")

    visualize_tcp_handshake()  # Визуализируем процесс после завершения handshake

if __name__ == "__main__":
    start_client()