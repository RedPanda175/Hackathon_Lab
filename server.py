import socket
import threading
import time
from random import shuffle
import struct

all_teams = {}
time_to_connect = 13


def tcp_main_listener():
    global time_to_connect
    bind_ip = "127.0.0.1"
    bind_port = 8473

    condition = threading.Condition()

    tcp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    tcp_server_socket.bind((bind_ip, bind_port))
    tcp_server_socket.settimeout(time_to_connect)
    tcp_server_socket.listen(1)
    start_time = time.time()
    while start_time + time_to_connect > time.time():
        try:
            connected_socket, address = tcp_server_socket.accept()
            thread_funk = threading.Thread(target=recv_name, args=(connected_socket, condition))
            thread_funk.start()
        except:
            if time_to_connect - time.time() + start_time > 0:
                tcp_server_socket.settimeout(time_to_connect - time.time() + start_time)
            continue

    all_teams_lst = list(all_teams.keys())
    shuffle(all_teams_lst)
    team1 = all_teams_lst[:len(all_teams_lst) // 2]
    team2 = all_teams_lst[len(all_teams_lst) // 2:]
    message_to_send_at_begin = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n"
    for player_name in team1:
        message_to_send_at_begin += player_name + "\n"
    message_to_send_at_begin += "\nGroup 2:\n"
    for player_name in team2:
        message_to_send_at_begin += player_name + "\n"
    message_to_send_at_begin += "Start pressing keys on your keyboard as fast as you can!!"
    print("test test test")
    print(message_to_send_at_begin)
    with condition:
        condition.notifyAll()


def recv_name(connected_socket, cv):
    global all_teams
    message = connected_socket.recv(2048)
    message = message.decode("utf-8") + str(len(all_teams))
    print(message)
    all_teams[message] = connected_socket
    with cv:
        cv.wait()
    print(message)
    # connected_socket.send(str.encode("last msg"))


def handle_client(message, client_name):
    global all_teams
    connection = all_teams[client_name]
    connection.send(str.encode(message))


def udp_server():
    global time_to_connect
    bind_ip = "127.0.0.1"
    bind_port = 13117
    print("Server started, listening on IP address - " + bind_ip)
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    # Enable broadcasting mode
    # udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_server_socket.settimeout(time_to_connect)
    # udp_server_socket.bind((bind_ip, bind_port))
    # bytesToSend1 = bytes(0xfeedbeef)
    magic_cookie = 0xfeedbeef
    message_type = 0x2
    server_tcp_port = 0x8473
    message = struct.pack('IBH', magic_cookie, message_type, server_tcp_port)

    count_time = 0
    while count_time < time_to_connect:
        udp_server_socket.sendto(message, (bind_ip, bind_port))
        time.sleep(1)
        count_time += 1
        print(count_time)
    print("No more players for know")


client_handler = threading.Thread(target=udp_server)
client_handler.start()
client_handler2 = threading.Thread(target=tcp_main_listener)
client_handler2.start()
time.sleep(time_to_connect + 3)
print("Players: ")
for key in all_teams:
    print(key)
