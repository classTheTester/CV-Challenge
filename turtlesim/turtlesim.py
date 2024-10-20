#Edward Weisberg, weisbere


import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
import threading

class SquareCircleDrawer(Node):
    def __init__(self):
        super().__init__('square_circle_drawer')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.square_thread = threading.Thread(target=self.draw_square)
        self.square_thread.start()

    def draw_square(self):
        # Draw square
        side_length = 2.0  # Length of each side of the square
        for _ in range(4):
            self.move_forward(side_length)
            self.turn(90)  # Turn right 90 degrees
        
        # Move to the starting position for the circle
        self.move_forward(side_length)
        self.turn(90)

        # Draw circle
        self.draw_circle()

    def move_forward(self, distance):
        msg = Twist()
        msg.linear.x = 1.0  # Forward speed
        msg.angular.z = 0.0  # No turn
        steps = 10  # Number of small steps to cover the distance
        for _ in range(steps):
            self.publisher_.publish(msg)
            time.sleep(distance / steps)

    def turn(self, angle):
        msg = Twist()
        msg.linear.x = 0.0  # No forward motion
        msg.angular.z = angle * (3.14 / 180)  # Convert angle to radians
        self.publisher_.publish(msg)
        time.sleep(abs(angle) / 90)  # Adjust the time for turning

    def draw_circle(self):
        msg = Twist()
        msg.linear.x = 1.0  # Forward speed
        msg.angular.z = 1.0  # Turn rate

        # Draw a circle
        while rclpy.ok():
            self.publisher_.publish(msg)
            self.get_logger().info('Drawing Circle: "%s"' % msg)
            time.sleep(0.1)  # Adjust the frequency as needed

def main(args=None):
    rclpy.init(args=args)
    square_circle_drawer = SquareCircleDrawer()

    try:
        rclpy.spin(square_circle_drawer)  # Keep the node alive
    except KeyboardInterrupt:
        pass
    finally:
        square_circle_drawer.square_thread.join()  # Wait for the thread to finish
        square_circle_drawer.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
