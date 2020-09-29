#project4.py
import project4_mechanics

def run_game():
	'''Gets user input and begins the game'''
	rows = int(input())
	columns = int(input())
	state = project4_mechanics.ColumnsState(rows, columns)

	inside_field = input().upper().strip()

	if inside_field == 'CONTENTS':
		contents(inside_field, rows, columns, state)

	#continues to check if the faller is active inside of the field;
	#if the faller lands outside of the field, GAME over is called.
	while state.start_game():
		print_field(state)
		command = input()
		if command == '':
			if state.check_in_field():
				print_field(state)
				print('GAME OVER')
				break
		elif command == 'Q':
			state.end_game()
		else:
			receive_commands(command, state)

def contents(inside_field: str, rows: int, columns: int, state: project4_mechanics.ColumnsState):
	'''Gets contents of field from user and sends it as a list to the 
	game mechanics module'''
	list_of_rows = []

	for row in range(rows):
		row_contents = []
		line = input() #example: Y X
		for i in range(columns):
			row_contents.append(line[i]) #example: [_, Y, _, X]
		list_of_rows.append(row_contents)

	state.create_field(list_of_rows)

def receive_commands(command: str, state: project4_mechanics.ColumnsState) -> None:
	'''Based on user commands, calls appropriate methods from the 
	game mechanics module'''
	if command[0] == 'F':
		line = command.split(' ')
		column_number = int(line[1])
		faller_info = (line[4], line[3], line[2])
		state.create_faller(column_number, faller_info)

	elif command == 'R':
		state.rotate_faller()
	elif command == '>':
		state.move_faller_right()
	elif command == '<':
		state.move_faller_left()


def print_field(state: project4_mechanics.ColumnsState) -> None:
	'''Displays the field using the number of rows and columns given
	by the user as well as the game state from the game mechanics module'''
	for row in range(state.return_rows()):
		print('|', end = '')
		for column in range(state.return_columns()):
			if state.get_state(row, column) == 'empty':
				print(' ' + ' ' + ' ', end='')
			if state.get_state(row, column) == 'frozen':
				print(' ' + state.get_letter(row, column) + ' ', end='')
			if state.get_state(row, column) == 'falling':
				print('[' + state.get_letter(row, column) + ']', end='')
			if state.get_state(row, column) == 'landed':
				print('|' + state.get_letter(row, column) + '|', end='')
			if state.get_state(row, column) == 'matched':
				print('*' + state.get_letter(row, column) + '*', end='')
		print('|')
	print(' ', end = '')
	for column in range(state.return_columns()):
		print('---', end = '')
	print(' ')

if __name__ == '__main__':
	run_game()
