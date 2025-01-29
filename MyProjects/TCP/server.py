from scapy.all import *
import threading

def handle_client(pkt):
    if pkt.haslayer(TCP):
        if pkt[TCP].flags == 'S':  # SYN packet
            print(f"Получен SYN пакет от {pkt[IP].src}:{pkt[TCP].sport}")
            # Отправляем SYN-ACK
            ip = IP(dst=pkt[IP].src)
            tcp = TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, flags='SA', seq=1000, ack=pkt[TCP].seq + 1)
            send(ip/tcp)
            print(f"Отправлен SYN-ACK пакет клиенту {pkt[IP].src}:{pkt[TCP].sport}")
        elif pkt[TCP].flags == 'A':  # ACK packet
            print(f"Получен ACK пакет от {pkt[IP].src}:{pkt[TCP].sport}")
            print("TCP-соединение установлено")

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