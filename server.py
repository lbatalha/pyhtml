#!/usr/bin/python3

import os
import sys
import socket
import mimetypes
import _thread
import http.client
import time
import urllib

def respond(conn, status_code, file_request = None):
	
	if not file_request:
		file_request = str(status_code)+".html"

	http_mime = mimetypes.guess_type(file_request, strict = True)
	encoding = str(http_mime[1])
	mime = str(http_mime[0])

	http_status_code = str(status_code) + " " + http.client.responses[status_code]
	http_ver = "HTTP/1.1 "

	with open(file_request, 'rb') as fo:
		content = fo.read()
	
	length_content = str(len(content))

	header = 	http_ver + http_status_code + \
				"\nContent-Type: " + mime + "; encoding=" + encoding + \
				"\nContent-Length: " + length_content + \
				"\n\n"

	#try:
	conn.sendall(bytes(header, 'utf-8') + content)
	#except:
		#return -1
	return status_code

def client_connection(conn,):
	
	status = 0
	print("start thread\n")	
	data = b''
	while True:
		chunk = conn.recv(1024)
		if chunk == b'':
			print("socket returned empty\n")
			break
		data = data + chunk
		if data[-4:] == b'\r\n\r\n':
			break
		
	print("\n----\n")
	input_string = data.decode()
	input_list = input_string.split()
	print(input_string)
	
	try:
		req = input_list[0]
		fname = input_list[1]
	except Exception as e:
		print (e)
		req, fname = None

	if req == 'GET':
		if fname == '/':
			file_request = 'index.html'
		elif not fname:
			status = respond(conn, 400)
		elif fname:
			file_request = "." + os.path.abspath(urllib.parse.unquote_plus(fname))
			print('Requested ' + file_request)	#debug
			if not os.path.isfile(file_request):
				status = respond(conn, 404)
	else:
		status = respond(conn, 400)
	
	if not status:
		status = respond(conn, 200, file_request)
	conn.close()
	return 0

def main():
	
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


###########################################################################
###########################################################################






main()
