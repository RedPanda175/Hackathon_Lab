import socket

serverAddressPort = ("127.0.0.1", 13117)
bufferSize = 2048
print("Client started, listening for offer requests...")

msgFromClient = "0xfeedbeef"
bytesToSend = str.encode(msgFromClient)
clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientSocket.sendto(bytesToSend, serverAddressPort)

resv_message, serverAddress = clientSocket.recvfrom(bufferSize)
print("Received offer from {} attempting to connect...".format(serverAddress[0]))

clientSocket.close()
print(resv_message)
print(serverAddress)
