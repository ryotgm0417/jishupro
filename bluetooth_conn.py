import bluetooth
import time
import rospy

size = 128
address = "98:D3:31:FD:5D:81"
port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((address, port))
time.sleep(5)
msg = b""

rospy.init_node('active_mouse')
pub = rospy.Publisher('/data')


while True:
    data = sock.recv(size)
    msg = msg + data
    if data.find(b";") != -1:
         print(msg)
         msg = b""
         pub.publish(msg)

sock.close()
