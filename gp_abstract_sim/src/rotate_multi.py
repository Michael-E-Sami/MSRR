#!/usr/bin/env python
import math
import os.path
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from std_msgs.msg import Float32
from gazebo_msgs.srv import GetModelState, SetModelState
from gazebo_msgs.msg import ModelState
#from mybot_gazebo.msg import PlanarOdometry, PlanarPose, PlanarTwist

###########################################################################

speed = Twist()

current_x = 0.0
current_y = 0.0
current_yaw = 0.0

yaw_goal = 0.0

pi = math.pi

#left_pub = rospy.Publisher('/ditto2/left_wheel_speed', Float32, queue_size=1000)
#right_pub = rospy.Publisher('/ditto2/right_wheel_speed', Float32, queue_size=1000)

###########################################################################

def rotlecall(data):
    # rospy.loginfo(rospy.get_caller_id() + "I heard ")
    global current_x
    global current_y
    global current_yaw

    current_x = data.pose.pose.position.x
    current_y = data.pose.pose.position.y
    rot_q = data.pose.pose.orientation
    (roll, pitch, current_yaw) = euler_from_quaternion([rot_q.x, rot_q.y,rot_q.z, rot_q.w])
    
    current_yaw = current_yaw*(180/pi)

    if current_yaw < 0:
        current_yaw +=  360

########################################################################### 
def rotate(omega,angle,ditto):
    ditstr=str(ditto)
    rospy.Subscriber("/ditto"+ditstr+"/odom", Odometry, rotlecall)
    left_pub = rospy.Publisher("/ditto"+ditstr+"/left_wheel_speed", Float32, queue_size=1000)
    right_pub = rospy.Publisher("/ditto"+ditstr+"/right_wheel_speed", Float32, queue_size=1000)
    save_path = os.path.dirname(__file__)
    name_of_file = "last_yaw_goal"
    completeName = os.path.join(save_path, name_of_file+".txt")         
    file1 = open(completeName, "r")
    first_yaw = file1.read()
    # print(first_yaw)
    first_yaw = float(first_yaw)
    file1.close()
    #ditto=str(input("please enter robot num::"))
    #angle=input("Please Enter Rotation Value(Degrees)::")
    #omega=input("Enter rotation speed::")
    yaw_goal = angle + first_yaw
    if yaw_goal < 0:
        yaw_goal = yaw_goal + 359.99
    elif yaw_goal > 359.99:
        yaw_goal = yaw_goal - 359.99

    file1 = open(completeName, "w")
    toFile = str(yaw_goal)
    file1.write(toFile)
    file1.close()

    global current_x
    global current_y
    global current_yaw
    #if (current_x == 0 and current_y == 0 and current_yaw == 0):
    #        rospy.wait_for_message("/ditto"+ditto+"/odom", Odometry, timeout=10)
    while not rospy.is_shutdown():
        print("Current Yaw: "),
        print(current_yaw)
        print("Yaw Goal: "),
        print(yaw_goal)
        print("Abs(yaw_goal - current_yaw) = "),
        print(abs(yaw_goal - current_yaw))

        if abs(yaw_goal - current_yaw) > 0.1:
            print("Angular Velocity")
            print(" ")
            
            if (angle >= 0):
                left_pub.publish(-omega)
                right_pub.publish(omega)
            else:
                left_pub.publish(omega)
                right_pub.publish(-omega)
        else:
            left_pub.publish(0)
            right_pub.publish(0) 
            rospy.signal_shutdown("FINISH")  
if __name__ == '__main__':
    rospy.init_node('Rotate_yeah',
                    anonymous=True, disable_signals=True)
    rotate(0.25,30,1)

