import pickle
import socket
import struct
import threading
import cv2


def carla_send_images():
    print("Server is waiting for a connection at port 6011 connection...")
    # Send images over TCP
    image_socket_6011 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    image_socket_6011.bind(('127.0.0.1', 6011))
    image_socket_6011.listen(1)
    conn_6011, addr_6011 = image_socket_6011.accept()
    print(f"Image connection established with {addr_6011} at port 6011")

    print("Server is waiting for a connection at port 6012 connection...")
    # Send images over TCP
    image_socket_6012 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    image_socket_6012.bind(('127.0.0.1', 6012))
    image_socket_6012.listen(1)
    conn_6012, addr_6012 = image_socket_6012.accept()
    print(f"Image connection established with {addr_6012} at port 6012")


    cap = cv2.VideoCapture('Drive_night01.mp4')  # Replace with Carla camera
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Serialize the image to bytes for TCP
        serialized_frame = pickle.dumps(frame)
        message = struct.pack('>I', len(serialized_frame)) + serialized_frame
        conn_6011.sendall(message)
        conn_6012.sendall(message)



def receive_new_speed():
    # Receive new speed over UDP
    new_speed_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_speed_udp_socket.bind(('127.0.0.1', 6031))

    while True:
        new_speed_data, _ = new_speed_udp_socket.recvfrom(1024)
        new_speed = float(new_speed_data.decode())
        print(f"Speed: {new_speed}")

if __name__ == "__main__":
    threading.Thread(target=carla_send_images).start()
    threading.Thread(target=receive_new_speed).start()