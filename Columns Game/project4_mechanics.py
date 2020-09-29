#Zoya Hajee; ID: 40043145

#project4_mechanics.py

#states:
#empty
#falling
#landed
#frozen
#matched
class NonexistentColumn(Exception):
	def __init__(self):
		Exception.__init__(self, "Non-existent column number")

class ColumnsState():

	def __init__(self, rows: int, columns: int):
		self._running = True
		self.rows = rows
		self.columns = columns
		self.faller = Faller()
		self.current_letters = []
		self.current_states = []

		#list of lists data structure to keep track of the contents and state of field separately
		for row in range(rows):
			letters_row = []
			states_row = []
			for col in range(columns):
				letters_row.append(' ')
				states_row.append('empty')
			self.current_letters.append(letters_row)
			self.current_states.append(states_row)


	def start_game(self):
		'''Returns the running attribute, which is set to true'''
		return self._running

	def end_game(self) -> None:
		'''Ends game by setting running attribute to False'''
		self._running = False

	def return_rows(self) -> int:
		'''Returns the number of rows in this field'''
		return self.rows

	def return_columns(self) -> int:
		'''Returns the number of columns in this field'''
		return self.columns

	def create_field(self, list_of_rows: [[str]]) -> None:
		'''Applies given letters to the appropriate locations.
		Completes matching and eliminating matches/moving letters to the spaces below.'''

		for row in range(self.return_rows()):
			for column in range(self.return_columns()):
				letter = list_of_rows[row][column]
				if letter == ' ':
					self.set_letter(row, column, ' ')
					self.set_state(row, column, 'empty')
				else:
					self.set_letter(row, column, letter)
					self.set_state(row, column, 'frozen')

		self.fill_space_below()
		self.all_matching()

	def create_faller(self, column_number: int, faller_info: tuple) -> None:
		'''Creates a faller based on the letters given by the user in the given column
		faller_info[0] is the first faller block'''
		if column_number < 0 or column_number > self.return_columns():
			raise NonexistentColumn()
		if self.faller.is_faller == True:
			return

		self.faller.is_faller = True
		self.faller.faller_info = faller_info
		self.faller.set_row(0)
		self.faller.set_column(column_number-1)

		self.set_letter(self.faller.return_row(), self.faller.return_column(), self.faller.faller_info[0])
		self.faller.state = 'falling'
		self.set_state(self.faller.return_row(), self.faller.return_column(), 'falling')
		self.change_state()

	def move_faller_down(self) -> None:
		'''Moves each block if the faller down depending on whether the block is in the field or not.
		If the block is not in the field, sets the cell above it to that block's value.'''

		if self._check_below(self.faller.return_row(), self.faller.return_column()):
			return #don't move down if occupied or bottom of field below this letter

		self.move_faller(self.faller.return_row(), self.faller.return_column(), 'down') 

		if self.faller.return_row() - 1 >= 0:
			self.move_faller(self.faller.return_row() -1, self.faller.return_column(), 'down') 
			if self.faller.return_row() - 2 >= 0:
				self.move_faller(self.faller.return_row() - 2, self.faller.return_column(), 'down') 

		self.faller.set_row(self.faller.return_row() + 1)

	def move_faller(self, row: int, column: int, direction: str) -> None:
		'''Takes current row and column, finds value of that cell, empties cell,
		and fills new cell with that value.'''

		value = self.current_letters[row][column]
		state = self.current_states[row][column]
		self.current_letters[row][column] = ' '
		self.current_states[row][column] = 'empty'

		if direction == 'down':
			self.current_letters[row+1][column] = value
			self.current_states[row+1][column] = state
		elif direction == 'right':
			self.current_letters[row][column+1] = value
			self.current_states[row][column+1] = state
		else: #Left
			self.current_letters[row][column-1] = value 
			self.current_states[row][column-1] = state

	def set_letter(self, row: int, column: int, value: str) -> None:
		'''Takes given row, column and sets given value into that position'''

		self.current_letters[row][column] = value

	def set_state(self, row: int, column: int, state: str) -> None:
		'''Takes given row, column, and sets given state into that position'''
		self.current_states[row][column] = state

	def get_letter(self, row:int, column: int) -> str:
		'''returns a string declaring the letter at the given position'''

		return self.current_letters[row][column]

	def get_state(self, row: int, column: int) -> str:
		'''returns a string saying if the cell is empty, falling, landed, frozen, or matched.'''

		return self.current_states[row][column]

	def change_state(self) -> None:
		'''Changes state of the faller based on its position in the field.'''

		if self._check_below(self.faller.return_row(), self.faller.return_column()):
			self.faller.state = 'landed'
			self.current_states[self.faller.return_row()][self.faller.return_column()] = 'landed'
		else: 
			self.faller.state = 'falling'
			self.current_states[self.faller.return_row()][self.faller.return_column()] = 'falling'

		self.set_faller_cells()

	def set_faller_cells(self) -> None:
		'''Sets the letter and state of each block of the active faller'''
		for i in range(3):
			if self.faller.return_row() - i < 0:
				return
			self.set_letter(self.faller.return_row() - i, self.faller.return_column(), self.faller.faller_info[i])
			self.set_state(self.faller.return_row() - i, self.faller.return_column(), self.faller.state)

	def check_in_field(self) -> None:
		'''If faller present and in the field, it falls. If landed faller, it freezes.
		If faller lands but is outside the field, returns True. Matching occurs if applicable.'''

		faller_landed_out_field = False
		if self.faller.is_faller == True:
			if self.current_states[self.faller.return_row()][self.faller.return_column()] == 'landed':
				self.change_state()
				if self.faller.return_row() - 2 < 0:
					faller_landed_out_field = True

				for i in range(3):
					self.set_state(self.faller.return_row() - i, self.faller.return_column(), 'frozen')
				self.faller.is_faller = False

				self.all_matching()
				return faller_landed_out_field

			self.move_faller_down()
			self.change_state()

		self.all_matching()
		return False

	def all_matching(self) -> None:
		'''First eliminates any matched letters, then proceeds to call each matching method.'''
		self._eliminate_matched()
		self._fill_space_below()
		self._matching_vertically()
		self._matching_horizontally()
		self._matching_diagonally()

	#OTHER COMMANDS:

	def move_faller_right(self) -> None:
		'''Checks if moving the faller right is a valid move. If it is, moves each block of the faller
		and updates the faller column and state.'''
		if not self.faller.is_faller:
			return

		if self._check_sides(self.faller.return_row(), self.faller.return_column(), 'right'):
			return


		for i in range(3):
			if self.faller.return_row() - i < 0:
				break

			if self.current_states[self.faller.return_row() - i][self.faller.return_column()+1] == 'frozen':
				return

			self.move_faller(self.faller.return_row() - i, self.faller.return_column(), 'right')

		self.faller.set_column(self.faller.return_column() + 1)

		self.change_state()

	def move_faller_left(self) -> None:
		'''Checks if moving the faller left is a valid move. If it is, moves each block of the faller
		and updates the faller column and state.'''
		if not self.faller.is_faller:
			return

		if self._check_sides(self.faller.return_row(), self.faller.return_column(), 'left'):
			return


		for i in range(3):
			if self.faller.return_row() - i < 0:
				break

			if self.current_states[self.faller.return_row() - i][self.faller.return_column()-1] == 'frozen':
				return

			self.move_faller(self.faller.return_row() - i, self.faller.return_column(), 'left')

		self.faller.set_column(self.faller.return_column() - 1)

		self.change_state()


	def rotate_faller(self) -> None:
		'''When called, moves sequence of faller blocks by one.'''
		if self.faller.is_faller:

			first_block = self.faller.faller_info[0]
			second_block = self.faller.faller_info[1]
			third_block = self.faller.faller_info[2]

			self.faller.faller_info = [second_block, third_block, first_block]
			self.set_faller_cells()
			self.change_state()

	#ALL MATCHING FUNCTIONS:

	def _matching_horizontally(self) -> None:
		'''If 3 or more letters along a row are the same, call method to change state to matched.'''
		for row in range(self.return_rows() - 1, -1, -1):
			matched = False
			match = 0
			previous_letter = ' '
			for column in range(0, self.return_columns()):

				matched = ((self.current_states[row][column] == 'frozen' or self.current_states[row][column] == 'matched') and self.current_letters[row][column] == previous_letter)
				
				if matched == True:
					match += 1

				if column == self.return_columns()-1:
					if match >= 3:
						if matched == True:
							self._recognize_horiz_match(row, column, match)
						else:
							self._recognize_horiz_match(row, column-1, match)
				elif not matched:
					if match >= 3:
						self._recognize_horiz_match(row, column-1, match)

					if self.current_states[row][column] == 'frozen' or self.current_states[row][column] == 'matched':
						previous_letter = self.current_letters[row][column]
						match = 1

					else:
						previous_letter = ' '
						match = 1


	def _matching_vertically(self) -> None:
		'''If 3 or more letters along a column are the same, called method to change state to matched.'''
		
		for column in range(0, self.return_columns()):
			matched = False
			match = 0
			previous_letter = ' '
			for row in range(self.return_rows() - 1, -1, -1):

				matched = ((self.current_states[row][column] == 'frozen' or self.current_states[row][column] == 'matched') and self.current_letters[row][column] == previous_letter)
				
				if matched == True:
					match += 1

				if column == self.return_columns()-1:
					if match >= 3:
						if matched == True:
							self._recognize_vertical_match(row, column, match)
						else:
							self._recognize_vertical_match(row + 1, column, match)
				elif not matched:
					if match >= 3:
						self._recognize_vertical_match(row + 1, column, match)

					if self.current_states[row][column] == 'frozen' or self.current_states[row][column] == 'matched':
						previous_letter = self.current_letters[row][column]
						match = 1

					else:
						previous_letter = ' '
						match = 1

	def _matching_diagonally(self) -> None:
		'''If 3 or more letters along a diagonal are the same, call method to change state to matched.'''
		for rowCounting in range(self.return_rows() - 1, -1, -1):
			for columnCounting in range(0, self.return_columns()):
				previous_letter = ' '
				match = 0
				matchLeft = 0
				countRow = 0
				countCol = 0
				while True:
					row = rowCounting - countRow
					columnRight = columnCounting + countCol
					columnLeft = columnCounting - countCol

					matchedRight = ((self.current_states[row][columnRight] == 'frozen' or self.current_states[row][columnRight] == 'matched') and self.current_letters[row][columnRight] == previous_letter)
					matchedLeft = ((self.current_states[row][columnLeft] == 'frozen' or self.current_states[row][columnLeft] == 'matched') and self.current_letters[row][columnLeft] == previous_letter)
					
					if matchedRight == True:
						match += 1

					if matchedLeft == True:
						matchLeft += 1

					if columnRight == self.return_columns()-1:
						if match >= 3:
							if matchedRight == True:
								self._recognize_diag_match(row, columnRight, match)
							else:
								self._recognize_diag_match(row + 1, columnRight-1, match)
					elif not matchedRight:
						if match >= 3:
							self._recognize_diag_match(row+1, columnRight-1, match)

						if self.current_states[row][columnRight] == 'frozen' or self.current_states[row][columnRight] == 'matched':
							previous_letter = self.current_letters[row][columnRight]
							match = 1

						else:
							previous_letter = ' '
							match = 1

					countRow += 1
					countCol += 1

					if rowCounting-countRow < 0:
						break
					if columnCounting+countCol >= self.return_columns():
						break


	def _recognize_horiz_match(self, row: int, column: int, number: int) -> None:
		'''Marks each element in loop as matched based on number of horizontal matches'''
		for c in range(column, column - number, -1):
			self.set_state(row, c, 'matched')

	def _recognize_vertical_match(self, row: int, column: int, number: int) -> None:
		'''Marks each element in loop as matched based on number of vertical matches'''
		for r in range(row, row + number):
			self.set_state(r, column, 'matched')

	def _recognize_diag_match(self, row: int, column: int, number: int) -> None:
		'''Marks each element in loop as matched based on number of diagonal matches'''
		for i in range(number):
			self.set_state(row + i, column - i, 'matched')

	def _eliminate_matched(self) -> None:

		'''If letters are marked as matched, they are eliminated and the method is called for the above letters to fill the space below them.'''

		for row in range(self.return_rows()):
			for column in range(self.return_columns()):
				if self.current_states[row][column] == 'matched':
					self.set_letter(row, column, ' ')
					self.set_state(row, column, 'empty')

	def _fill_space_below(self) -> None:
		'''Letters fill the space below them'''
		for column in range(self.return_columns()):
			for row in range(self.return_rows() - 1, -1, -1):
				if self.current_states[row][column] == 'falling' or self.current_states[row][column] == 'landed':
					continue
				if self.current_states[row][column] == 'frozen':
					if self._check_below(row, column) == False:
						self.move_faller(row, column, 'down')

	def _check_below(self, row: int, column: int) -> bool:
		'''Checks to see if the row below the given cell is frozen or if it reached ground level 
		and returns True if so.'''

		if row + 1 >= self.return_rows():
			return True

		if self.current_states[row + 1][column] == 'frozen':
			return True

		return False

	def _check_sides(self, row: int, column: int, direction: str) -> bool:
		'''Checks to see if the columns to the sides the given cell are edges of the field
		and returns True if so.'''
		if direction == 'right':
			if (self.faller.return_column() == self.return_columns() - 1): 			
				return True

		if direction == 'left':
			if (self.faller.return_column() == 0):
				return True


class Faller():

	def __init__(self):
		self.is_faller = False
		self.row = 0
		self.column = 0
		self.faller_info = ('', '', '')
		self.state = 'falling'

	def set_row(self, row: int) -> None:

		self.row = row

	def set_column(self, column_number: int) -> None:

		self.column = column_number


	def return_row(self) -> int:
		'''Returns the row this faller starts in'''

		return self.row

	def return_column(self) -> int:
		'''Returns the column this faller is in'''

		return self.column

