import pygame
import vector as v

import mapobjects


class Location:
	def __init__(self):
		self.stuff = []

	def get_stuff(self, type_):
		r = list(filter(lambda x: type(x) is type_, self.stuff))
		if r == []:
			return type_.default
		if len(r) > 1:
			raise Exception("Location " + str(self) + " has multiple " + str(type_) + ": " + str(r))
		return r[0]

	def add_stuff(self, *stuff):
		self.stuff += stuff

	def gen_imgs(self):
		return [stuff.img for stuff in self.stuff]



class Board:
	def __init__(self, game, size): # size is a vector
		self.game = game
		self.size = size

		self.grid = [[Location() for _ in range(self.width())] for _ in range(self.height())]
		#self.rects = [[pygame.Rect((y,x), tuple(self.cell_size)) for x in range(self.width())] for y in range(self.height())]

		self.cell_size = v.Vector(15,15)

	def __iter__(self):
		for y in range(len(self.grid)):
			for x in range(len(self.grid[0])):
				yield (y,x)

	def __getitem__(self, index):
		return self.grid[index]

	# ~~~ ~~~ ~~~

	def add_all(self, name): # DEBUG: Should NOT be used for anything else
		for y,x in self:
			l = Location(); l.add_stuff(mapobjects.new_stuff(name)); self[y][x] = l

	# ~~~ ~~~ ~~~

	def height(self): return self.size[1]
	def width(self): return self.size[0]

	def draw(self, surface, start=v.Vector(0,0)):
		for y in range(self.height()):
			for x in range(self.width()):
				for img in self.grid[y][x].gen_imgs():
					surface.blit(img, (start[1]+y*self.cell_size[1], start[0]+x*self.cell_size[0]))

	# ~~~ ~~~ ~~~

	def drop_player(self, player, pos):
		self[pos[1]][pos[0]].add_stuff(player)
		player.board = self; player.pos = pos