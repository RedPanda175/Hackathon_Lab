from socket import *
import time
import struct


def getch():
    import termios
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch()


class Client:
    def __init__(self, ip):
        self.ip = ip

    def udp_part(self):
        server_address_port = (self.ip, 13124)
        buffer_size = 1024
        print("Client started, listening for offer requests...")

        udp_client_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)  # UDP
        udp_client_socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        udp_client_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        udp_client_socket.bind(server_address_port)
        receive_message, server_address = udp_client_socket.recvfrom(buffer_size)
        # udp_client_socket.close()
        print("Received offer from {} attempting to connect...".format(server_address[0]))

        tcp_ip = server_address[0]
        print(tcp_ip)
        receive_message = struct.unpack('IBH', receive_message)
        magic_cookie = hex(receive_message[0])
        # message_type = hex(receive_message[1])
        tcp_port = hex(receive_message[2])
        tcp_port = int(tcp_port, 16)
        print(magic_cookie)
        print(tcp_port)

        if magic_cookie == '0xfeedbeef':
            self.tcp_part(tcp_port, tcp_ip)

    def tcp_part(self, tcp_port, tcp_ip):
        print("connect")
        server_address = (tcp_ip, int(tcp_port))
        tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        print(server_address)
        tcp_client_socket.connect(server_address)
        tcp_client_socket.send(str.encode("team rocket\n"))
        message = tcp_client_socket.recv(1024)
        message = message.decode("utf-8")
        print(message)
        future = time.time() + 10
        while future > time.time():
            tcp_client_socket.send(str.encode(getch()))

        message = tcp_client_socket.recv(1024)
        message = message.decode("utf-8")
        print(message)
        self.udp_part()


c1 = Client("<broadcast>")
c1.udp_part()
