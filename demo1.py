#!/usr/bin/env python

import time,sys,threading
import rospy
from std_msgs.msg import *
from raspimouse_ros.msg import *
from raspimouse_ros.srv import *
from check_driver_io import *

class RP(object):
    def __init__(self):
	self.__lightsensor_sub = rospy.Subscriber('/raspimouse/lightsensors', LightSensorValues, self.lightsensor_callback)
	self.__lv = LightSensorValues()
#	self.p = rospy.get_param('~p_gain', 0.1)
	rospy.on_shutdown(self.shutdown_hook)

    def lightsensor_callback(self, data):
        self.__lv = data

    def get_left_lightsensor(self):
        return(self.__lv.left_side)

    def get_forward_lightsensor(self):
        return(self.__lv.left_forward + self.__lv.right_forward) * 0.5

    def shutdown_hook(self):
        print pos_control(0, 0, 0)
        print switch_motors(False)

    def left_walltrace(self):
        p=0.1   #p_gain
        e = p * (data_l - target)
        motor_r = motor - e
        motor_l = motor + e
        raw_control(motor_l,motor_r)

    def turn_right(self):
        pos_control(0,0,0.1)
        pos_control(450,-450,0.5)

if __name__=='__main__':
    rospy.init_node("raspimouse")

    rp = RP()
    print switch_motors(True)
    print rp.p
    target = 700
    motor = 500
    raw_control(motor,motor)
    while not rospy.is_shutdown():
	try:
            t=threading.Timer(0.1,LightSensorValues)
            t.start()
            time.sleep(0.1)
            t.cancel()

	    data_l = rp.get_left_lightsensor()
            data_f = rp.get_forward_lightsensor()

            if data_f >= 2000:
                rp.turn_right()
                continue

            rp.left_walltrace()
	except rospy.ROSInterruptException:
	    pass
    raw_control(0,0)
    print "stop now : raw_control(0,0)"
