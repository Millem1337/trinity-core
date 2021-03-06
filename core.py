import socket
import json
import os
from urls import *

server_setting = None

with open('settings.json') as ss:
	server_settings = json.load(ss)

def parse_request(request):
	parsed = request.split(' ')
	if len(parsed) == 1:
		return
	method = parsed[0]
	url = parsed[1]

	return [method, url]

def generate_headers(method, url):
	if method != "GET":
		return ("HTTP/1.1 405 Method not allowed\n\n", 405)
	if not url in PAGES:
		return ('HTTP/1.1 404 Not found\n\n', 404)

	return ('HTTP/1.1 200 URL FOUND, Method ALLOWED\n\n', 200)

def generate_content(code, url):
	match code:
		case 404:
			return '<h1>404 Url not found</h1>'
		case 405:
			return '<h1>405 Method not allowed</h1>'
		case 200:
			return PAGES[url]

def generate_respone(request):
	method, url = parse_request(request)
	headers, code = generate_headers(method, url)
	body = generate_content(code, url)

	return (headers + body).encode()

def run_server():
	print('Server starting on:', os.name)
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((server_settings['ip'], server_settings['port']))
	server_socket.listen()

	while True:
		client_socket, addres = server_socket.accept()
		req = client_socket.recv(1024)
		print(req)
		print()
		print(addres)

		response = generate_respone(req.decode('utf-8'))

		client_socket.sendall(response)
		client_socket.close()

if __name__ == "__main__":
	run_server()
