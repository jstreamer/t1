import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.10', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

while True:
    data = input("Message: ")

    message = str.encode(data)
    print('sending {}'.format(message))
    sock.sendall(message)

    response = sock.recv(10)
    print('received {}'.format(response))

    if str(response,"utf-8") == "terminatec":
        print("Terminating connection")
        break
print('closing socket')
sock.close()