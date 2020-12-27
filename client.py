import socket

serverAddressPort = ("127.0.0.1", 13117)
bufferSize = 2048
print("Client started, listening for offer requests...")

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
#udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udp_client_socket.bind(serverAddressPort)
resv_message, serverAddress = udp_client_socket.recvfrom(bufferSize)
#udp_client_socket.close()
print("Received offer from {} attempting to connect...".format(serverAddress[0]))
udp_port = serverAddress[1]
print(udp_port)

resv_message = resv_message.decode("utf-8")
#resv_message = bytes.hex(resv_message)
if resv_message[:8] == "feedbeef":
    print("the correct password")
    serverAddress = ('127.0.0.1', int(resv_message[-4:]))
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client_socket.connect(serverAddress)
    tcp_client_socket.send(str.encode("team rokets port {}\n".format(udp_port)))
    message = tcp_client_socket.recv(bufferSize)
    message = message.decode("utf-8")
    print(message)
