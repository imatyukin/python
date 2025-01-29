from scapy.all import *
import threading


def handle_client(pkt):
    if pkt.haslayer(TCP):
        src_ip = pkt[IP].src
        src_port = pkt[TCP].sport
        dst_port = pkt[TCP].dport

        if pkt[TCP].flags == 'S':  # SYN packet
            print(f"Получен SYN пакет от {src_ip}:{src_port}")
            # Отправляем SYN-ACK
            ip = IP(dst=src_ip)
            tcp = TCP(sport=dst_port, dport=src_port, flags='SA', seq=1000, ack=pkt[TCP].seq + 1)
            send(ip / tcp)
            print(f"Отправлен SYN-ACK пакет клиенту {src_ip}:{src_port}")
        elif pkt[TCP].flags == 'A':  # ACK packet
            print(f"Получен ACK пакет от {src_ip}:{src_port}")
            print("TCP-соединение установлено")
        elif pkt[TCP].flags & 0x01:  # FIN packet
            print(f"Получен FIN пакет от {src_ip}:{src_port}")
            # Отправляем ACK для FIN
            ip = IP(dst=src_ip)
            tcp = TCP(sport=dst_port, dport=src_port, flags='A', seq=pkt[TCP].ack, ack=pkt[TCP].seq + 1)
            send(ip / tcp)
            print(f"Отправлен ACK пакет для FIN от клиента {src_ip}:{src_port}")
            # Отправляем FIN
            tcp = TCP(sport=dst_port, dport=src_port, flags='FA', seq=pkt[TCP].ack, ack=pkt[TCP].seq + 1)
            send(ip / tcp)
            print(f"Отправлен FIN пакет клиенту {src_ip}:{src_port}")
        elif pkt[TCP].flags == 'PA':  # PSH-ACK (data) packet
            print(f"Получен PSH-ACK пакет с данными от {src_ip}:{src_port}: {pkt[TCP].payload.load.decode()}")
            # Отправляем ACK для данных
            ip = IP(dst=src_ip)
            tcp = TCP(sport=dst_port, dport=src_port, flags='A', seq=pkt[TCP].ack,
                      ack=pkt[TCP].seq + len(pkt[TCP].payload.load))
            send(ip / tcp)
            print(f"Отправлен ACK пакет для данных от клиента {src_ip}:{src_port}")
        elif pkt[TCP].flags == 'A':  # Final ACK packet
            print(f"Получен окончательный ACK пакет от {src_ip}:{src_port}")
            print("Соединение закрыто")


def start_server(host='127.0.0.1', port=65432):
    def sniff_packets():
        sniff(filter=f"tcp and host {host} and port {port}", prn=handle_client, store=0)

    sniffer_thread = threading.Thread(target=sniff_packets)
    sniffer_thread.daemon = True
    sniffer_thread.start()

    print(f"Сервер слушает на {host}:{port}")
    sniffer_thread.join()


if __name__ == "__main__":
    start_server()