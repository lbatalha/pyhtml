#!/usr/bin/python3

import os
import sys
import socket
import mimetypes
import _thread
import http.client

http_ver = "HTTP/1.1"

def respond(status_code, file_request = None):
	
	http_status_code = str(status_code) + " " + http.client.responses[status_code] + "\n"
	http_mime = mimetypes.guess_type(file_request, strict = True)
	http_ver = "HTTP/1.1 "
	encoding = str(http_mime[1])
	mime = str(http_mime[0])

	header = http_ver +  http_status_code + "Content Type: " + mime + "; encoding=" + encoding + "\n"

	if file_request == None or mime.split('/') == 'text':
		with open(file_request, 'r') as fo:
			content = bytes(fo.read(), encoding)
	else:
		with open(file_request, 'rb') as fo:
			content = fo.read()
	
	
	try:
		conn.sendall(bytes(header, 'utf-8') + content)
	except:
		return -1
	return 0

def client_connection(conn):
	while True:
		data = conn.recv(1024)
		if not data: break

		input_string = data.decode()
		input_list = input_string.split()
		try:
			fr = input_list[1]
		except:
			fr = None

		if input_list[0] == 'GET':
			if fr == '/':
				file_request = './index.html'
			elif not fr:
				respond(400)
				break
			elif fr != None:
				file_request =  fr[1:]
				if not os.path.isfile(file_request):
					respond(404)
					break
				print('Requested ' + file_request)
		else:
			respond(400)
			break
	
		respond(200, file_request)
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


# Content-Type: text/html; encoding=UTF-8
# Content-Length: 258
