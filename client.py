import socket

msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("127.0.0.1", 3000)
bufferSize = 2048

clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientSocket.sendto(bytesToSend, serverAddressPort)

resv_message, serverAddress = clientSocket.recvfrom(bufferSize)

clientSocket.close()
print(resv_message)
