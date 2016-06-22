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

def switch_callback(data):
    print "switches:",data.front, data.center, data.rear

def pos_control(left_hz,right_hz,time_ms):
    rospy.wait_for_service('/raspimouse/put_motor_freqs')
    try:
        p = rospy.ServiceProxy('/raspimouse/put_motor_freqs', PutMotorFreqs)
        res = p(left_hz,right_hz,time_ms)
        return res.accepted
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
    else:
        return False


def left_walltrace(ls):
    motor = 500
    #e = 0.2 * (ls.left_side + (ls.left_forward - ls.right_forward)*0.5 - 700)
    e = 0.2 * (ls.left_side - 700)
    motor_r = motor - e
    motor_l = motor + e
    raw_control(motor_l,motor_r)

if __name__ == "__main__":
    rospy.init_node("lefthand")

    ### motor_raw test ###
    if not switch_motors(True):
        print "[check failed]: motors are not empowered"
        sys.exit(1)

    subls = rospy.Subscriber('/raspimouse/lightsensors', LightSensorValues, lightsensor_callback)

    r = rospy.Rate(10)
    wall = False
    turnright = True

    try:
        while not rospy.is_shutdown():
            if wall:
                if turnright:
                    raw_control(250,-250)
                else:
                    raw_control(-250,250)

                if lightsensors.left_forward < 500 and lightsensors.right_forward  < 500:
                    wall = False
            else:
                left_walltrace(lightsensors)

                if lightsensors.left_forward > 1500 or lightsensors.right_forward > 1500:
                    wall = True
                    raw_control(0,0)
                    if lightsensors.left_side > 500:
                        turnright = True
                    else:
                        turnright = False
                
            r.sleep()

    except rospy.ROSInterruptException:
        raw_control(0,0)
        switch_motors(False)

