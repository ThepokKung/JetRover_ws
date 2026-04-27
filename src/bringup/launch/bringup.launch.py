import os
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch import LaunchDescription, LaunchService
from launch.actions import IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource

def launch_setup(context):
    compiled = os.environ['need_compile']
    if compiled == 'True':
        controller_package_path = get_package_share_directory('controller')
        app_package_path = get_package_share_directory('app')
        peripherals_package_path = get_package_share_directory('peripherals')
        ros_tcp_endpoint_package_path = get_package_share_directory('ROS-TCP-Endpoint-main-ros2')
    else:
        # controller_package_path = '/home/ubuntu/JetRover_ws/src/driver/controller'
        controller_package_path = '/home/ubuntu/JetRover_ws/src/driver/controller' # for Class Project Only
        # app_package_path = '/home/ubuntu/JetRover_ws/src/app'
        app_package_path = '/home/ubuntu/JetRover_ws/src/app' # for Class Project Only
        # peripherals_package_path = '/home/ubuntu/JetRover_ws/src/peripherals' 
        peripherals_package_path = '/home/ubuntu/JetRover_ws/src/peripherals' # for Class Project Only
        ros_tcp_endpoint_package_path = '/home/ubuntu/JetRover_ws/src/ROS-TCP-Endpoint-main-ros2' # for Class Project Only
    
    ros_tcp_endpoint_node = Node(
        package='ros_tcp_endpoint',
        executable='default_server_endpoint',
        name='ros_tcp_endpoint',
        output='screen',
        respawn=True,
        parameters=[
             {"ROS_IP": "192.168.0.2"}
        ]
    )


    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(controller_package_path, 'launch/controller.launch.py')),
    )
    
    depth_camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(peripherals_package_path, 'launch/depth_camera.launch.py')),
    )

    lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(peripherals_package_path, 'launch/lidar.launch.py')),
    )

    init_pose_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(controller_package_path, 'launch/init_pose.launch.py')),
        launch_arguments={
            'namespace': '',  
            'use_namespace': 'false',
            'action_name': 'init',
        }.items(),
    )

    startup_check_node = Node(
        package='bringup',
        executable='startup_check',
        output='screen',
    )

    return [
            startup_check_node,
            controller_launch,
            depth_camera_launch,
            lidar_launch,
            init_pose_launch,
            ros_tcp_endpoint_node,
            ]

def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function = launch_setup)
    ])

if __name__ == '__main__':
    # 创建一个LaunchDescription对象(create a LaunchDescription object)
    ld = generate_launch_description()

    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
