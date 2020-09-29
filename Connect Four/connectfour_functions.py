#connectfour_functions.py

import connectfour

def print_board(game_state):
	'''Prints out the board for user to see given current state of the game'''
	for c in range(1, connectfour.BOARD_COLUMNS+1):
		print(c, end=' ')

	for r in range(connectfour.BOARD_ROWS):
		print()
		for c in range(connectfour.BOARD_COLUMNS):
			if game_state.board[c][r] == 0:
				print('.', end=' ')
			else:
				if game_state.board[c][r] == 1:
					print('R', end = ' ')
				if game_state.board[c][r] == 2:
					print('Y', end = ' ')
	print()

def choose_column() -> int:
	'''Asks user for a column number input; if not an integer between 1 and 7, asks user for input again'''
	while True:
		column_num = input('Pick a column from 1 to 7: ')
		try:
			column_num = int(column_num)
		except:
			print('Invalid input, please enter an integer between 1 and 7.')
		else:
			if column_num < 1 or column_num > connectfour.BOARD_COLUMNS:
				print('Invalid input, please enter a number between 1 and 7.')
			else:
				return column_num

def choose_move() -> str:
	'''Asks user to enter a move type; if invalid, asks user again'''
	while True:
		print('Do you want to drop or pop?')
		move = input().strip()
		if move.lower() == 'drop' or move.lower() == 'pop':
			return move.lower()
		else:
			print('Invalid input, please enter drop or pop.')

def execute_move(move: str, column_num: int, game_state: connectfour.GameState) -> connectfour.GameState:
	'''Calls drop or pop function from connectfour depending on user input; if invalid or if game is over, tells that to user. 
	Returns updated game state.'''
	try:
		if move == 'drop' or move == 'DROP':
			game_state = connectfour.drop(game_state, column_num-1)
		if move == 'pop' or move == 'POP':
			game_state = connectfour.pop(game_state, column_num-1)
	except connectfour.InvalidMoveError:
		print('That move is invalid. Please try again.')
	except connectfour.GameOverError:
		print('Sorry, the game is over!')
	finally:
		return game_state

