import socket
import threading
import time
from random import shuffle
import struct


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Server:
    def __init__(self, ip):
        self.ip = ip
        self.time_to_connect = 10
        self.all_teams = {}
        self.message_to_send_at_begin = ""

    def tcp_main_listener(self):
        bind_port = 8473

        condition = threading.Condition()

        tcp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        tcp_server_socket.bind((self.ip, bind_port))
        tcp_server_socket.settimeout(self.time_to_connect)
        tcp_server_socket.listen(1)
        start_time = time.time()
        while start_time + self.time_to_connect > time.time():
            try:
                connected_socket, address = tcp_server_socket.accept()
                thread_funk = threading.Thread(target=self.recv_name, args=(connected_socket, condition))
                thread_funk.start()
            except:
                if self.time_to_connect - time.time() + start_time > 0:
                    tcp_server_socket.settimeout(self.time_to_connect - time.time() + start_time)
                continue

        all_teams_lst = list(self.all_teams.keys())
        shuffle(all_teams_lst)
        team1 = all_teams_lst[:len(all_teams_lst) // 2]
        team2 = all_teams_lst[len(all_teams_lst) // 2:]
        self.message_to_send_at_begin = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n"
        for player_name in team1:
            self.message_to_send_at_begin += player_name + "\n"
        self.message_to_send_at_begin += "\nGroup 2:\n"
        for player_name in team2:
            self.message_to_send_at_begin += player_name + "\n"
        self.message_to_send_at_begin += "Start pressing keys on your keyboard as fast as you can!!"
        with condition:
            condition.notifyAll()

    def recv_name(self, connected_socket, cv):
        message = connected_socket.recv(2048)
        message = message.decode("utf-8")
        message = message[:-1] + str(len(self.all_teams))
        self.all_teams[message] = connected_socket
        with cv:
            cv.wait()
        connected_socket.send(str.encode(self.message_to_send_at_begin))

    def udp_server(self):
        bind_port = 13117
        print(f"{bcolors.HEADER}Server started, listening on IP address - " + self.ip)
        udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        # Enable broadcasting mode
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_server_socket.settimeout(self.time_to_connect)
        # udp_server_socket.bind((self.ip, bind_port))
        # bytesToSend1 = bytes(0xfeedbeef)
        magic_cookie = 0xfeedbeef
        message_type = 0x2
        server_tcp_port = 0x8473
        message = struct.pack('IBH', magic_cookie, message_type, server_tcp_port)

        count_time = 0
        while count_time < self.time_to_connect:
            udp_server_socket.sendto(message, (self.ip, bind_port))
            time.sleep(1)
            count_time += 1
            print(count_time)
        print("No more players for know")

    def main_server(self):
        client_handler = threading.Thread(target=self.udp_server)
        client_handler.start()
        client_handler2 = threading.Thread(target=self.tcp_main_listener)
        client_handler2.start()
        time.sleep(self.time_to_connect + 3)
        print("Players: ")
        for key in self.all_teams:
            print(key)


s1 = Server('127.0.0.1')
s1.main_server()
