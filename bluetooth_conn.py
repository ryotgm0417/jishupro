import bluetooth


address = "98:D3:31:FD:5D:81"
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

sock.connect((address, 1))

sock.send("AT")

sock.close()
