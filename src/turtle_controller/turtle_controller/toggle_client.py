import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class ToggleClient(Node):
    def __init__(self):
        super().__init__('toggle_client')

        self.client = self.create_client(SetBool, '/toggle_movement')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /toggle_movement service...')

        # 5 Second Delay
        self.timer = self.create_timer(5.0, self.send_request)
       
    def send_request(self):
        # Stop the timer so the request is sent only once
        self.timer.cancel()

        # Send True to start movement
        request = SetBool.Request()
        request.data = True



        self.future = self.client.call_async(request)
        self.future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        response = future.result()

        self.destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = ToggleClient()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()