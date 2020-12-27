import socket
import threading
import time


def tcp_server(bind_port):
    bind_ip = "127.0.0.1"

    tcp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    tcp_server_socket.bind((bind_ip, bind_port))
    tcp_server_socket.listen(1)
    tcp_server_socket.settimeout(15)

    message, address = tcp_server_socket.accept()

    client_ip = address[0]
    client_port = address[1]
    print(address)
    print("ip - " + client_ip)
    print("port - " + str(client_port))


def udp_server():
    bind_ip = "127.0.0.1"
    bind_port = 13117
    print("Server started, listening on IP address - " + bind_ip)

    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    # Enable broadcasting mode
    udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 10)
    udp_server_socket.settimeout(10)
    # udp_server_socket.bind((bind_ip, bind_port))
    # bytesToSend1 = bytes(0xfeedbeef)
    bytesToSend1 = bytes.fromhex('feedbeef9999')
    bytesToSend2 = bytes(0x2)
    bytesToSend3 = bytes(0x9999)

    count_time = 0
    clients_address = []
    while count_time < 10:
        udp_server_socket.sendto(bytesToSend1, (bind_ip, bind_port))
        time.sleep(1)
        count_time += 1
        print(bind_ip, bind_port)
        # thread_funk = threading.Thread(target=tcp_server)
        # thread_funk.start()
    # udp_server_socket.sendto(bytesToSend, ('<broadcast>', bind_port))
    # print(clientAddress, bytes.hex(message))
    # clients_address.append(clientAddress)
    # udp_server_socket.sendto(bytesToSend, clientAddress)


client_handler = threading.Thread(target=udp_server)
client_handler.start()

