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
	self.p = rospy.get_param('~p_gain', 0.1)
	rospy.on_shutdown(self.shutdown_hook)

    def lightsensor_callback(self, data):
        self.__lv = data

    def get_left_lightsensor(self):
        return(self.__lv.left_side)

    def get_right_lightsensor(self):
        return(self.__lv.right_side)

    def get_forward_lightsensor(self):
        return(self.__lv.left_forward + self.__lv.right_forward) * 0.5

    def shutdown_hook(self):
        print pos_control(0, 0, 0)
        print switch_motors(False)

    #def left_walltrace(self):
        #e = rp.p * (data_l - target) 
        #motor_l = motor + e
        #motor_r = motor - e


if __name__=='__main__':
    rospy.init_node("raspimouse")

    rp = RP()
    print switch_motors(True)
    print rp.p
    target = 950
    motor = 550
    turn = 0
    raw_control(motor, motor)

    while not rospy.is_shutdown():
	try:
            #thread
            t=threading.Timer(0.1,LightSensorValues)
            t.start()
            time.sleep(0.1)
            t.cancel()

            #lightsensors data
	    data_l = rp.get_left_lightsensor()
	    data_r = rp.get_right_lightsensor()
            data_f = rp.get_forward_lightsensor()

            #turn right
            if data_f >= 2000:
                #motor_r=-450
                #motor_l=450
                raw_control(450,-450)
                time.sleep(0.5)
                raw_control(0,0)
                time.sleep(0.1)
                #turn = turn + 1
                #if turn >= 8:
                #    break
                continue

            if data_l <= 90:
                turn = turn + 1
                if turn >= 8:
                    break
                while not rospy.is_shutdown():
                    k = threading.Timer(0.1, LightSensorValues)
                    k.start()
                    time.sleep(0.1)
                    k.cancel()
                    data_r = rp.get_right_lightsensor()
                    data_l = rp.get_left_lightsensor()
                    if data_l >= 700 or data_f >= 1000:
                        raw_control(0,0)
                        time.sleep(0.2)
                        raw_control(-450,450)
                        time.sleep(0.5)
                        break
                    e = rp.p * (target - data_r)
                    motor_r = motor - e
                    motor_l = motor + e
                    raw_control(motor_l, motor_r)

            #race left wall
	    e = rp.p*(data_l - target)# - (data_r - target))
	    motor_r = motor - e
	    motor_l = motor + e
            #rp.left_walltrace()
	    raw_control(motor_l, motor_r)
	    #rp.r.sleep()
	except rospy.ROSInterruptException:
	    pass
    raw_control(0,0)
    print "stop now : raw_control(0,0)"
