import json
import socket
import sys
import time

from modules import *


with open('sample.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

# get the hostname
host = '0.0.0.0'
port = 500  # initiate port no above 1024




# def server_program():
# get the hostname
host = "127.0.0.1"
port = 500  # initiate port no above 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (host, port)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
Message = ['Otrzymano ustawienia urządzenia', 'Ustawiono ustawienia', 'parametry ramki', 'ramka danych']
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        total_str = ''
        t = 0
        while True:
            ind = 0 if t == 0 else 2
            print('odbieram')
            print(Message[ind])
            data = connection.recv(1024)
            if data:
                total_str += data.decode('utf-8')
            else:
                print(total_str)
                print('no more data from', client_address)
            print(data.decode())
            if ind == 0:
                data = Message[1]
                print('wysyłam')
                print(data)
                connection.sendall(data.encode())
            else:
                data = json.dumps(json_object)
                # data = Message[1]
                print('wysyłam')
                print(data)
                connection.sendall(data.encode())
            time.sleep(15)
            t += 1


    finally:
        # Clean up the connection
        connection.close()
# if __name__ == '__main__':
#     server_program()
