import vector as v
from pygame.locals import *

import common


class Controllable:
	def handle_keydown_event(self, ev): pass
	def handle_keyup_event(self, ev): pass

class StoresPos:
	pass


class Thing: # The class for a game object that inhabits a board, e.g. tiles, interactive objects, entities, and items.

	# Given attribute img, type pygame.Surface
	# Given attribute spritesheet, type pygame.Surface

	passable = True

	def __init__(self, board):
		self.board = board

	def get_sprite(self):
		return self.getcv("sprite")
	def get_spritesheet(self):
		return self.getcv("spritesheet")

	def getcv(self, name): # get class variable
		return getattr(self.__class__, name)


class Tile(Thing): # WIP - this class is *not* used yet

	def __init__(self, board, pos, spritesheet_path):
		super().__init__(board)
		self.pos = pos # Vector
		self.spritesheet = spritesheet
		self.sprite_index = 0
		self.update_texture()

	# ~~~ ~~~ ~~~

	def update_sprite_index(self):
		m = self.get_moore_neighbourhood_tiles
		t=True;f=False
		if t == [[f,f,f],[f,f,f],[f,f,f]]: self.sprite_index = 0
		elif t in ()

	def get_moore_neighbourhood_tiles(self):
		mn = self.board.get_moore_neighbourhood(self.pos)
		r = [[None for _ in range(3)] for _ in range(3)]
		for y in range(3):
			for x in range(3):
				r[y][x] = issubclass(type(mn[y][x]), Tile)
		return r


class Entity(Thing, StoresPos):

	def __init__(self, board):
		super().__init__(board)
		self.direction = 0

	def get_sprite(self):
		return self.get_spritesheet()[self.direction]

	def walk(self, direction, dist=1):
		self.direction = direction
		new = self.pos + common.direction_int_to_vector(self.direction)
		if self.board[new].is_passable():
			self.board.move(self, new)

class ControllableEntity(Entity, Controllable):

	def handle_keydown_event(self, ev):
		if ev.key is K_s:
			self.walk(0)
		elif ev.key is K_a:
			self.walk(1)
		elif ev.key is K_w:
			self.walk(2)
		elif ev.key is K_d:
			self.walk(3)