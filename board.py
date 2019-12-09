import pygame
import copy
import vector as v

import thing


class Location:

	def __init__(self, board, x, y):
		self.pos = v.Vector(x,y)
		self.board = board
		self.things = []

	def __iter__(self):
		for t in self.things:
			yield t

	def __getitem__(self, index):
		return self.things[index]
	def __setitem__(self, index, element):
		self.things[index] = element

	def __len__(self):
		return len(self.things)

	def add(self, *things):
		for t in things:
			t.loc = self
		self.things += things

	def remove(self, obj):
		self.things.remove(obj)

	def clear(self):
		for thing in self:
			self.remove(thing)
	remove_all = clear

	def get_sprites(self):
		for t in self:
			yield t.get_sprite()

	def is_passable(self):
		for t in self:
			if not t.passable:
				return False
		return True

	def interact(self, entity):
		for t in self:
			t.interact(entity)



	def step_on(self, entity):
		for t in self:
			t.step_on(entity)
	def bump(self, entity):
		for t in self:
			t.bump(entity)

	def has_tile(self):
		for t in self:
			if issubclass(type(t), thing.Tile):
				return True
		return False

	def get_moore_neighbourhood_tiles(self):
		return self.board.get_moore_neighbourhood_tiles(self.pos)

class Board:
	def __init__(self, save, size):
		self.save = save
		self.size = size # v.Vector(x,y)

		self.grid = [[Location(self,x,y) for x in range(self.width())] for y in range(self.height())]

		self.cell_size = v.Vector(32,32)

	def __iter__(self):
		for ln in self.grid:
			for loc in ln:
				yield loc

	def __getitem__(self, index): # index as Vector(x,y)
		return self.grid[index[1]][index[0]]
	def __setitem__(self, index, element):
		self.grid[index[1]][index[0]] = element

	# ~~~ ~~~ ~~~

	def copy(self):
		return copy.deepcopy(self)

	def correct_pointers(self):
		for loc in self:
			loc.board = self
			for t in loc:
				t.loc = loc

	def clear(self, pos):
		self[pos].clear()

	def add(self, thing_, pos):
		self[pos].add(thing_)
		if issubclass(type(thing_),thing.Controllable):
			self.save.set_control(thing_)

	def move(self, thing_, dest):
		self[thing_.get_pos()].remove(thing_)
		self[dest].add(thing_)

	def add_from_class(self, thing_class, pos): # a lil bit wonky, use with caution
		self.add(thing_class(), pos)

	def add_all(self, thing_class): # DEBUG: Should definitely NOT be used for anything else
		for loc in self:
			loc.add(thing_class())

	# ~~~ ~~~ ~~~

	def height(self): return self.size[1]
	def width(self): return self.size[0]

	def draw(self, surface, start=v.Vector(0,0)):
		sx, sy = self.save.control.loc.pos + v.Vector(-12, -10)
		ex, ey = self.save.control.loc.pos + v.Vector(12, 10)
		cx, cy = (0, 0)
		for x in range(sx, ex):
			if 0 <= x < self.width():
				for y in range(sy, ey):
					if 0 <= y < self.height():
						for thing in self[v.Vector(x,y)]:
							thing.draw(surface, start[0]+cx, start[1]+cy)
					cy += self.cell_size[1]
			cy = 0; cx += self.cell_size[0]

	# ~~~ ~~~ ~~~

	def get_moore_neighbourhood(self, pos):
		x, y = pos
		e = v.Vector
		return [
			[self[e(x-1,y-1)], self[e(x  ,y-1)], self[e(x+1,y-1)]],
			[self[e(x-1,y  )], self[e(x  ,y  )], self[e(x+1,y  )]],
			[self[e(x-1,y+1)], self[e(x  ,y+1)], self[e(x+1,y+1)]]
		]

	def get_moore_neighbourhood_tiles(self, pos):
		mn = self.get_moore_neighbourhood(pos)
		r = [[None for _ in range(3)] for _ in range(3)]
		for x in range(3):
			for y in range(3):
				r[x][y] = mn[x][y].has_tile()
		return r

	# ~~~ ~~~ ~~~

	def drop_player(self, player, pos):
		self[pos[0]][pos[1]].add_stuff(player)
		player.board = self; player.pos = pos