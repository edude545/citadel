import os
import pygame
from pygame.locals import *
import ctypes
import vector as v

import thing
import colors

class Game:
	def __init__(self):

		self.max_tps = 30
		self.tps = self.max_tps
		self.ticking = False
		self.gametime = 0

		gsm = ctypes.windll.user32.GetSystemMetrics
		self.res = gsm(0), gsm(1)

		self.active_board = None

		self.game_region_corner = v.Vector(8, 8)
		self.ui_region_corner = v.Vector(912, 8)

		self.cmds = {}
		self.ui_elements = []

		self.console_input = ""
		self.console_messages = []
		self.console_is_selected = False
		self.pause_status_before_console_opened = True

		self.control = None

	# ~~~ ~~~ ~~~ v Core game functions v ~~~ ~~~ ~~~

	def do_pygame_init(self):
		#pygame.init()
		pygame.font.init()
		os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0" # forces pygame window to be created starting at the top-left of the screen
		self.screen = pygame.display.set_mode(tuple(self.res), pygame.NOFRAME)
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font(pygame.font.get_default_font(), 10)

	def launch(self):
		while True:
			for ev in pygame.event.get():
				self.handle_event(ev)

			if self.ticking:
				self.tick()

			self.draw()

			self.clock.tick(self.tps)

	def quit(self): pygame.quit(); quit()
	def toggle_pause(self): self.ticking = not self.ticking

	# ~~~ ~~~ ~~~ v Console/script methods v ~~~ ~~~ ~~~

	def do_cmd(self, inp):
		if inp != "" and inp[0] != ";" and not inp.isspace():
			inp = inp.split(" ")
			try: cmd = self.cmds[inp[0]]
			except KeyError: self.add_console_message("Command not found: " + inp[0])
			else:
				if len(cmd[0]) != len(inp)-1:
					self.add_console_message("Invalid number of arguments for "+inp[0]+": expected "+str(len(cmd[0]))+", got "+str(len(inp)-1))
				else:
					for i in range(len(inp)-1):
						try:
							inp[i+1] = cmd[0][i](inp[i+1])
						except ValueError:
							self.add_console_message("Couldn't interpret "+inp[i+1]+" as "+cmd[0][i]+" for argument "+str(i)+" of "+cmd[0])
					cmd[1](self, inp[1:])

	def add_cmd(self, name, args, func):
		self.cmds[name] = (args, func)

	def add_console_message(self, msg):
		self.console_messages.append(msg)

	# ~~~ ~~~ ~~~ v Attribute access methods v ~~~ ~~~ ~~~

	def is_ticking(self): return self.ticking
			
	# ~~~ ~~~ ~~~ v Drawing methods v ~~~ ~~~ ~~~

	def draw(self, board=None):
		if board is None: board=self.active_board # you can't put "self" in parameter declarations so you have to do this manually

		self.screen.fill(colors.backdrop)
		board.draw(self.screen, start=self.game_region_corner)
		self.draw_ui(self.screen)
		pygame.display.flip()

	# ~~~ ~~~ ~~~ v Event methods v ~~~ ~~~ ~~~

	def handle_event(self, ev):
		if ev.type is QUIT:
			self.quit()
		elif ev.type is KEYDOWN:
			self.handle_keydown_event(ev)
		elif ev.type is KEYUP:
			self.handle_keyup_event(ev)

	def handle_keydown_event(self, ev):
		if self.get_control() is not None and self.is_ticking():
			self.control.handle_keydown_event(ev)

		if self.console_is_selected:
			if ev.key in (K_BACKQUOTE,K_ESCAPE):
				self.console_is_selected = False
				self.ticking = self.pause_status_before_console_opened
			elif ev.key is K_BACKSPACE:
				self.console_input = self.console_input[0:-1]
			elif ev.key is K_RETURN:
				self.do_cmd(self.console_input); self.console_input = ""
			else:
				if 97 <= ev.key <= 122 and pygame.key.get_mods() & KMOD_SHIFT: self.console_input += chr(ev.key-32)
				elif ev.key not in (K_RSHIFT,K_LSHIFT): self.console_input += chr(ev.key)
		elif ev.key is K_ESCAPE:
			self.quit()
		elif ev.key is K_SPACE:
			self.toggle_pause()
		elif ev.key is K_BACKQUOTE:
			self.console_is_selected = True
			self.pause_status_before_console_opened = self.ticking
			self.ticking = False
		elif ev.key is K_SEMICOLON:
			for element in self.ui_elements:
				element.toggle_visibility()

	def handle_keyup_event(self, ev):
		pass

	# ~~~ ~~~ ~~~ v Control methods v ~~~ ~~~ ~~~

	def set_control(self, entity):
		if not issubclass(entity.__class__, thing.Controllable):
			raise ValueError("Attempted to shift control to an object that does not inherit from Controllable")
		self.control = entity

	def get_control(self):
		return self.control

	# ~~~ ~~~ ~~~ v UI methods v ~~~ ~~~ ~~~

	def add_ui_element(self, element):
		self.ui_elements.append(element)
		#self.ui_elements.insert(0, element)

	def draw_ui(self, surface):
		pos = self.ui_region_corner
		for element in self.ui_elements:
			if not element.hidden:
				if element.pos is not None:
					element.draw(surface, element.pos)
				else:
					element.draw(surface, tuple(pos))
					pos += v.Vector(0, element.height)

	# ~~~ ~~~ ~~~

	def tick(self):

		self.gametime += 1
