import socket
import sys
import time
import threading
import odroid_wiringpi as wiringpi

OUTPUT = 1
left_motor_speed_pin = 23
wiringpi.wiringPiSetup()
wiringpi.pinMode(left_motor_speed_pin, OUTPUT)
wiringpi.softPwmCreate(left_motor_speed_pin, 0, 100)


left_truck_speed = 0
right_truck_speed = 0
left_truck_operational = True
pulse_delay = 0.01


def left_truck_movement_loop():
    print("Starting left track")
    while left_truck_operational:
        if left_truck_speed == 0:
            wiringpi.softPwmWrite(left_motor_speed_pin, 0)
            continue
        wiringpi.softPwmWrite(left_motor_speed_pin, left_truck_speed)


left_truck = threading.Thread(target=left_truck_movement_loop)
left_truck.start()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.1.10', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = str(connection.recv(10), "utf-8")
            print('received {}'.format(data))
            if data:
                if data.startswith("s"):
                    print("Speed parameter received")
                    speed_left = data.split("l")[1].split("r")[0]
                    speed_right = data.split("r")[1]
                    left_truck_speed = int(speed_left)
                    print("speed: left = {} right = {}".format(speed_left, speed_right))
                    connection.sendall(str.encode("OK"))
                elif data == "terminatec":
                    connection.sendall(str.encode(data))
                    connection.close()
                    left_truck_operational = False
                    exit()
                else:
                    print("Unknown control received - {}".format(data))
                    connection.sendall(str.encode("Unknown control"))
            else:
                print('no data from', client_address)
                break


    finally:
        # Clean up the connection
        connection.close()
        left_truck_operational = False
