import socket
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class ROS2DistancePublisher(Node):
    def __init__(self):
        # Initialize the ROS 2 node
        super().__init__('ros2_distance_publisher')
        
        # Create a publisher for the 'distance' topic
        self.publisher_ = self.create_publisher(Float64, 'distance', 10)
        self.get_logger().info('ROS 2 Distance Publisher Node started.')

    def publish_distance(self, distance):
        # Publish the received distance data
        msg = Float64()
        msg.data = distance
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published Distance: {distance}")


def receive_distance(ros2_publisher):
    # Receive distance over UDP
    distance_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    distance_udp_socket.bind(('192.168.1.185', 6021))

    while True:
        try:
            # Receive distance data
            distance_data, _ = distance_udp_socket.recvfrom(1024)
            distance = float(distance_data.decode())
            print(f"Received Distance: {distance}")
            
            # Publish the distance data via ROS 2
            ros2_publisher.publish_distance(distance)
        except Exception as e:
            print(f"Error receiving distance: {e}")


def send_new_speed():
    # Send new_speed over UDP
    new_speed_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_speed_server = ('192.168.1.69', 6031)

    while True:
        try:
            new_speed = 15
            new_speed_udp_socket.sendto(str(new_speed).encode(), new_speed_server)
            # print(f"Sent Speed: {new_speed}")
        except Exception as e:
            print(f"Error sending speed: {e}")


if __name__ == "__main__":
    # Initialize ROS 2
    rclpy.init()

    # Create the ROS 2 publisher node
    ros2_publisher = ROS2DistancePublisher()

    # Start the threads
    threading.Thread(target=receive_distance, args=(ros2_publisher,), daemon=True).start()
    threading.Thread(target=send_new_speed, daemon=True).start()

    try:
        # Spin the ROS 2 node to handle publishing
        rclpy.spin(ros2_publisher)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        # Clean up resources
        ros2_publisher.destroy_node()
        rclpy.shutdown()
