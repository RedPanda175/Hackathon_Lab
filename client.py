import socket

serverAddressPort = ("127.0.0.1", 13117)
bufferSize = 2048
print("Client started, listening for offer requests...")

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udp_client_socket.bind(serverAddressPort)
resv_message, serverAddress = udp_client_socket.recvfrom(bufferSize)
print("Received offer from {} attempting to connect...".format(serverAddress[0]))

if bytes.hex(resv_message)[:8] == "feedbeef":
    print("the correct password")
    print(resv_message, serverAddress)
    serverAddress = ('127.0.0.1', 9999)
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client_socket.connect(serverAddress)
    tcp_client_socket.send(str.encode("team rokets\n"))
    print("send message")
