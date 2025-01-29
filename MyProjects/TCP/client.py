from scapy.all import *


def start_client(host='127.0.0.1', port=65432):
    print(f"Попытка подключения к {host}:{port}")

    # Отправляем SYN пакет
    ip = IP(dst=host)
    tcp_syn = TCP(sport=RandShort(), dport=port, flags='S', seq=1000)
    syn_ack_pkt = sr1(ip / tcp_syn)
    print(f"Отправлен SYN пакет на {host}:{port}")

    if syn_ack_pkt and syn_ack_pkt.haslayer(TCP) and syn_ack_pkt[TCP].flags & 0x12:  # SYN-ACK
        print(f"Получен SYN-ACK пакет от {host}:{port}")

        # Отправляем ACK
        my_ack = syn_ack_pkt[TCP].seq + 1
        tcp_ack = TCP(sport=syn_ack_pkt[TCP].dport, dport=port, flags='A', seq=syn_ack_pkt[TCP].ack, ack=my_ack)
        send(ip / tcp_ack)
        print(f"Отправлен ACK пакет на {host}:{port}")
        print("TCP-соединение установлено")
    else:
        print("Не удалось установить соединение")


if __name__ == "__main__":
    start_client()