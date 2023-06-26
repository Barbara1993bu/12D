import json
import socket
import sys
from modules import *


with open('sample.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

# get the hostname
host = '0.0.0.0'
port = 500  # initiate port no above 1024

server_socket = socket.socket()  # get instance
# look closely. The bind() function takes tuple as argument
server_socket.bind((host, port))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(10)
conn, address = server_socket.accept()  # accept new connection
print("Connection from: " + str(address))
# VV = vhex(np.array(DFs['voltages_P'], dtype=int)).tolist()
while True:
    # receive data stream. it won't accept data packet greater than 1024 bytes
    data = conn.recv(4096).decode()
    if not data:
        # if data is not received break
        break
    print("from connected user: " + str(data))
    # data = VV

    message = json.dumps(json_object)
    conn.sendall(message.encode('utf-8'))  # send data to the client
    data = conn.recv(4096).decode()
    print("from connected user: " + str(data))
    message = json.dumps(json_object)  # send data to the client
    conn.sendall(message.encode('utf-8'))


conn.close()  # close the connection
