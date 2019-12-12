import bluetooth
import time

size = 1024
address = "98:D3:31:FD:5D:81"
port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((address, port))
time.sleep(5)
start = time.time()
msg = b""

while True:
    data = sock.recv(size)
    if not data:
        break
    msg = msg + data
    if data.find(b";") != -1:
        end = time.time()
        print(data)
        print(end - start)
        msg = b""

    time.sleep(0.1)

sock.close()
