from socket import *
import time
import struct


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

    def udp_part(self, counter):
        server_address_port = (self.ip, 13217)
        print("Client started, listening for offer requests...")

        # init the UDP socket
        udp_client_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        udp_client_socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        udp_client_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        udp_client_socket.settimeout(10)

        # wait for some connection
        to_continue = True
        try:
            udp_client_socket.bind(server_address_port)
            receive_message, server_address = udp_client_socket.recvfrom(self.buffer_size)
            print("Received offer from {} attempting to connect...".format(server_address[0]))
            tcp_ip = server_address[0]
            receive_message = struct.unpack('IBH', receive_message)
        except:
            time.sleep(0.5)
            if counter > 5:
                time.sleep(5)
            self.udp_part(counter + 1)
            to_continue = False

        if to_continue:
            # organize recv data
            magic_cookie = hex(receive_message[0])
            tcp_port = hex(receive_message[2])
            tcp_port = int(tcp_port, 16)
            if magic_cookie == '0xfeedbeef':
                self.tcp_part(tcp_port, tcp_ip, counter)

    def tcp_part(self, tcp_port, tcp_ip, counter):
        # init the TCP socket
        server_address = (tcp_ip, int(tcp_port))
        tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        try:
            to_continue = True
            tcp_client_socket.connect(server_address)
        except:
            tcp_client_socket.close()
            time.sleep(0.5)
            if counter > 5:
                time.sleep(5)
            self.udp_part(counter + 1)
            to_continue = False

        if to_continue:
            # send team name
            tcp_client_socket.send(str.encode("FSM\n"))
            message = ""
            try:
                tcp_client_socket.settimeout(10)
                message = tcp_client_socket.recv(self.buffer_size)
            except:
                tcp_client_socket.close()
                time.sleep(0.5)
                if counter > 5:
                    time.sleep(5)
                self.udp_part(counter + 1)
                to_continue = False

            if to_continue:
                message = message.decode("utf-8")
                print(message)

                # start the game !!!
                future = time.time() + 10
                while future > time.time():
                    try:
                        tcp_client_socket.send(str.encode(getch()))
                    except:
                        continue

                # recv end message
                try:
                    tcp_client_socket.settimeout(10)
                    message = tcp_client_socket.recv(self.buffer_size)
                    message = message.decode("utf-8")
                    print(message)
                except:
                    time.sleep(0.5)
                self.udp_part(0)


eth1 = "172.1.0.24"
eth2 = "172.99.0.24"
broadcast_ip = "<broadcast>"
c1 = Client("")
c1.udp_part(0)
