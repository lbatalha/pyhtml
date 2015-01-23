#!/usr/bin/python3

import os
import sys
import socket
import mimetypes
import _thread
import http.client



def respond(status_code, file_request = None):
	
	if not file_request:
		file_request = str(status_code)+".html"
	
	http_mime = mimetypes.guess_type(file_request, strict = True)	
	encoding = str(http_mime[1])
	mime = str(http_mime[0])

	http_status_code = str(status_code) + " " + http.client.responses[status_code] + "\n"
	http_ver = "HTTP/1.1 "


	header = http_ver +  http_status_code + "Content-Type: " + mime + "; encoding=" + encoding + "\n\n"

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
			fname = input_list[1]
		except:
			fname = None

		if input_list[0] == 'GET':
			if fname == '/':
				file_request = 'index.html'
			elif not fname:
				respond(400)
				break
			elif fname:
				file_request =  fname[1:]
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
