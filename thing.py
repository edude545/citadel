import vector as v
import transform
import pygame
from pygame.locals import *

import common


class Controllable:
	def handle_keydown_event(self, ev): pass
	def handle_keyup_event(self, ev): pass

class StorePos:
	pass

class Door:
	def interact(self, entity):
		self.passable = not self.passable
		self.sprite = int(not self.sprite)


class Thing: # The class for a game object that can exist in a board, e.g. tiles, interactive objects, entities, and items.

	# Given attribute img, type pygame.Surface
	# Given attribute spritesheet, type pygame.Surface

	passable = True

	def __init__(self, board):
		self.enabled = True
		self.board = board

	def draw(self, surface, x, y):
		surface.blit(self.get_sprite(), (x, y))

	def get_sprite(self):
		return self.spritesheet[self.sprite]
	def get_spritesheet(self):
		return self.spritesheet

	def interact(self, entity):
		pass


class Tile(Thing, StorePos): # WIP - this class is *not* used yet

	passable = False

	def __init__(self, board):
		super().__init__(board)

	# ~~~ ~~~ ~~~

	def get_sprite(self): # x and y switch places here because an array visually representing a section of a board is accessed directly
		mn = self.board.get_moore_neighbourhood_tiles(self.pos)
		r = self.spritesheet[0].copy()
		for x in range(3): # side
			for y in range(3):
				if not mn[y][x] and not (x==y==1):
					if 1 in (y,x):
						ang = {(2,1):0,(1,2):90,(0,1):180,(1,0):270}[(y,x)]
						img = pygame.transform.rotate(self.spritesheet[1], ang)
						r.blit(img, (0,0))
		for x in (0,2): # corner
			for y in (0,2):
				if not (mn[y][x] or mn[1][x] or mn[y][1]):
					ang = {(2,0):0,(0,0):90,(0,2):180,(2,2):270}[(y,x)]
					img = pygame.transform.rotate(self.spritesheet[2], ang)
					r.blit(img, (0,0))
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


class Entity(Thing, StorePos):

	def __init__(self, board):
		super().__init__(board)
		self.direction = 0
		self.ghost = False

	def get_sprite(self):
		return self.get_spritesheet()[self.direction]

	def get_facing_location(self):
		return self.board[self.pos + common.direction_int_to_vector(self.direction)]

	def face(self, direction):
		self.direction = direction

	def walk(self, dist=1):
		new = self.pos + common.direction_int_to_vector(self.direction) * dist
		if 0 <= new[0] < self.board.width() and 0 <= new[1] < self.board.height() and (self.ghost or self.board[new].is_passable()):
			self.board.move(self, new)

	def interact(self):
		self.get_facing_location().interact(self)


class ControllableEntity(Entity, Controllable):

	def handle_keydown_event(self, ev):
		
		if ev.key in (K_s,K_a,K_w,K_d):
			if ev.key is K_s: direc = 0
			elif ev.key is K_a: direc = 1
			elif ev.key is K_w: direc = 2
			elif ev.key is K_d: direc = 3
			self.face(direc)
			if not pygame.key.get_mods() & KMOD_LSHIFT:
				self.walk()

		elif ev.key is K_f:
			self.interact()

	def toggle_ghost(self):
		self.ghost = not self.ghost