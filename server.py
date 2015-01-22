import os
import sys
import socket

HOST = ''                 
PORT = 8080

fo = open('index.html', 'r')
content = fo.read()
message = "HTTP/1.1 200 OK\n\n" + content

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while True:
	data = conn.recv(1024)
	if not data: break
	conn.sendall(bytes(message, 'UTF-8'))
conn.close()

