#connectfour_network_userinterface.py

import connectfour
import connectfour_network
import connectfour_functions

def user_interface():
	'''Main function of AI Game'''
	connection = establish_connection()

	welcome(connection)
	start_AI(connection) #READY
	execute_game(connection)
	connectfour_network.close(connection)

def establish_connection() -> 'connection':
	'''Reads the host and port input from user. Tries to connect to server; 
	if unsuccessful, tells user and terminates program.'''
	host = connectfour_network.read_host()
	port = connectfour_network.read_port()
	try:
		connection = connectfour_network.connect(host, port)
		return connection
	except:
		print('Unable to establish connection')
		quit()
 

def welcome(connection: 'connection'):
	'''Gets the username from user. Sends Hello message to server, 
	calling a function that returns the server message.'''
	username = _get_username()
	server_response = connectfour_network.welcome_message(connection, username)
	print(server_response)

def start_AI(connection: 'connection'):
	'''Send an AI Game request to server and prints the server response.'''
	server_response = connectfour_network.request_AI_game(connection)
	print(server_response)

def execute_game(connection: 'connection'):
	'''Execution block of the network version of Connect Four game. 
	Takes turns between user and server until server detects a winner.'''
	game_state = connectfour.new_game()
	connectfour_functions.print_board(game_state)
	print()
	winner = connectfour.NONE
	server_response = ''

	while (winner == connectfour.NONE):
		game_over = check_game_over(server_response)
		if game_over == True:
			break
		if game_state.turn == connectfour.RED:
			print('It is Red Player\'s turn')
			game_state = user(connection, game_state)
			server_response = connectfour_network.receive_response(connection)
		if game_state.turn == connectfour.YELLOW:
			while server_response != 'OKAY':
				server_response = connectfour_network.receive_response(connection)
			print('It is Yellow Player\'s turn')
			game_state = server(connection, game_state)
			server_response = connectfour_network.receive_response(connection) #OKAY or READY

		connectfour_functions.print_board(game_state)

def check_game_over(server_response: str) -> bool:
	'''Determines if the game is over based on if the server detects a winner.'''
	if server_response == 'WINNER_RED':
		print('Congrats! Player 1 (Red Player) has won!')
		return True
	if server_response == 'WINNER_YELLOW':
		print('Congrats! Player 2 (Yellow Player) has won!')
		return True

def user(connection: 'connection', game_state: connectfour.GameState) -> connectfour.GameState:
	'''Allows user to choose column and move, then execute the move, send that to the server, and update game state.'''
	column = connectfour_functions.choose_column()
	move = connectfour_functions.choose_move()
	game_state = connectfour_functions.execute_move(move, column, game_state)
	connectfour_network.send_message(connection, _return_turn(column, move))
	return game_state

def server(connection: 'connection', game_state: connectfour.GameState) -> connectfour.GameState:
	'''Retrieves a response from the server indicating the column and move. Executes that move and updates game state.'''
	response = connectfour_network.receive_response(connection)
	print(response)
	column = int(response[-1].strip())
	move = response[0:4].strip()
	return connectfour_functions.execute_move(move, column, game_state)

#private functions

def _get_username():
	'''Asks the user for a username repeatedly until given a nonempty string with no spaces.'''
	while True:
		username = input('Username: ').strip()
		if len(username.strip()) < 1:
			print('That username is blank, please try again')
		elif ' ' in username.strip():
			print('You cannot have spaces in username. Please try again.')
		else:
			return username

def _return_turn(column: int, move: str):
	'''Returns the move and column in a format that the server can read.'''
	return move.upper() + ' ' + str(column)


if __name__ == '__main__':
	user_interface()
