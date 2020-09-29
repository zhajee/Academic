#connectfour_console.py

import connectfour
import connectfour_functions

def play_connect_four():
	'''Main function of console version of the Connect Four game. 
	Loops through checking player turn, choosing column and move, 
	updating the game state, printing the board for each turn
	until there is a winner.'''

	game_state = start_game()
	winner = connectfour.NONE

	while (winner == connectfour.NONE):
		check_turn(game_state)
		column_num = connectfour_functions.choose_column()
		move = connectfour_functions.choose_move()
		game_state = connectfour_functions.execute_move(move, column_num, game_state)
		connectfour_functions.print_board(game_state)
		winner = connectfour.winner(game_state)

	check_winner(winner)

def start_game() -> connectfour.GameState:
	'''Prints Welcome message. Starts a new game. Prints board.'''
	print('Welcome to Connect Four!')
	game_state = connectfour.new_game()
	connectfour_functions.print_board(game_state)
	return game_state

def check_turn(game_state: connectfour.GameState):
	'''Prints the player's turn based on the turn field of gamestate'''
	if game_state.turn == connectfour.RED:
		print('It is Player 1\'s (Red Player\'s) turn')
	if game_state.turn == connectfour.YELLOW:
		print('It is Player 2\'s (Yellow Player\'s) turn')

def check_winner(winner: str): 
	'''Prints a congratulatory message based on the winner that is passed as a paramater'''
	if winner == connectfour.RED:
		print('Congrats! Player 1 (Red Player) has won!')
	if winner == connectfour.YELLOW:
		print('Congrats! Player 2 (Yellow Player) has won!')

if __name__ == '__main__':
	play_connect_four()
