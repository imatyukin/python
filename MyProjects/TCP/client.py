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

        # Отправляем данные
        message = "Привет, сервер!"
        tcp_data = TCP(sport=syn_ack_pkt[TCP].dport, dport=port, flags='PA', seq=syn_ack_pkt[TCP].ack, ack=my_ack)
        send(ip / tcp_data / Raw(load=message))
        print(f"Отправлен PSH-ACK пакет с данными на {host}:{port}: {message}")

        # Получаем ACK для данных
        ack_pkt = sr1(
            ip / TCP(sport=syn_ack_pkt[TCP].dport, dport=port, flags='A', seq=tcp_data.seq + len(message), ack=my_ack))
        print(f"Получен ACK пакет для данных от {host}:{port}")

        # Отправляем FIN пакет
        tcp_fin = TCP(sport=syn_ack_pkt[TCP].dport, dport=port, flags='F', seq=ack_pkt[TCP].ack, ack=my_ack)
        fin_ack_pkt = sr1(ip / tcp_fin)
        print(f"Отправлен FIN пакет на {host}:{port}")

        if fin_ack_pkt and fin_ack_pkt.haslayer(TCP) and fin_ack_pkt[TCP].flags & 0x11:  # FIN-ACK
            print(f"Получен FIN-ACK пакет от {host}:{port}")

            # Отправляем ACK для FIN-ACK
            final_ack = TCP(sport=syn_ack_pkt[TCP].dport, dport=port, flags='A', seq=fin_ack_pkt[TCP].ack,
                            ack=fin_ack_pkt[TCP].seq + 1)
            send(ip / final_ack)
            print(f"Отправлен окончательный ACK пакет на {host}:{port}")
            print("Соединение закрыто")


if __name__ == "__main__":
    start_client()