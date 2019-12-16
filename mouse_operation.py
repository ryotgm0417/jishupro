#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui as gui
import rospy
from std_msgs.msg import String

def callback(msg):
    print(msg)

screenWidth, screenHeight = gui.size()

rospy.init_node('mouse_operation')
rospy.Subscriber('sensor_data', String, callback)
rospy.spin()
