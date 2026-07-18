#!/usr/bin/env python3
"""
odom_to_tf_broadcaster.py

Читает nav_msgs/Odometry из навигационного стека и транслирует
преобразование odom -> base_link в TF-дерево.

Запуск:
    ros2 run <ваш_пакет> odom_to_tf_broadcaster \
        --ros-args -p odom_frame:=odom -p base_frame:=base_link
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class OdomToTfNode(Node):
    def __init__(self):
        super().__init__('odom_to_tf_broadcaster')

        # Имена кадров и топик можно переопределить параметрами
        self.declare_parameter('odom_frame', 'odom')
        self.declare_parameter('base_frame', 'base_link')
        self.declare_parameter('odom_topic', '/odom')

        self.odom_frame = self.get_parameter('odom_frame').value
        self.base_frame = self.get_parameter('base_frame').value
        odom_topic = self.get_parameter('odom_topic').value

        # QoS под одометрию: best-effort/volatile — типично для сенсорных
        # топиков в Nav2. Если источник шлёт RELIABLE, поменяйте надёжность.
        # qos = QoSProfile(
        #     depth=10,
        #     reliability=ReliabilityPolicy.BEST_EFFORT,
        #     durability=DurabilityPolicy.VOLATILE,
        # )

        self.tf_broadcaster = TransformBroadcaster(self)
        self.odom_sub = self.create_subscription(
            Odometry, '/model/my_robot/odometry', self.odom_callback, 10
        )

        self.get_logger().info(
            f'Транслирую {self.odom_frame} -> {self.base_frame} '
            f'из топика {odom_topic}'
        )

    def odom_callback(self, msg: Odometry) -> None:
        t = TransformStamped()

        # ВАЖНО: берём штамп времени из самого сообщения одометрии, а не
        # node.get_clock().now(). Так TF будет синхронизирован с данными
        # сенсора, и Nav2/SLAM не получат extrapolation-ошибок.
        t.header.stamp = msg.header.stamp
        t.header.frame_id = self.odom_frame       # parent: odom
        t.child_frame_id = self.base_frame        # child:  base_link

        pose = msg.pose.pose
        t.transform.translation.x = pose.position.x
        t.transform.translation.y = pose.position.y
        t.transform.translation.z = pose.position.z
        t.transform.rotation.x = pose.orientation.x
        t.transform.rotation.y = pose.orientation.y
        t.transform.rotation.z = pose.orientation.z
        t.transform.rotation.w = pose.orientation.w

        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = OdomToTfNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()