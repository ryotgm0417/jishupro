#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import string
import time
import math
import numpy as np

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


# Gyro
ROLL_OFFSET = 3.2
PITCH_OFFSET = -1.7
YAW_OFFSET = 0.3
INTERVAL = 0.1

light_position = [1.0, 1.0, 1.0, 0.0]
light_ambient = [0.4, 0.4, 0.4, 1.0]
light_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_default_color = [1.0, 1.0, 1.0, 1.0]
mat_default_specular = [1.0, 1.0, 1.0, 1.0]
mat_default_shininess = [100.0]
mat_default_emission = [0.0, 0.0, 0.0, 0.0]

size = 0.5


def callback(msg):
    global mpu_data, prev_data, pressed, released
    message = msg.data
    pressed = "P" in message    # True when switch is pressed
    released = "R" in message   # True when switch is released
    message = message.translate(string.maketrans('',''), ' PR')  # removes characters {space, R, P} from string
    for ele in message.split(';'):
        ele = ele.split(',')
        if len(ele) == 7:
            mpu_data = [float(x) for x in ele[:-1]]


def calculate_angles(dt=INTERVAL):
    global angles

    if pressed:
        angles = np.zeros(3)
    else:
        d_rpy = np.array([mpu_data[3] - ROLL_OFFSET,
                          -(mpu_data[4] - PITCH_OFFSET),
                          -(mpu_data[5] - YAW_OFFSET)])*dt
        s = np.sin(angles*np.pi/180.)
        c = np.cos(angles*np.pi/180.)
        t = np.tan(angles*np.pi/180.)
        Q = np.array([[1, c[0]*t[2], s[0]*t[2]],
                      [0, c[0]/c[2], s[0]/c[2]],
                      [0, -s[0], c[0]]])

        angles = angles + np.matmul(Q,d_rpy)

        # スイッチが上を向いている時は mpu_data[1], mpu_data[2] の値が小さくなるため angles[0] を正確に計算できない。
        angles[0] = math.atan2(mpu_data[1], mpu_data[2])*180/np.pi
        angles[1] = math.atan2(mpu_data[0], (mpu_data[1]**2 + mpu_data[2]**2)**0.5)*180/np.pi

    for i in range(3):
        if angles[i] > 360:
            angles[i] -= 360
        elif angles[i] < -360:
            angles[i] += 360


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # gluLookAt(0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glPushMatrix()

    color = [1.0, 0.0, 1.0, 1.0]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    glRotatef(angles[2], 0., 1., 0.)
    glRotatef(angles[1], 0., 0., -1.)
    glRotatef(angles[0], 1., 0., 0.)


    glutSolidTeapot(size)

    glPopMatrix()
    glutSwapBuffers()


if __name__ == "__main__":
    mpu_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # most recent data from accelerometer
    prev_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    pressed = False
    released = False

    angles = np.zeros(3)

    rospy.init_node('mouse_operation')
    rospy.Subscriber('sensor_data', String, callback)

    #### GL initialization ####
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
    glutInitWindowSize(500, 500)
    window = glutCreateWindow("Teapot")

    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LESS )
    glShadeModel (GL_SMOOTH)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_ambient)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_default_color)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_default_color)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_default_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_default_shininess)

    glutDisplayFunc(display)
    glutIdleFunc(display)
    #glutMainLoop()

    try:
        while not rospy.is_shutdown():
            if prev_data != mpu_data:
                # acc_abs = (mpu_data[0]**2 + mpu_data[1]**2 + mpu_data[2]**2)**0.5
                # print(mpu_data[1], acc_abs)

                for i in range(4):
                    calculate_angles(INTERVAL/4.)
                    print(angles)

                    #### GL loop, draw object ####
                    glutPostRedisplay()
                    glutMainLoopEvent()

                prev_data = mpu_data


    except rospy.ROSInterruptException:
        pass
