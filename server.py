import socket
import threading
import time
from random import shuffle


all_teams = {}


def main_tcp_funk():
    bind_ip = "127.0.0.1"
    bind_port = 9999

    tcp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    tcp_server_socket.bind((bind_ip, bind_port))
    tcp_server_socket.listen(1)
    tcp_server_socket.settimeout(0)
    i = 0
    future = time.time() + 15

    while time.time() < future:
        try:
            connected_socket, address = tcp_server_socket.accept()
        except:
            continue
        thread_funk = threading.Thread(target=recv_name, args=(connected_socket,))
        thread_funk.start()
        i += 1
    all_teams_lst = list(all_teams.keys())
    shuffle(all_teams_lst)
    team1 = all_teams_lst[:len(all_teams_lst)//2]
    team2 = all_teams_lst[len(all_teams_lst)//2:]
    message_to_send_at_begin = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n"
    for player_name in team1:
        message_to_send_at_begin += player_name + "\n"
    message_to_send_at_begin += "\nGroup 2:\n"
    for player_name in team2:
        message_to_send_at_begin += player_name + "\n"
    message_to_send_at_begin += "Start pressing keys on your keyboard as fast as you can!!"
    for player_name in all_teams_lst:
        thread_funk = threading.Thread(target=handel_client, args=(message_to_send_at_begin, player_name))
        thread_funk.start()
    print(message_to_send_at_begin)


def recv_name(connected_socket):
    global all_teams
    message = connected_socket.recv(2048)
    message = message.decode("utf-8")
    print(message)
    print("boo")
    all_teams[message] = connected_socket


def handel_client(message, client_name):
    global all_teams
    connection = all_teams[client_name]
    connection.send(str.encode(message))


def udp_server():
    bind_ip = "127.0.0.1"
    bind_port = 13117
    print("Server started, listening on IP address - " + bind_ip)
    print("hi")
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    # Enable broadcasting mode
    udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_server_socket.settimeout(30)
    # udp_server_socket.bind((bind_ip, bind_port))
    # bytesToSend1 = bytes(0xfeedbeef)
    bytes_to_send1 = str.encode('feedbeef9999')
    bytes_to_send2 = bytes(0x2)
    bytes_to_send3 = bytes(0x9999)

    count_time = 0
    while count_time < 15:
        udp_server_socket.sendto(bytes_to_send1, (bind_ip, bind_port))
        time.sleep(1)
        count_time += 1
        print(count_time)
    print("No more players for know")


client_handler = threading.Thread(target=udp_server)
client_handler.start()
client_handler2 = threading.Thread(target=TCP_Main_Listener)
client_handler2.start()
time.sleep(20)
print("Players: ")
for key in all_teams:
    print(key)




def TCP_Main_Listener():
    bind_ip = "127.0.0.1"
    bind_port = 9999

    tcp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    tcp_server_socket.bind((bind_ip, bind_port))
    while True:
        try:
            connected_socket, address = tcp_server_socket.accept()
            thread_funk = threading.Thread(target=recv_name, args=(connected_socket,))
            thread_funk.start()
        except:
            continue