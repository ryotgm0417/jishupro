#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui as gui
import rospy
from std_msgs.msg import String
import string
import time

# Mouse
ACC_THRESHOLD = 2.
SENSITIVITY = 1.


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
    global v_x, v_y
    acc_x = mpu_data[0]
    acc_y = mpu_data[1]

    if acc_x**2 + acc_y**2 < ACC_THRESHOLD:
        v_x = 0
        v_y = 0
    else:
        v_x += acc_x * SENSITIVITY
        v_y -= acc_y * SENSITIVITY
        x, y = gui.position()
        gui.moveTo(x + v_x, y + v_y, duration = 0.1)


if __name__ == "__main__":
    mpu_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # most recent data from accelerometer
    pressed = False
    released = False

    v_x = 0
    v_y = 0

    screenWidth, screenHeight = gui.size()

    rospy.init_node('mouse_operation')
    rospy.Subscriber('sensor_data', String, callback)

    try:
        while not rospy.is_shutdown():
            print(mpu_data, pressed, released)
            check_click()
            mouse_movement()

    except rospy.ROSInterruptException:
        pass
