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
        p=0.1				 #p_gain  制御定数
        e = p * (data_l - target)	#制御量 = 制御定数 * (左側のセンサー値 - コース真ん中時の左側のセンサー値)
        motor_r = motor - e		#右モータの値(Hz) = 元のモータ値 - 制御量
        motor_l = motor + e		#左モータの値	　= 元のモータ値 + 制御量
        raw_control(motor_l,motor_r)

    def turn_right(self):		#約９０度右旋回
        pos_control(0,0,0.1)
        pos_control(450,-450,0.5)

if __name__=='__main__':
    rospy.init_node("raspimouse")

    rp = RP()
    print switch_motors(True)
    print rp.p
    target = 700			#コースの真ん中時の左センサの値
    motor = 500				#基本のモータの値
    raw_control(motor,motor)		#走り出しで必要
    while not rospy.is_shutdown():
	try:
            t=threading.Timer(0.1,LightSensorValues)	#light_sensorの計測を0.1秒ごとに
            t.start()
            time.sleep(0.1)				
            t.cancel()					#thread0.1秒後に止める

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
