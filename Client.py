import json
import socket
import sys
import time



# get the hostname

host = '127.0.0.1'
port = 500
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    print('polaczono')
    # QMessageBox.warning(self, "Connection", "Connection made")

    while True:
        message = 'Hellow'
        s.send(message.encode())

        # time.sleep(5)
        total_str = ''
        try:
            data = s.recv(5000)
            total_str += data.decode('utf-8')
            print(total_str)
        except:
            break

        # print(total_str)
except:
    print("Failed to connect with {}:{}".format(host, port))


