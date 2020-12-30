import socket
import threading
import time
from random import shuffle
import struct
import operator


class Colors:
    CEND = '\33[0m'  # 0

    CBLACK = '\33[30m'  # 1
    CRED = '\33[31m'  # 2
    CGREEN = '\33[32m'  # 3
    CYELLOW = '\33[33m'  # 4
    CBLUE = '\33[34m'  # 5
    CVIOLET = '\33[35m'  # 6
    CBEIGE = '\33[36m'  # 7
    CWHITE = '\33[37m'  # 8

    CGREY = '\33[90m'  # 9
    CRED2 = '\33[91m'  # 10
    CGREEN2 = '\33[92m'  # 11
    CYELLOW2 = '\33[93m'  # 12
    CBLUE2 = '\33[94m'  # 13
    CVIOLET2 = '\33[95m'  # 14
    CBEIGE2 = '\33[96m'  # 15
    CWHITE2 = '\33[97m'  # 16


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
        self.tcp_port = 8473
        self.best_team = ("None", 0)
        self.lock_best_team = threading.Lock()
        self.end_message = Colors.CRED + "Game over!\n" + Colors.CEND + Colors.CGREEN + "Group 1 typed in {} characters.\n" + Colors.CEND + Colors.CBLUE + "Group 2 typed in {} characters." + Colors.CEND
        self.end_message_part2 = "\nGroup {} wins!\n" + Colors.CYELLOW + "Congratulations to the winners:\n==\n==" + Colors.CEND
        self.end_message_draw = "\nIt's a draw!\n" + Colors.CYELLOW + "Congratulations to both teams!!!" + Colors.CEND

    def tcp_main_listener(self):
        condition = threading.Condition()
        all_threads = []

        tcp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        did_bind = False
        while not did_bind:
            try:
                tcp_server_socket.bind(('', 0))
                did_bind = True
            except:
                print("error")
        self.tcp_port = tcp_server_socket.getsockname()[1]
        tcp_server_socket.settimeout(self.time_to_connect)
        tcp_server_socket.listen(17)
        start_time = time.time()
        while start_time + self.time_to_connect > time.time():
            try:
                connected_socket, address = tcp_server_socket.accept()
                print(address)
                thread_funk = threading.Thread(target=self.handle_client, args=(connected_socket, condition))
                thread_funk.start()
                all_threads.append(thread_funk)
            except:
                if self.time_to_connect - time.time() + start_time > 0:
                    tcp_server_socket.settimeout(self.time_to_connect - time.time() + start_time)
                continue
        print("time - ", time.time() - start_time)

        all_teams_lst = list(self.all_teams.keys())
        shuffle(all_teams_lst)
        self.team1 = all_teams_lst[:len(all_teams_lst) // 2]
        self.team2 = all_teams_lst[len(all_teams_lst) // 2:]
        self.message_to_send_at_begin = Colors.CVIOLET + "Welcome to Keyboard Spamming Battle Royale.\n" + Colors.CEND + Colors.CGREEN + "Group 1:\n" + Colors.CEND
        for player_name in self.team1:
            self.message_to_send_at_begin += player_name + "\n"
        self.message_to_send_at_begin += Colors.CBLUE + "\nGroup 2:\n" + Colors.CEND
        for player_name in self.team2:
            self.message_to_send_at_begin += player_name + "\n"
        self.message_to_send_at_begin += Colors.CYELLOW + "Start pressing keys on your keyboard as fast as you can!!\nGO GO GO!!!" + Colors.CEND

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
        for my_tread in all_threads:
            my_tread.join()
        print(Colors.CRED + "Game over, sending out offer requests..." + Colors.CEND)
        self.main_server()

    def handle_client(self, connected_socket, cv):
        try:
            message = connected_socket.recv(2048)
        except:
            print("error")
        message = message.decode("utf-8")
        if message in self.all_teams:
            message = message[:-1] + str(len(self.all_teams))
        message = message[:-1]
        self.all_teams[message] = {}
        print(message)
        with cv:
            cv.wait()
        chars = []
        try:
            connected_socket.send(str.encode(self.message_to_send_at_begin))
        except:
            print("error")
        connected_socket.settimeout(10)
        start_time = time.time()
        future = time.time() + 10
        while future > time.time():
            try:
                ch = connected_socket.recv(1024)
            except:
                continue
            chars.append(list(ch.decode("utf-8")))
            time_pass = time.time() - start_time
            connected_socket.settimeout(10 - time_pass)
        dict_chars = {}
        for lst in chars:
            for c in lst:
                if c in dict_chars:
                    dict_chars[c] += 1
                else:
                    dict_chars[c] = 1
        self.all_teams[message] = dict_chars
        print("put in main dict - ", dict_chars)
        if dict_chars == {}:
            max_char = "None"
        else:
            max_char = max(dict_chars.items(), key=operator.itemgetter(1))[0]
        self.lock_best_team.acquire()
        if self.best_team[1] < len(chars):
            self.best_team = (message, len(chars))
        self.lock_best_team.release()
        with cv:
            cv.wait()
        to_send = self.end_message + "\nYour most common char is - " + max_char
        to_send += "\nThe beat team ever on this server is {} with {} points\n".format(self.best_team[0],
                                                                                       self.best_team[1])
        try:
            connected_socket.send(str.encode(to_send))
        except:
            print("error")

    def who_won(self):
        print("start calculate")
        for team in self.team1:
            for c in self.all_teams[team]:
                self.team1_points += self.all_teams[team][c]
        for team in self.team2:
            for c in self.all_teams[team]:
                self.team2_points += self.all_teams[team][c]

    def udp_server(self):
        print(Colors.CYELLOW + "Server started, listening on IP address - " + Colors.CEND + self.ip)
        udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        # Enable broadcasting mode
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_server_socket.settimeout(self.time_to_connect)

        magic_cookie = 0xfeedbeef
        message_type = 0x2
        message = struct.pack('IBH', magic_cookie, message_type, self.tcp_port)

        count_time = 0
        while count_time < self.time_to_connect:
            udp_server_socket.sendto(message, (self.ip, 13125))
            time.sleep(1)
            count_time += 1
            print(count_time)
        print("No more players for know")

    def main_server(self):
        self.all_teams = {}
        self.message_to_send_at_begin = ""
        self.team1 = []
        self.team2 = []
        self.team1_points = 0
        self.team2_points = 0
        client_handler2 = threading.Thread(target=self.tcp_main_listener)
        client_handler2.start()
        client_handler = threading.Thread(target=self.udp_server)
        client_handler.start()


s1 = Server("<broadcast>")
s1.main_server()
