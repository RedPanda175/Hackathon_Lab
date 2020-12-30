from socket import *
import time
import struct
from server import Colors


# funk from the web to get chat from user
def getch():
    import termios
    import sys
    import tty

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
        self.buffer_size = 1024

    def udp_part(self):
        server_address_port = (self.ip, 13117)
        print(Colors.CBLUE + "Client started, listening for offer requests..." + Colors.CEND)

        # init the UDP socket
        udp_client_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        udp_client_socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        udp_client_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        did_bind = False

        # wait for some connection
        while not did_bind:
            try:
                time.sleep(0.1)
                udp_client_socket.bind(server_address_port)
                did_bind = True
            except:
                print("error")
        receive_message, server_address = udp_client_socket.recvfrom(self.buffer_size)
        print(
            Colors.CYELLOW + "Received offer from {} attempting to connect...".format(server_address[0] + Colors.CEND))

        # organize recv data
        tcp_ip = server_address[0]
        receive_message = struct.unpack('IBH', receive_message)
        magic_cookie = hex(receive_message[0])
        tcp_port = hex(receive_message[2])
        tcp_port = int(tcp_port, 16)

        if magic_cookie == '0xfeedbeef':
            self.tcp_part(tcp_port, tcp_ip)

    def tcp_part(self, tcp_port, tcp_ip):
        # init the TCP socket
        server_address = (tcp_ip, int(tcp_port))
        tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        did_connect = False
        # wait for some connection
        while not did_connect:
            try:
                time.sleep(0.1)
                tcp_client_socket.connect(server_address)
                did_connect = True
            except:
                continue
        # send team name
        tcp_client_socket.send(str.encode("FSM\n"))
        message = tcp_client_socket.recv(self.buffer_size)
        message = message.decode("utf-8")
        print(message)

        # start the game !!!
        future = time.time() + 10
        while future > time.time():
            tcp_client_socket.send(str.encode(getch()))

        # recv end message
        message = tcp_client_socket.recv(self.buffer_size)
        message = message.decode("utf-8")
        print(message)
        self.udp_part()


c1 = Client("<broadcast>")
c1.udp_part()
