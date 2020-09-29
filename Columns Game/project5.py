#Zoya Hajee, ID: 40043145

#project5.py

import project4_mechanics
import pygame
import random

_MARGIN = 1 #pixel
_ROWS = 13
_COLUMNS = 6
_FRAME_RATE = 10
_INITIAL_WIDTH = 300
_INITIAL_HEIGHT = 600
_BACKGROUND_COLOR = pygame.Color(0, 0, 0)


class ColumnsGame:

	def __init__(self):
		'''Creates the ColumnsGame class and initializes variables. Sets tick to the Frame Rate'''
		self._state = project4_mechanics.ColumnsState(_ROWS, _COLUMNS)
		rows = self._state.return_rows()
		cols = self._state.return_columns()
		self._faller_width = (_INITIAL_WIDTH-(cols+1))/cols #in pixels
		self._faller_height = (_INITIAL_HEIGHT-(rows+1))/rows #in pixels

		self._tick = _FRAME_RATE

	def run(self) -> None:
		'''Initiates Pygame. Displays the field. While running, calls the function that "ticks" the game mechanics.'''
		pygame.init()

		try:
			clock = pygame.time.Clock()

			self._create_field((_INITIAL_WIDTH, _INITIAL_HEIGHT))

			while self._state._running:
				clock.tick(_FRAME_RATE)
				self._handle_events()

				self._tick -= 1 
				#to allow the game to be paced at a reasonable time while keeping the field displays and handling key presses at a quicker pace
				if self._tick == 0:
					self._time_passage()
					self._tick = _FRAME_RATE
					
				self._draw_frame()
				

		finally:
			pygame.quit()

	def _create_field(self, size: (int, int)) -> None:
		'''Sets field size to given global size constants.'''
		self._field = pygame.display.set_mode(size, pygame.RESIZABLE)

	def _handle_events(self) -> None:
		'''Handles each event including key presses.'''
		for event in pygame.event.get():
			self._handle_event(event)

		self._handle_keys()

	def _handle_event(self, event) -> None:
		'''Handles quitting the game and resizing the field.'''
		if event.type == pygame.QUIT:
			self._stop_running()
		elif event.type == pygame.VIDEORESIZE:
			self._create_field(event.size)

	def _handle_keys(self) -> None:
		'''Handles left, right, and spacebar key presses by calling appropriate functions from game mechanics.'''
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			self._state.move_faller_left()

		if keys[pygame.K_RIGHT]:
			self._state.move_faller_right()

		if keys[pygame.K_SPACE]:
			self._state.rotate_faller()

	def _stop_running(self) -> None:
		'''If called, ends the game.'''
		self._state.end_game()

	def _draw_frame(self) -> None:
		'''Displays the field (including grid and fallers) and updates it.'''
		self._field.fill(_BACKGROUND_COLOR)
		self._draw_field() 
		pygame.display.flip()

	def _draw_field(self) -> None:
		'''Draws the grid of the game and each block of the faller.'''
		self._draw_grid()

		for row in range(self._state.return_rows()):
			for column in range(self._state.return_columns()):
				state = self._state.get_state(row, column)
				self._draw_blocks(column, row, state)

	def _draw_grid(self) -> None:
		'''Draws the grid with 1 pixel margin in between each square. Resizeable upon changing the height and width of screen.'''
		for col in range(self._state.return_columns()):
			for row in range(self._state.return_rows()):
				rect = pygame.Rect(_MARGIN + col*(self._faller_width + _MARGIN), _MARGIN + row*(self._faller_height + _MARGIN), self._faller_width, self._faller_height)
				pygame.draw.rect(self._field, pygame.color.Color(255, 255, 255), rect, 0)

	def _draw_blocks(self, column: int, row: int, state: str) -> None:
		'''Displays each block of the faller in its appropriate box on the grid. If the state is landed or matched, 
		displays a visual cue to the player.'''
		color = None
		w = self._faller_width
		h = self._faller_height
		left = _MARGIN + (column * (self._faller_width + _MARGIN))
		top = _MARGIN + (row * (self._faller_height + _MARGIN))
		rect = pygame.Rect(left, top, w, h)
		color = self._find_color(row, column)
		pygame.draw.rect(self._field, color, rect, 0)

		if self._state.get_state(row, column) == 'landed':
			color = pygame.Color(0, 0, 0)
			pygame.draw.rect(self._field, color, rect, 5)

		if self._state.get_state(row, column) == 'matched':
			color = pygame.Color(255, 0, 0)
			pygame.draw.rect(self._field, color, rect, 5)

	def _time_passage(self) -> None:
		'''Ticks the game mechanics. Creates a faller if not one currently present.'''
		if self._state.check_in_field():
			self._state._running = False
		if not self._state.check_in_field():
			if self._state.faller.is_faller == False:
				faller_info = random.sample(['S', 'T', 'V', 'W', 'X', 'Y', 'Z'], 3)
				column = random.randint(1, 6)
				self._state.create_faller(column, faller_info)

	def _find_color(self, row: int, column: int) -> 'pygame.Color':
		'''Returns a distinct color based on the letter of the block.'''
		color = pygame.Color(255, 255, 255)
		if self._state.get_letter(row, column) == 'S':
			color = pygame.Color(50, 168, 82)
		elif self._state.get_letter(row, column) == 'T':
			color = pygame.Color(199, 212, 61)
		elif self._state.get_letter(row, column) == 'V':
			color = pygame.Color(227, 158, 48)
		elif self._state.get_letter(row, column) == 'W':
			color = pygame.Color(217, 52, 43)
		elif self._state.get_letter(row, column) == 'X':
			color = pygame.Color(31, 196, 174)
		elif self._state.get_letter(row, column) == 'Y':
			color = pygame.Color(31, 46, 207)
		elif self._state.get_letter(row, column) == 'Z':
			color = pygame.Color(153, 29, 191)
		return color

if __name__ == '__main__':
    ColumnsGame().run()