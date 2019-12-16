#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bluetooth
import time
import rospy
from std_msgs.msg import String

size = 128
address = "98:D3:31:FD:5D:81"
port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((address, port))
time.sleep(5)
msg = ""

rospy.init_node('data_publisher')
pub = rospy.Publisher('sensor_data', String, queue_size=1)

while True:
    data = sock.recv(size)
    msg = msg + data
    if data.find(";") != -1:
         # print(msg)
         pub.publish(msg)
         msg = ""

sock.close()
