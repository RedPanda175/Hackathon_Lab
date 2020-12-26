import socket
import threading


def handle_client_connection():
    print("handle_client_connection")


bind_ip = "127.0.0.1"
bind_port = 13117
bufferSize = 2048
max_clients = 4
print("Server started, listening on IP address - " + bind_ip)

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)
serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverSocket.bind((bind_ip, bind_port))

clients_address = []
while len(clients_address) < max_clients:
    message, clientAddress = serverSocket.recvfrom(bufferSize)
    clients_address.apped(clientAddress)
    client_handler = threading.Thread(target=handle_client_connection)
    client_handler.start()
    #serverSocket.sendto(bytesToSend, clientAddress)
