# server.py
from scapy.all import *
from threading import Thread
from utils import log_event, visualize_tcp_handshake  # Импортируем функции из utils.py

def handle_client(pkt):
    src_ip = pkt[IP].src
    src_port = pkt[TCP].sport
    dst_port = pkt[TCP].dport

    if pkt[TCP].flags == 'S':  # SYN packet
        log_event('SYN', 'Client -> Server')
        print(f"Получен SYN пакет от {src_ip}:{src_port}")
        ip = IP(dst=src_ip)
        tcp = TCP(sport=dst_port, dport=src_port, flags='SA', seq=1000, ack=pkt[TCP].seq + 1)
        send(ip / tcp)
        log_event('SYN_ACK', 'Server -> Client')
        print(f"Отправлен SYN-ACK пакет клиенту {src_ip}:{src_port}")

    elif pkt[TCP].flags == 'A':  # ACK packet
        log_event('ACK', 'Client -> Server')
        print(f"Получен ACK пакет от {src_ip}:{src_port}")
        print("TCP-соединение установлено")

    elif pkt[TCP].flags & 0x01:  # FIN packet
        log_event('FIN', 'Client -> Server')
        print(f"Получен FIN пакет от {src_ip}:{src_port}")
        ip = IP(dst=src_ip)
        tcp = TCP(sport=dst_port, dport=src_port, flags='A', seq=pkt[TCP].ack, ack=pkt[TCP].seq + 1)
        send(ip / tcp)
        log_event('ACK', 'Server -> Client')
        print(f"Отправлен ACK пакет для FIN от клиента {src_ip}:{src_port}")
        tcp = TCP(sport=dst_port, dport=src_port, flags='FA', seq=pkt[TCP].ack, ack=pkt[TCP].seq + 1)
        send(ip / tcp)
        log_event('FIN_ACK', 'Server -> Client')
        print(f"Отправлен FIN пакет клиенту {src_ip}:{src_port}")

    elif pkt[TCP].flags == 'A':  # Final ACK packet
        log_event('ACK', 'Client -> Server')
        print(f"Получен окончательный ACK пакет от {src_ip}:{src_port}")
        print("Соединение закрыто")

def start_server(host='127.0.0.1', port=65432):
    def sniff_packets():
        sniff(filter=f"tcp and host {host} and port {port}", prn=handle_client, store=0)

    sniffer_thread = Thread(target=sniff_packets)
    sniffer_thread.daemon = True
    sniffer_thread.start()
    print(f"Сервер слушает на {host}:{port}")
    sniffer_thread.join()

    visualize_tcp_handshake()  # Визуализируем процесс после завершения handshake

if __name__ == "__main__":
    start_server()