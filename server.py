import socket

bind_ip = "127.0.0.1"
bind_port = 3000
bufferSize = 2048

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverSocket.bind((bind_ip, bind_port))
print("UDP server up and listening")

while True:
    message, clientAddress = serverSocket.recvfrom(bufferSize)
    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(clientAddress)
    print(clientMsg)
    print(clientIP)
    serverSocket.sendto(bytesToSend, clientAddress)
    break
