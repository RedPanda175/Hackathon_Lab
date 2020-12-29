import socket
import threading
import time
from random import shuffle
import struct
import operator


class Server:
    def __init__(self, ip):
        self.ip = ip
        self.time_to_connect = 20
        self.all_teams = {}
        self.message_to_send_at_begin = ""
        self.team1 = []
        self.team2 = []
        self.team1_points = 0
        self.team2_points = 0
        self.end_message = "Game over!\nGroup 1 typed in {} characters. Group 2 typed in {} characters."
        self.end_message_part2 = "\nGroup {} wins!\n Congratulations to the winners:\n==\n=="
        self.end_message_draw = "\nIt's a draw!\nCongratulations to both teams!!!"

    def tcp_main_listener(self):
        bind_port = 8473

        condition = threading.Condition()

        tcp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        tcp_server_socket.bind((self.ip, bind_port))
        tcp_server_socket.settimeout(self.time_to_connect)
        tcp_server_socket.listen(17)
        start_time = time.time()
        while start_time + self.time_to_connect > time.time():
            try:
                connected_socket, address = tcp_server_socket.accept()
                thread_funk = threading.Thread(target=self.handle_client, args=(connected_socket, condition))
                thread_funk.start()
            except:
                if self.time_to_connect - time.time() + start_time > 0:
                    tcp_server_socket.settimeout(self.time_to_connect - time.time() + start_time)
                continue

        all_teams_lst = list(self.all_teams.keys())
        shuffle(all_teams_lst)
        self.team1 = all_teams_lst[:len(all_teams_lst) // 2]
        self.team2 = all_teams_lst[len(all_teams_lst) // 2:]
        self.message_to_send_at_begin = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n"
        for player_name in self.team1:
            self.message_to_send_at_begin += player_name + "\n"
        self.message_to_send_at_begin += "\nGroup 2:\n"
        for player_name in self.team2:
            self.message_to_send_at_begin += player_name + "\n"
        self.message_to_send_at_begin += "Start pressing keys on your keyboard as fast as you can!!"

        with condition:
            condition.notifyAll()

        time.sleep(11)
        self.who_won()
        winner_team = None
        self.end_message = self.end_message.format(self.team1_points, self.team2_points)
        if self.team1_points == self.team2_points:
            self.end_message += self.end_message_draw
        elif self.team1_points > self.team2_points:
            self.end_message += self.end_message_part2.format(1)
            winner_team = self.team1
        else:
            self.end_message += self.end_message_part2.format(2)
            winner_team = self.team2
        if winner_team is not None:
            for name in winner_team:
                self.end_message += "\n" + name

        print(self.end_message)
        print(1, self.team1_points)
        print(2, self.team2_points)
        with condition:
            condition.notifyAll()

    def handle_client(self, connected_socket, cv):
        message = connected_socket.recv(2048)
        message = message.decode("utf-8")
        message = message[:-1] + str(len(self.all_teams))
        self.all_teams[message] = {}
        print(message)
        with cv:
            cv.wait()
        chars = []
        print("start to recv")
        connected_socket.send(str.encode(self.message_to_send_at_begin))
        connected_socket.settimeout(10)
        start_time = time.time()
        future = time.time() + 10
        while future > time.time():
            try:
                ch = connected_socket.recv(1024)
            except:
                continue
            chars.append(list(ch.decode("utf-8")))
            print("recv from", message, ch.decode("utf-8"))
            time_pass = time.time() - start_time
            print(time_pass, 10 - time_pass)
            connected_socket.settimeout(10 - time_pass)
        print("finish recv")
        dict_chars = {}
        for lst in chars:
            for c in lst:
                if c in dict_chars:
                    dict_chars[c] += 1
                else:
                    dict_chars[c] = 1
        self.all_teams[message] = dict_chars
        print("put in main dict - ", dict_chars)
        max_char = max(dict_chars.items(), key=operator.itemgetter(1))[0]
        with cv:
            cv.wait()
        to_send = self.end_message + "\nYour most common char is - " + max_char
        connected_socket.send(str.encode(to_send))

    def who_won(self):
        print("start calculate")
        for team in self.team1:
            for c in self.all_teams[team]:
                self.team1_points += self.all_teams[team][c]
        for team in self.team2:
            for c in self.all_teams[team]:
                self.team2_points += self.all_teams[team][c]

    def udp_server(self):
        bind_port = 13117
        print("Server started, listening on IP address - " + self.ip)
        udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        # Enable broadcasting mode
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
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


s1 = Server('127.0.0.1')
s1.main_server()
