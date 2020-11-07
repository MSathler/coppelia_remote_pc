#!/usr/bin/env python

"""
This node receives the motors telemetry from the espeleorobo and calculates the odometry based on the wheels velocity
It subscribes to the wheels velocities in ros_eposmcd/motor1 to motor6, published by ros_eposmcd
It publishes the odometry to odom topic
It can calculate the odometry using differential or skidsteering kinematic models,
just change the flag skid_steer to 1 if you want skid steer or to 0 if you want differential
The parameters used both for robot and skidsteer come from Eduardo Cota master thesis
https://gist.github.com/atotto/f2754f75bedb6ea56e3e0264ec405dcf
"""

from math import sin, cos, pi

import rospy
import tf

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from sensor_msgs.msg import JointState


class odometry:
    def __init__(self):

        # Kinematic model

        self.time_counter_aux = 0
        self.ros_init()
        self.pose = 0

    def ros_init(self):

        rospy.init_node('wheel_odometry_publisher', anonymous=True)

        # Times used to integrate velocity to pose
        self.current_time = 0.0
        self.last_time = 0.0

        # Create subscribers that receives the wheels velocities
        self.subscriber_mot = rospy.Subscriber("/pose", Pose, self.odom_conversion)

        # odom publisher
        self.odom_pub = rospy.Publisher("/odom", Odometry, queue_size=50)
        self.vel_pub = rospy.Publisher("robot_vel", Twist, queue_size=1)

        # Tf broadcaster
        self.odom_broadcaster = tf.TransformBroadcaster()

        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

    # Motor velocity callbacks

    def odom_conversion(self, message):
        self.pose = message
        odom = Odometry()
        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = "odom"

        # set the position
        odom.pose.pose = self.pose
	odom.pose.pose.position.z = self.pose.position.z - 40

        # set the velocity
        odom.child_frame_id = "espeleo_robo/base_link"

        self.odom_pub.publish(odom)

        self.last_time = self.current_time


if __name__ == '__main__':
    odometry_obj = odometry()
