import socket
print("this is it")
serverAddressPort = ("127.0.0.1", 13117)
bufferSize = 2048
print("Client started, listening for offer requests...")

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udp_client_socket.bind(serverAddressPort)
resv_message, serverAddress = udp_client_socket.recvfrom(bufferSize)
#udp_client_socket.close()
print("Received offer from {} attempting to connect...".format(serverAddress[0]))
udp_port = serverAddress[1]
print(udp_port)
print("\n")
count = 0;
while count < len(serverAddress):
    print(serverAddress[count])
    count += 1

resv_message = resv_message.decode("utf-8")
#resv_message = bytes.hex(resv_message)
if resv_message[:8] == "feedbeef":
    print("the correct password")
    serverAddress = ('127.0.0.1', int(resv_message[-4:]))
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client_socket.connect(serverAddress)
    tcp_client_socket.send(str.encode("team rokets port {}\n".format(udp_port)))
    #the problem is that we are trying to connect to the master TCP server port, and not to the address we get from this tcp server.
    #the proccess should be:  wait for UDP -> rcv offer -> connect to master TCP -> rcv address to connect -> connect to address
    # -> send msg to address
    message = tcp_client_socket.recv(bufferSize)
    message = message.decode("utf-8")
    print(message)
