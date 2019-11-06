import vector as v
import transform
import pygame
from pygame.locals import *

import common


class Controllable:
	def handle_keydown_event(self, ev): pass
	def handle_keyup_event(self, ev): pass


class Door:
	def interact(self, entity):
		self.passable = not self.passable
		self.sprite = int(not self.sprite)


class Thing: # The class for a game object that can exist in a board, e.g. tiles, interactive objects, entities, and items.

	# Given attribute img, type pygame.Surface
	# Given attribute spritesheet, type pygame.Surface
	# Given attribute loc, type board.Location

	unique = False

	passable = True

	def __init__(self):
		self.enabled = True

	def __str__(self):
		return type(self).__name__

	def __eq__(self, arg):
		return type(self) is type(arg) and not self.unique and not arg.unique

	# ~~~ ~~~ v Attribute access

	def get_pos(self): return self.get_loc().pos
	def get_loc(self): return self.loc
	def get_board(self): return self.get_loc().board
	def get_game(self): return self.get_board().game

	def draw(self, surface, x, y):
		surface.blit(self.get_sprite(), (x,y))

	def get_sprite(self):
		return self.spritesheet[self.sprite]
	def get_spritesheet(self):
		return self.spritesheet

	def teleport(self, target_location, target_board_key):
		if target_board_key is None:
			target_board_key = self.get_game().active_board_key
		self.get_game()[target_board_key].move(self, target_location)

	def interact(self, entity):
		pass

	def step_on(self, entity):
		pass


class Tile(Thing):

	passable = False

	# ~~~ ~~~ ~~~

	def get_sprite(self): # x and y switch places here because an array visually representing a section of a board is accessed directly
		mn = self.loc.get_moore_neighbourhood_tiles() # mn is a 3*3 array where True represents the presence of a Tile and False the absence
		r = self.spritesheet[0].copy()
		for y in range(3): # side
			for x in range(3):
				if not mn[y][x] and not (y==x==1):
					if 1 in (y,x):
						ang = {(2,1):0,(1,2):90,(0,1):180,(1,0):270}[(y,x)]
						img = pygame.transform.rotate(self.spritesheet[1], ang)
						r.blit(img, (0,0))
		for y in (0,2): # out-facing corner
			for x in (0,2):
				if not mn[y][x] and not mn[1][x] and not mn[y][1]: # ¬(a|b|c) == (¬a)&(¬b)&(¬c)
					ang = {(2,0):0,(2,2):90,(0,2):180,(0,0):270}[(y,x)]
					img = pygame.transform.rotate(self.spritesheet[2], ang)
					r.blit(img, (0,0))
		for y in (0,2): # in-facing corner
			for x in (0,2):
				if not mn[y][x] and mn[1][x] and mn[y][1]:
					ang = {(2,0):0,(0,0):90,(0,2):180,(2,2):270}[(y,x)]
					img = pygame.transform.rotate(self.spritesheet[3],ang)
					r.blit(img,(0,0))

		return r
		#self.update_sprite_index()
		#return self.spritesheet[self.sprite_index]

	def update_sprite_index(self): ###
		self.sprite_index=0;self.sprite_rotation=0;return
		m = self.get_moore_neighbourhood_tiles
		for x in (-1,0,1):
			for y in (-1,0,1):
				if abs(x)==abs(y): # corner
					pass
				elif 0 in (x,y): # side
					pass


class Entity(Thing):

	def __init__(self):
		super().__init__()
		self.direction = 0
		self.ghost = False

	def get_sprite(self):
		return self.get_spritesheet()[self.direction]

	def get_facing_location(self):
		return self.get_board()[self.get_pos() + common.direction_int_to_vector(self.direction)]

	def face(self, direction):
		self.direction = direction

	def walk(self, dist=1):
		new = self.get_pos() + common.direction_int_to_vector(self.direction) * dist
		if 0 <= new[0] < self.loc.board.width() and 0 <= new[1] < self.loc.board.height() and (self.ghost or self.loc.board[new].is_passable()):
			self.loc.board.move(self, new)
			self.loc.board[new].step_on(self)

	def interact(self):
		self.get_facing_location().interact(self)


class ControllableEntity(Entity, Controllable):

	def handle_keydown_event(self, ev):
		
		if ev.key in (K_DOWN,K_LEFT,K_UP,K_RIGHT):
			if ev.key == K_DOWN: direc = 0
			elif ev.key == K_LEFT: direc = 1
			elif ev.key == K_UP: direc = 2
			elif ev.key == K_RIGHT: direc = 3
			self.face(direc)
			if not pygame.key.get_mods() & KMOD_LSHIFT:
				self.walk()

		elif ev.key == K_z:
			self.interact()

	def toggle_ghost(self):
		self.ghost = not self.ghost