import pygame
import os
from pygame.locals import *
import vector as v

import colors

class Game:
	def __init__(self, size=v.Vector(1280,720)):
		self.size = size

		self.max_tps = 30
		self.tps = self.max_tps
		self.ticking = True

		self.active_board = None

		self.game_region_corner = (v.Vector(0, self.size[0]/4))

	# ~~~ ~~~ ~~~

	def do_pygame_init(self):
		pygame.init()
		pygame.font.init()
		os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
		self.screen = pygame.display.set_mode(tuple(self.size), pygame.NOFRAME)
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font(pygame.font.get_default_font(), 10)

	def launch(self):
		self.toggle_pause()
		while True:
			for ev in pygame.event.get():
				self.handle_event(ev)

			self.tick()
			self.draw()

			self.clock.tick(self.tps)

	def quit(self):
		pygame.quit(); quit()

	def toggle_pause(self):
		self.ticking = not self.ticking
		if self.ticking:
			self.paused_text = self.font.render("", True, colors.text)
		else:
			self.paused_text = self.font.render("(paused)", True, colors.text)
			
	# ~~~ ~~~ ~~~ v Drawing methods v ~~~ ~~~ ~~~

	def draw(self, board=None):
		if board is None: board=self.active_board # you can't put "self" in parameter declarations so you have to do this manually

		self.screen.fill(colors.backdrop)
		board.draw(self.screen, start=self.game_region_corner)
		self.draw_text()
		pygame.display.flip()

	def draw_text(self):
		self.screen.blit(self.paused_text, (1230,705))

	# ~~~ ~~~ ~~~ v Event methods v ~~~ ~~~ ~~~

	def handle_event(self, ev):
		if ev.type is QUIT:
			self.quit()
		elif ev.type is KEYDOWN:
			self.handle_keydown_event(ev)
		elif ev.type is KEYUP:
			self.handle_keyup_event(ev)

	def handle_keydown_event(self, ev):
		if ev.key is K_ESCAPE:
			self.quit()
		elif ev.key is K_SPACE:
			self.toggle_pause()

	def handle_keyup_event(self, ev):
		pass


	# ~~~ ~~~ ~~~

	def tick(self):
		pass