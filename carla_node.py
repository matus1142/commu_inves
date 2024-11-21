import pickle
import socket
import struct
import threading
import cv2


def carla_send_images():
    # Send images over TCP
    image_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    image_socket.bind(('192.168.1.69', 6011))
    image_socket.listen(1)

    print("Server is waiting for a connection...")
    conn, addr = image_socket.accept()
    print(f"Image connection established with {addr}")

    cap = cv2.VideoCapture('Drive_night01.mp4')  # Replace with Carla camera
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Serialize the image to bytes for TCP
        serialized_frame = pickle.dumps(frame)
        message = struct.pack('>I', len(serialized_frame)) + serialized_frame
        conn.sendall(message)



def receive_new_speed():
    # Receive new speed over UDP
    new_speed_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_speed_udp_socket.bind(('192.168.1.69', 6031))

    while True:
        new_speed_data, _ = new_speed_udp_socket.recvfrom(1024)
        new_speed = float(new_speed_data.decode())
        print(f"Speed: {new_speed}")

if __name__ == "__main__":
    threading.Thread(target=carla_send_images).start()
    threading.Thread(target=receive_new_speed).start()