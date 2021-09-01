# send command
from command_1_utility import command_request
import socket

RECEIVER_ADDR = '192.168.0.15'
HOST_ADDR = '192.168.0.146'
PORT = 2000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST_ADDR, PORT))

s.listen(1)
conn, addr = s.accept()

print('Connection established with IRNSS reciever at:' + str(addr))

while True:
    if input('Do you want to continue? (y/n)\t').strip().lower() != 'y':
        break
    to_send = command_request()
    conn.send(to_send)
    print (to_send)

conn.close()
