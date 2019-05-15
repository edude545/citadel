import pygame
import vector as v

import thing


class Location:
	def __init__(self, x, y):
		self.pos = v.Vector(y,x)
		self.things = []

	def add(self, *things):
		for t in things:
			if issubclass(type(t), thing.StoresPos):
				t.pos = self.pos
		self.things += things

	def remove(self, obj):
		self.things.remove(obj)

	def get_sprites(self):
		return [thing.get_sprite() for thing in self.things]

	def is_passable(self):
		for thing in self.things:
			if not thing.getcv("passable"):
				return False
		return True

class Board:
	def __init__(self, game, size):
		self.game = game
		self.size = size # vector

		self.grid = [[Location(x,y) for x in range(self.width())] for y in range(self.height())]
		#self.rects = [[pygame.Rect((y,x), tuple(self.cell_size)) for x in range(self.width())] for y in range(self.height())]

		self.cell_size = v.Vector(32,32)

	def __iter__(self):
		for ln in self.grid:
			for loc in ln:
				yield loc

	def __getitem__(self, index):
		if type(index) is v.Vector:
			return self.grid[index[0]][index[1]]
		return self.grid[index]

	# ~~~ ~~~ ~~~

	def add(self, thing, pos):
		self[pos].add(thing)

	def move(self, obj, dest):
		#print(str(obj.pos)+" ==> "+str(dest))
		self[obj.pos].remove(obj)
		self[dest].add(obj)

	def add_from_class(self, thing_class, pos): # DEBUG: very wonky, probably shouldnt be used
		self[pos].add(thing_class(self))

	def add_all(self, thing_class): # DEBUG: Should definitely NOT be used for anything else
		for loc in self:
			loc.add(thing_class(self))

	# ~~~ ~~~ ~~~

	def height(self): return self.size[1]
	def width(self): return self.size[0]

	def draw(self, surface, start=v.Vector(0,0)):
		for y in range(self.height()):
			for x in range(self.width()):
				for sprite in self.grid[y][x].get_sprites():
					surface.blit(sprite, (start[1]+y*self.cell_size[1], start[0]+x*self.cell_size[0]))

	# ~~~ ~~~ ~~~

	def get_moore_neighbourhood(self, pos):
		y, x = pos
		return [
			[self[y-1][x-1], self[y-1][x], self[y-1][x+1]]
			[self[y][x-1], self[y][x], self[y][x+1]]
			[self[y+1][x-1], self[y+1][x], self[y+1][x+1]]
		]

	# ~~~ ~~~ ~~~

	def drop_player(self, player, pos):
		self[pos[1]][pos[0]].add_stuff(player)
		player.board = self; player.pos = pos