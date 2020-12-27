import socket
import threading
import time


def handle_client_connection(ip, port):
    print("handle_client_connection")
    print("ip - " + ip)
    print("port - " + str(port))


bind_ip = "127.0.0.1"
bind_port = 13117
bufferSize = 2048
max_clients = 2
print("Server started, listening on IP address - " + bind_ip)

msgFromServer = "Welcome to Tomer & Elad game!"
bytesToSend = str.encode(msgFromServer)
UDP_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDP_server_socket.bind((bind_ip, bind_port))

future = time.time() + 10
clients_address = []
while time.time() < future:
    message, clientAddress = UDP_server_socket.recvfrom(bufferSize)
    print(clientAddress)
    clients_address.append(clientAddress)
    UDP_server_socket.sendto(bytesToSend, clientAddress)
    client_handler = threading.Thread(target=handle_client_connection, args=clientAddress)
    client_handler.start()
