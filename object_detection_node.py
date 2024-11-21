import pickle
import socket
import struct
import threading
import time
import cv2


def receive_images():

    # Send distance over UDP
    distance_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    distance_server = ('127.0.0.1', 6021)

    # Receive camera images over TCP
    image_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    image_socket.connect(('127.0.0.1', 6011))  # Replace <server_ip> with server's IP


    data = b""
    payload_size = struct.calcsize('>I')
    while True:

        # Retrieve message size
        while len(data) < payload_size:
            packet = image_socket.recv(4096)  # Adjust buffer size as needed
            if not packet:
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack('>I', packed_msg_size)[0]

        # Retrieve the actual message data
        while len(data) < msg_size:
            packet = image_socket.recv(4096)
            if not packet:
                break
            data += packet

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Deserialize the frame
        frame = pickle.loads(frame_data)

        # Display the frame
        cv2.imshow("Received Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # simulation delay process
        time.sleep(0.5)

        # send distance to interface node
        distance = 10
        distance_udp_socket.sendto(str(distance).encode(), distance_server)


if __name__ == "__main__":
    # Run each thread
    threading.Thread(target=receive_images).start()
