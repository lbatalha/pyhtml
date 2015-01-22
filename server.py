#!/usr/bin/python


import os
import sys
import socket
import _thread

def client_connection(conn):
	while True:
		data = conn.recv(1024)
		if not data: break

		input_string = data.decode()
		input_list = input_string.split()

		if input_list[0] == 'GET':
			if input_list[1] == '/':
				file_request = './index.html'
			else:
				file_request = '.' + input_list[1]
				if os.path.isfile(file_request) != True:
					break
				print('Requested ' + file_request)
		else:
			conn.close()
			break
		
		with open(file_request, 'r') as fo:
			content = fo.read()
			message = "HTTP/1.1 200 OK\n\n" + content
			conn.sendall(bytes(message, 'UTF-8'))
			break;
	conn.close()

HOST = ''                 
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

while True:
	conn, addr = s.accept()
	print('Connected by', addr)
	_thread.start_new_thread(client_connection, (conn,))

s.close()


