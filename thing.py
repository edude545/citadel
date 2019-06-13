import vector as v
import transform
from pygame.locals import *

import common


class Controllable:
	def handle_keydown_event(self, ev): pass
	def handle_keyup_event(self, ev): pass

class StorePos:
	pass


class Thing: # The class for a game object that inhabits a board, e.g. tiles, interactive objects, entities, and items.

	# Given attribute img, type pygame.Surface
	# Given attribute spritesheet, type pygame.Surface

	passable = True

	def __init__(self, board):
		self.board = board

	def get_sprite(self):
		return self.sprite
	def get_spritesheet(self):
		return self.spritesheet

	def getcv(self, name): # get class variable
		return getattr(self.__class__, name)


class Tile(Thing): # WIP - this class is *not* used yet

	passable = False

	def __init__(self, board):
		super().__init__(board)

	# ~~~ ~~~ ~~~

	def get_sprite(self):
		self.update_sprite_index()
		return self.spritesheet[self.sprite_index]

	def update_sprite_index(self):
		self.sprite_index=0;self.sprite_rotation=0;return
		m = self.get_moore_neighbourhood_tiles
		t=True;f=False
		_0 = [[t,t,t],[t,t,t],[t,t,t]]
		_0 = [[f,f,f],[t,t,t],[t,t,t]]
		_0 = [[f,f,f],[f,t,f],[f,f,f]]
		_0 = [[f,f,f],[f,t,f],[f,f,f]]
		_0 = [[f,f,f],[f,t,f],[f,f,f]]
		_0 = [[f,f,f],[f,t,f],[f,f,f]]
		_0 = [[f,f,f],[f,t,f],[f,f,f]]
		_0 = [[f,f,f],[f,t,f],[f,f,f]]
		_0 = [[f,f,f],[f,t,f],[f,f,f]]
		_0 = [[f,f,f],[f,t,f],[f,f,f]]

		if m == full: self.sprite_index = 0; self.sprite_rotation = 0
		elif m == [[f,f,f],[t,t,t],[f,f,f]]: self.sprite_index = 1; self.sprite_rotation = 0

	def get_moore_neighbourhood_tiles(self):
		mn = self.board.get_moore_neighbourhood(self.pos)
		r = [[None for _ in range(3)] for _ in range(3)]
		for y in range(3):
			for x in range(3):
				r[y][x] = issubclass(type(mn[y][x]), Tile)
		return r


class Entity(Thing, StorePos):

	def __init__(self, board):
		super().__init__(board)
		self.direction = 0

	def get_sprite(self):
		return self.get_spritesheet()[self.direction]

	def walk(self, direction, dist=1):
		self.direction = direction
		new = self.pos + common.direction_int_to_vector(self.direction) * dist
		if 0 <= new[0] < self.board.width() and 0 <= new[1] < self.board.height() and self.board[new].is_passable():
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