#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import cos, pow, sin, sqrt

import rospy
from geometry_msgs.msg import Point, Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from tf.transformations import euler_from_quaternion

# from planarMovement import *

# Ana 3ayez a-Define Function
# Bta5od Distance
# W esm el Ditto / El publishers bto3o


###########################################################################

frw_x = 0.0
frw_y = 0.0
frw_yaw = 0.0

###########################################################################


def callbackFrw(data):
    global frw_x
    global frw_y
    global frw_yaw

    frw_x = data.pose.pose.position.x
    frw_y = data.pose.pose.position.y
    rotFrw = data.pose.pose.orientation
    (rotFrwroll, rotFrwpitch, frw_yaw) = euler_from_quaternion(
        [rotFrw.x, rotFrw.y, rotFrw.z, rotFrw.w])

###########################################################################


def forwardFn(goal_x, goal_y, Omega, left, right, dittoNum):
    # rospy.init_node('planarMovement', anonymous=True, disable_signals=True)
    print(" ")
    print("Forwarding")

    frwDitto = str(dittoNum)

    omega = Float32(Omega)

    rospy.Subscriber("ditto" + frwDitto + "/odom", Odometry, callbackFrw)

    rospy.wait_for_message("ditto" + frwDitto + "/odom", Odometry, timeout=5)

    while not rospy.is_shutdown():
        FrwDiff_x = goal_x - frw_x
        FrwDiff_y = goal_y - frw_y

        eucFrw = sqrt(pow(FrwDiff_x, 2)+pow(FrwDiff_y, 2))

        print'Dist. in X to goal_x= ', FrwDiff_x
        print'Dist. in Y to goal_y= ', FrwDiff_y
        print'euc= ', eucFrw

        while eucFrw > 0.05 and not rospy.is_shutdown():
            FrwDiff_x = goal_x - frw_x
            FrwDiff_y = goal_y - frw_y
            eucFrw = sqrt(pow(FrwDiff_x, 2)+pow(FrwDiff_y, 2))
            
            print("Inside While Loop")
            print(frw_x)
            left.publish(omega)
            right.publish(omega)

        print("Left While Loop")

        left.publish(0)
        right.publish(0)
        break

