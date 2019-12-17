#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui as gui
import rospy
from std_msgs.msg import String
import string
import time

def callback(msg):
    global mpu_data, pressed, released
    message = msg.data
    pressed = "P" in message    # True when switch is pressed
    released = "R" in message   # True when switch is released
    message = message.translate(string.maketrans('',''), ' PR')  # removes characters {space, R, P} from string
    for ele in message.split(';'):
        ele = ele.split(',')
        if(len(ele) == 7):
            mpu_data = [float(x) for x in ele[:-1]]


def check_click():
    if(pressed == True):
        gui.click()


def mouse_movement():
    x, y = gui.position()
    acc_x = mpu_data[0]
    acc_y = mpu_data[1]
    gui.moveTo(x + 10*acc_x, y + 10*acc_y)


if __name__ == "__main__":
    mpu_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # most recent data from accelerometer
    pressed = False
    released = False

    screenWidth, screenHeight = gui.size()

    rospy.init_node('mouse_operation')
    rospy.Subscriber('sensor_data', String, callback)

    try:
        while not rospy.is_shutdown():
            print(mpu_data, pressed, released)
            check_click()
            mouse_movement()
            time.sleep(0.1)

    except rospy.ROSInterruptException:
        pass
