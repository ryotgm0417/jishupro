#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui as gui
import rospy
from std_msgs.msg import String
import string
import time

# Mouse
ROLL_OFFSET = 3
PITCH_OFFSET = -2
X_SENS = 2
Y_SENS = 2
RP_THRESHOLD = 20
SHAKE_THRESHOLD = 200


def callback(msg):
    global mpu_data, prev_data, pressed, released
    message = msg.data
    pressed = "P" in message    # True when switch is pressed
    released = "R" in message   # True when switch is released
    message = message.translate(string.maketrans('',''), ' PR')  # removes characters {space, R, P} from string
    for ele in message.split(';'):
        ele = ele.split(',')
        if(len(ele) == 7):
            mpu_data = [float(x) for x in ele[:-1]]


def check_click():
    if pressed == True:
        gui.click()


def mouse_movement():
    if (mpu_data[0]**2 + mpu_data[1]**2 + mpu_data[2]**2)**0.5 > SHAKE_THRESHOLD:
        gui.moveTo(screenWidth/2, screenHeight/2)
        time.sleep(1)
        return 0

    roll = mpu_data[3] - ROLL_OFFSET
    pitch = mpu_data[4] - PITCH_OFFSET

    if roll**2 + pitch**2 > RP_THRESHOLD:
        x, y = gui.position()
        gui.moveTo(x-X_SENS*roll, y+Y_SENS*pitch, duration=0.1)
    else:
        time.sleep(0.1)


if __name__ == "__main__":
    mpu_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # most recent data from accelerometer
    prev_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    pressed = False
    released = False

    screenWidth, screenHeight = gui.size()
    gui.moveTo(screenWidth / 2, screenHeight / 2)

    rospy.init_node('mouse_operation')
    rospy.Subscriber('sensor_data', String, callback)

    try:
        while not rospy.is_shutdown():
            if prev_data != mpu_data:
                print(mpu_data, pressed, released)
                check_click()
                mouse_movement()
                prev_data = mpu_data

    except rospy.ROSInterruptException:
        pass
