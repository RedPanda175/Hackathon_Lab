from socket import *
import struct


class Client:
    def __init__(self, ip):
        self.ip = ip

    def udp_part(self):
        server_address_port = (self.ip, 13117)
        buffer_size = 2048
        print("Client started, listening for offer requests...")

        udp_client_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)  # UDP
        udp_client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        udp_client_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        udp_client_socket.bind(server_address_port)
        receive_message, server_address = udp_client_socket.recvfrom(buffer_size)
        # udp_client_socket.close()
        print("Received offer from {} attempting to connect...".format(server_address[0]))

        receive_message = struct.unpack('IBH', receive_message)
        magic_cookie = receive_message[0]
        # message_type = receive_message[1]
        tcp_port = 8473

        if magic_cookie == 4276993775:
            self.tcp_part(tcp_port)

    def tcp_part(self, tcp_port):
        server_address = (self.ip, int(tcp_port))
        tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        tcp_client_socket.connect(server_address)
        tcp_client_socket.send(str.encode("team rocket\n"))
        # the problem is that we are trying to connect to the master TCP server port, and not to the address we get from this tcp server.
        # the process should be: wait for UDP -> rcv offer -> connect to master TCP -> rcv address to connect -> connect to address
        # -> send msg to address
        message = tcp_client_socket.recv(1048)
        message = message.decode("utf-8")
        print(message)


c1 = Client("127.0.0.1")
c1.udp_part()
