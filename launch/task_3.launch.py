from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        # Start turtlesim
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),

        # Start go_to_goal with YAML parameters
        Node(
            package='turtle_controller',
            executable='go_to_goal',
            name='go_to_goal',
            parameters=[
                'config/params.yaml'
            ]
        ),

        # Start service client
        Node(
            package='turtle_controller',
            executable='toggle_client',
            name='toggle_client'
        )
    ])
