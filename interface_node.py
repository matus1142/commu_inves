
import socket
import struct
import threading


def receive_distance():
    # Receive distance over UDP
    distance_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    distance_udp_socket.bind(('127.0.0.1', 6021))

    while True:
        distance_data, _ = distance_udp_socket.recvfrom(1024)
        distance = float(distance_data.decode())
        print(f"Speed: {distance}")


def send_new_speed():
    # Send new_speed over UDP
    new_speed_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_speed_server = ('127.0.0.1', 6031)
    while True:
        new_speed = 15
        new_speed_udp_socket.sendto(str(new_speed).encode(), new_speed_server)

if __name__ == "__main__":
    threading.Thread(target=receive_distance).start()
    threading.Thread(target=send_new_speed).start()