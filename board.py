import pygame
import vector as v

import thing


class Location:
	def __init__(self, x, y):
		self.pos = v.Vector(x,y)
		self.things = []

	def __iter__(self):
		for thing in self.things:
			yield thing

	def add(self, *things):
		for t in things:
			if issubclass(type(t), thing.StorePos):
				t.pos = self.pos
		self.things += things

	def remove(self, obj):
		self.things.remove(obj)

	def get_sprites(self):
		for thing in self:
			yield thing.get_sprite()

	def is_passable(self):
		for thing in self:
			if not thing.passable:
				return False
		return True

class Board:
	def __init__(self, game, size):
		self.game = game
		self.size = size # vector

		self.grid = [[Location(x,y) for x in range(self.width())] for y in range(self.height())]

		self.cell_size = v.Vector(32,32)

	def __iter__(self):
		for ln in self.grid:
			for loc in ln:
				yield loc

	def __getitem__(self, index): # index is Vector(x,y)
		if type(index) is v.Vector:
			return self.grid[index[1]][index[0]]
		return self.grid[index]

	# ~~~ ~~~ ~~~

	def add(self, thing, pos):
		self[pos].add(thing)

	def move(self, obj, dest):
		#print(str(obj.pos)+" ==> "+str(dest))
		self[obj.pos].remove(obj)
		self[dest].add(obj)

	def add_from_class(self, thing_class, pos): # a lil bit wonky, use with caution
		self[pos].add(thing_class(self))

	def add_all(self, thing_class): # DEBUG: Should definitely NOT be used for anything else
		for loc in self:
			loc.add(thing_class(self))

	# ~~~ ~~~ ~~~

	def height(self): return self.size[1]
	def width(self): return self.size[0]

	def draw(self, surface, start=v.Vector(0,0)):
		sx, sy = self.game.control.pos + v.Vector(-12, -10)
		ex, ey = self.game.control.pos + v.Vector(12, 10)
		cx, cy = (0, 0)
		for x in range(sx, ex):
			if 0 <= x < self.width():
				for y in range(sy, ey):
					if 0 <= y < self.height():
						for sprite in self[y][x].get_sprites():
							surface.blit(sprite, (start[0]+cx, start[1]+cy))
					cy += self.cell_size[1]
			cy = 0; cx += self.cell_size[0]

	# ~~~ ~~~ ~~~

	def get_moore_neighbourhood(self, pos):
		y, x = pos
		return [
			[self[y-1][x-1], self[y-1][x], self[y-1][x+1]]
			[self[y]  [x-1], self[y]  [x], self[y]  [x+1]]
			[self[y+1][x-1], self[y+1][x], self[y+1][x+1]]
		]

	# ~~~ ~~~ ~~~

	def drop_player(self, player, pos):
		self[pos[0]][pos[1]].add_stuff(player)
		player.board = self; player.pos = pos