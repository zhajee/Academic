#connectfour_network.py

import socket

def read_host() -> str:
	'''Asks the user for a host until a nonempty input is given.'''

	while True:
	    host = input('Host: ').strip()

	    if host == '':
	        print('Please specify a host')
	    else:
	        return host

def read_port() -> int:
	'''Asks user for a port number until a valid input between 0 and 65535 is given.'''

	while True:
	    try:
	        port = int(input('Port: ').strip())

	        if port < 0 or port > 65535:
	            print('Ports must be an integer between 0 and 65535')
	        else:
	            return port

	    except ValueError:
	        print('Ports must be an integer between 0 and 65535')

def connect(host: str, port: int) -> 'connection':
	'''Connects to the server based on the given host and port. 
	Returns a connection object if successful and an exception is raised if unsuccessful.'''
	connectfour_socket = socket.socket()
	connectfour_socket.connect((host, port))

	connectfour_socket_input = connectfour_socket.makefile('r')
	connectfour_socket_output = connectfour_socket.makefile('w')

	return connectfour_socket, connectfour_socket_input, connectfour_socket_output

def send_message(connection: 'connection', message: str):
	'''Sends message to server'''
	connectfour_socket, connectfour_socket_input, connectfour_socket_output = connection
	connectfour_socket_output.write(message + '\r\n')
	connectfour_socket_output.flush()

def receive_response(connection: 'connection') -> str:
	'''Receives a response from server and returns that message'''

	connectfour_socket, connectfour_socket_input, connectfour_socket_output = connection

	return connectfour_socket_input.readline()[:-1]

def welcome_message(connection: 'connection', username: str) -> str:
	'''Sends HELLO message and username to server and returns a WELCOME message from server'''
	send_message(connection, 'I32CFSP_HELLO ' + username)
	return receive_response(connection)

def request_AI_game(connection: 'connection') -> str:
	'''Requests to play a game with AI. Sends AI_GAME and returns READY from server'''
	send_message(connection, 'AI_GAME')
	return receive_response(connection)

def close(connection: 'connection'):
	'''Closes the connection and its pseudo-files.'''
	connectfour_socket, connectfour_socket_input, connectfour_socket_output = connection

	connectfour_socket_input.close()
	connectfour_socket_output.close()
	connectfour_socket.close()
