#!/usr/bin/env python

import sys, time
import rospy
from raspimouse_ros.srv import *
from raspimouse_ros.msg import *
from std_msgs.msg import UInt16

def switch_motors(onoff):
    rospy.wait_for_service('/raspimouse/switch_motors')
    try:
        p = rospy.ServiceProxy('/raspimouse/switch_motors', SwitchMotors)
        res = p(onoff)
        return res.accepted
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
    else:
        return False

def raw_control(left_hz,right_hz):
    pub = rospy.Publisher('/raspimouse/motor_raw', LeftRightFreq, queue_size=10)

    if not rospy.is_shutdown():
        d = LeftRightFreq()
        d.left = left_hz
        d.right = right_hz
        pub.publish(d)

lightsensors = LightSensorValues()

def lightsensor_callback(data):
    lightsensors.left_side = data.left_side
    lightsensors.right_side = data.right_side
    lightsensors.left_forward = data.left_forward
    lightsensors.right_forward = data.right_forward

def left_walltrace(ls):
    if lightsensors.left_forward > 1500 or lightsensors.right_forward > 1500:
        raw_control(0,0)
        return False

    base = 500
    e = 0.2 * (ls.left_side - 700)
    raw_control(base + e,base - e)
    return True
        
def turn(right):
        if right:   raw_control(250,-250)
        else:       raw_control(-250,250)
        return lightsensors.left_forward > 500 or lightsensors.right_forward  > 500

def stop_motors():
    raw_control(0,0)
    switch_motors(False)

if __name__ == "__main__":
    rospy.init_node("lefthand")
    rospy.on_shutdown(stop_motors)

    ### motor_raw test ###
    if not switch_motors(True):
        print "[check failed]: motors are not empowered"
        sys.exit(1)

    subls = rospy.Subscriber('/raspimouse/lightsensors', LightSensorValues, lightsensor_callback)

    r = rospy.Rate(10)

    wall = False
    while not rospy.is_shutdown():
        if wall:
            wall = turn(lightsensors.left_side > 500)
        else:
            wall = not left_walltrace(lightsensors)
            
        r.sleep()

    stop_motors()
