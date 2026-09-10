import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import SetBool

class GoToGoal(Node):
    def __init__(self):
        super().__init__('go_to_goal')

        # Declare ROS 2 Parameters
        self.declare_parameter('target_x', 10.0)
        self.declare_parameter('target_y', 10.0)
        self.declare_parameter('linear_gain', 1.5)
        self.declare_parameter('angular_gain', 6.0)
        self.declare_parameter('distance_tolerance', 0.1)
        self.declare_parameter('angle_tolerance', 0.05)
        self.declare_parameter('loop_rate_hz', 20.0)

        # Target Goal Coordinates
        self.goal_x = self.get_parameter('target_x').value
        self.goal_y = self.get_parameter('target_y').value

        # Proportional Gains (K_p)
        self.kp_linear = self.get_parameter('linear_gain').value
        self.kp_angular = self.get_parameter('angular_gain').value

        # Tolerances
        self.distance_tolerance = self.get_parameter('distance_tolerance').value
        self.angle_tolerance = self.get_parameter('angle_tolerance').value

        # Control Loop Frequency
        self.loop_rate = self.get_parameter('loop_rate_hz').value

        # State Variables
        self.current_pose = None
        self.goal_reached = False
        self.movement_enabled = False

        
        # ROS 2 Publisher & Subscriber
        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_subscriber = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10
        )

        self.toggle_service = self.create_service(
            SetBool, '/toggle_movement', self.toggle_movement_callback

)


        # Control Loop running at the parameterized frequency
        self.timer = self.create_timer(1.0 / self.loop_rate, self.control_loop)

        self.get_logger().info(
            f'Navigating turtle to target goal: ({self.goal_x}, {self.goal_y})'
        )

    def pose_callback(self, msg: Pose):
        """Update current position and heading from /turtle1/pose stream."""
        self.current_pose = msg

   
   
    def toggle_movement_callback(self, request, response):
        """Enable or disable turtle movement."""
        self.movement_enabled = request.data
        response.success = True

        return response

   
   
    def normalize_angle(self, angle: float) -> float:
        """Keep heading angle within [-pi, pi] to avoid unnecessary 360-degree turns."""
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle

    def control_loop(self):
        """Proportional Control Loop."""
        if self.current_pose is None or self.goal_reached or not self.movement_enabled:
            return

        dx = self.goal_x - self.current_pose.x
        dy = self.goal_y - self.current_pose.y

        distance_error = math.sqrt(dx**2 + dy**2)

        target_angle = math.atan2(dy, dx)
        heading_error = self.normalize_angle(target_angle - self.current_pose.theta)

        msg = Twist()

        # 2. Check if Goal is Reached
        if distance_error < self.distance_tolerance:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.cmd_vel_publisher.publish(msg)
            self.goal_reached = True
            self.get_logger().info('Goal Reached Successfully!')
            return

        # 3. Proportional Control Logic
        # If heading error is large, align facing direction first before moving forward
        if abs(heading_error) > self.angle_tolerance:
            msg.linear.x = 0.0
            msg.angular.z = self.kp_angular * heading_error
        else:
            # Scale forward speed and heading alignment concurrently
            msg.linear.x = min(self.kp_linear * distance_error, 2.0)  # Cap speed at 2.0 m/s
            msg.angular.z = self.kp_angular * heading_error

        self.cmd_vel_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = GoToGoal()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()