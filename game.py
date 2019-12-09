import os
import pygame
from pygame.locals import *
import ctypes
import vector as v

import thing
import board
import colors
import mod_registry
import common
import ui
import pickle

class Game:
	def __init__(self):

		self.max_tps = 30
		self.tps = self.max_tps

		gsm = ctypes.windll.user32.GetSystemMetrics
		self.res = gsm(0), gsm(1)

		self.game_region_corner = v.Vector(8, 8)
		self.ui_region_corner = v.Vector(912, 8)

		self.cmds = {}
		self.ui_elements = []

		self.console_input = ""
		self.console_messages = []
		self.console_is_selected = False
		self.pause_status_before_console_opened = True
		self.last = None

		self.control_inventory_panel = None
		self.cursor_itemstack_panel = None

		self.ticking = False

		self.active_save = None
		self.active_save_name = None
		self.autosave_enabled = True
		self.autosave_interval = 6000

	# ~~~ ~~~ ~~~ v Core game functions v ~~~ ~~~ ~~~

	def load_mods(self):
		self.mods = mod_registry.ModRegistry(self)
		self.add_console_message("Loaded mods: " + str(self.mods.get_mod_names()))

	def do_pygame_init(self):
		#pygame.init()
		pygame.font.init()
		os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0" # forces pygame window to be created starting at the top-left of the screen
		self.screen = pygame.display.set_mode(tuple(self.res), pygame.NOFRAME)
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font(pygame.font.get_default_font(), 10)

	def launch(self):
		self.mods.call_hooks("onlaunch")
		while True:
			for ev in pygame.event.get():
				self.handle_event(ev)

			if self.has_save_loaded() and self.ticking:
				self.active_save.tick()

			self.draw()

			self.clock.tick(self.tps)

	def is_ticking(self): return self.ticking

	# ~~~ ~~~ ~~~ v Save functions v ~~~ ~~~ ~~~

	def new_save(self):
		self.add_console_message("Created new save")
		self.active_save = Save()
		self.active_save.game = self
		self.active_save_name = "unnamed"

	def save(self, save_name, debug_msg=True):
		delattr(self.active_save,"game") # the reference to the game object is removed so it doesn't get pickled...
		with open("saves\\"+save_name,"wb") as f:
			pickle.dump(self.active_save, f)
		self.active_save.game = self # ...and re-added once saving is complete
		if self.active_save_name != save_name:
			self.active_save_name = save_name
			self.add_console_message("Updated active save name to "+save_name)
		if debug_msg: self.add_console_message("Saved to "+save_name)

	def load(self, save_name):
		if save_name not in os.listdir("saves"):
			self.add_console_message("Failed loading save "+save_name+" - save does not exist")
		else:
			with open("saves\\"+save_name,"rb") as f:
				self.active_save = pickle.load(f)
			self.active_save.game = self
			self.active_save_name = save_name
			self.add_console_message("Loaded "+save_name)
			self.refresh_ui()

	def autosave(self, debug_msg=True):
		self.save(self.active_save_name, debug_msg=False)
		if debug_msg: self.add_console_message("Autosaved as "+self.active_save_name)

	def has_save_loaded(self): return self.active_save is not None

	def quit(self):
		if self.has_save_loaded() and self.autosave_enabled:
			self.autosave(debug_msg=False)
			self.add_console_message("Autosaved as "+self.active_save_name+"; quitting")
		else:
			self.add_console_message("Quitting")
		pygame.quit()
		quit()
	def toggle_pause(self): self.ticking = not self.ticking
	def toggle_autosave(self): self.autosave_enabled = not self.autosave_enabled

	# ~~~ ~~~ ~~~ v Console/script methods v ~~~ ~~~ ~~~

	def do_cmd(self, inp): # cmd[0] is list of argument types, cmd[1] is the function it calls with the arguments
		if inp != "" and inp[0] != ";" and not inp.isspace():
			inp = inp.split(" ")
			try: cmd = self.cmds[inp[0]]
			except KeyError: self.add_console_message("Command not found: " + inp[0])
			else:
				if cmd[0] is None:
					for i in range(len(inp[1:])+1):
						inp[i] = common.smartcast(inp[i])
					cmd[1](self, inp[1:])
				elif len(cmd[0]) != len(inp)-1:
					self.add_console_message("Invalid number of arguments for "+inp[0]+": expected "+str(len(cmd[0]))+", got "+str(len(inp)-1))
				else:
					for i in range(1, len(inp)):
						try:
							inp[i] = cmd[0][i-1](inp[i])
						except ValueError:
							self.add_console_message("Couldn't interpret "+inp[i]+" as "+str(cmd[0][i-1])+" for argument "+str(i)+" of "+inp[0]); return
					cmd[1](self, inp[1:])

	def add_cmd(self, name, arg_types, func):
		self.cmds[name] = (arg_types, func)

	def add_console_message(self, msg):
		print(":: "+msg)
		self.console_messages.append(msg)

			
	# ~~~ ~~~ ~~~ v Drawing methods v ~~~ ~~~ ~~~

	def draw(self):
		self.screen.fill(colors.backdrop)
		if not self.has_save_loaded():
			self.screen.blit(ui.qrender("NO SAVE LOADED"),(10,10))
		elif self.active_save.get_control() is None:
			self.screen.blit(ui.qrender("CONTROL UNASSIGNED"),(10,10))
		else:
			self.active_save.active_board.draw(self.screen, start=self.game_region_corner)
		self.draw_ui(self.screen)
		pygame.display.flip()

	# ~~~ ~~~ ~~~ v Event methods v ~~~ ~~~ ~~~

	def handle_event(self, ev):
		if ev.type is QUIT:
			self.quit()
		elif ev.type is KEYDOWN:
			self.handle_keydown_event(ev)
		elif ev.type is MOUSEBUTTONDOWN:
			self.handle_click_event(ev.button,ev.pos)

	def handle_keydown_event(self, ev):
		if self.has_save_loaded() and self.active_save.get_control() is not None and self.is_ticking():
			self.active_save.get_control().handle_keydown_event(ev)

		if self.cursor_has_item():
			if ev.key is K_ESCAPE:
				self.cursor_cancel()
		elif self.console_is_selected:
			if ev.key in (K_BACKQUOTE,K_ESCAPE):
				self.toggle_select_console()
			elif ev.key is K_BACKSPACE:
				self.console_input = self.console_input[0:-1]
			elif ev.key is K_RETURN:
				self.do_cmd(self.console_input); self.console_input = ""
			else:
				if chr(ev.key) in common.keyboard_replace_dict:
					ev.key = ord(common.keyboard_replace_dict[chr(ev.key)])
				if pygame.key.get_mods() & KMOD_SHIFT: # if shift is held...
					if 97 <= ev.key <= 122: # ...and the character entered is a letter...
						self.console_input += chr(ev.key-32) # ...subtract 32 from the character to make it uppercase
					elif chr(ev.key) in common.keyboard_shift_dict:
						self.console_input += common.keyboard_shift_dict[chr(ev.key)]
				else:
					self.console_input += chr(ev.key)

		elif ev.key is K_ESCAPE:
			self.quit()
		elif ev.key is K_SPACE:
			self.toggle_pause()
		elif ev.key is K_BACKQUOTE:
			self.toggle_select_console()
		elif ev.key is K_c:
			self.toggle_select_inventory()
		elif ev.key is K_SEMICOLON:
			for element in self.ui_elements:
				element.toggle_visibility()

	def handle_click_event(self,button,pos):
		for element in self.ui_elements:
			if element.pos is not None and element.in_bounds(pos):
				element.on_click(button,(pos[0]-element.pos[0],pos[1]-element.pos[1]))

	# ~~~ ~~~ ~~~ v Interface methods v ~~~ ~~~ ~~~

	def toggle_select_console(self):
		#self.toggle_control_inventory_panel()
		if not self.console_is_selected:
			self.pause_status_before_console_opened = self.ticking
			self.ticking = False
		else:
			self.ticking = self.pause_status_before_console_opened
		self.console_is_selected = not self.console_is_selected

	def cursor_pickup(self,isp):
		self.cursor_itemstack_panel = isp

	def cursor_cancel(self):
		self.cursor_itemstack_panel = None

	def cursor_has_item(self):
		return self.cursor_itemstack_panel is not None

	# ~~~ ~~~ ~~~ v UI methods v ~~~ ~~~ ~~~

	def add_ui_element(self, element):
		self.ui_elements.append(element)
		element.game = self
		#self.ui_elements.insert(0, element)

	def remove_ui_element(self, element):
		self.ui_elements.remove(element)

	def add_control_inventory_panel(self):
		self.control_inventory_panel = ui.InventoryPanel(self.active_save.control.inventory, (10,5), pos=(912,480))
		self.add_ui_element(self.control_inventory_panel)

	def remove_control_inventory_panel(self):
		self.remove_ui_element(self.control_inventory_panel)
		self.control_inventory_panel = None

	def toggle_control_inventory_panel(self):
		self.control_inventory_panel.toggle_visibility()

	def draw_ui(self, surface):
		pos = self.ui_region_corner
		for element in self.ui_elements:
			if not element.hidden:
				if element.pos is not None:
					element.draw(surface, element.pos)
				else:
					element.draw(surface, tuple(pos))
					pos += v.Vector(0, element.height)
		if self.cursor_has_item():
			self.screen.blit(self.cursor_itemstack_panel.render(),(pygame.mouse.get_pos()[0]-16,pygame.mouse.get_pos()[1]-16))

	def refresh_ui(self):
		if self.control_inventory_panel is not None:
			self.remove_control_inventory_panel()
		if self.has_save_loaded and hasattr(self.active_save.control,"inventory"):
			self.add_control_inventory_panel()

	

class Save:

	def __init__(self):
		self.control = None
		self.active_board = None
		self.active_board_key = None
		self.boards = {}
		self.gametime = 0
		# Given attribute game - type Game

	def __getitem__(self, index):
		return self.boards[index]
	def __setitem__(self, element, index):
		self.boards[index] = element

	# ~~~ ~~~ ~~~ v Game methods v ~~~ ~~~ ~~~

	def tick(self):
		self.gametime += 1
		if self.gametime % self.game.autosave_interval == 0:
			self.game.autosave()

	# ~~~ ~~~ ~~~ v Board methods v ~~~ ~~~ ~~~

	def add_board(self, board, key):
		if key == "_metadata":
			self.add_console_message("Can't add board with name \"_metadata\"!")
		else:
			self[key] = board

	def get_board(self, key):
		return self.boards[key]

	def set_active_board(self, key):
		self.active_board = self.boards[key]

	# ~~~ ~~~ ~~~ v Attribute access methods v ~~~ ~~~ ~~~

	def get_gametime(self): return self.gametime
	
	# ~~~ ~~~ ~~~ v Control methods v ~~~ ~~~ ~~~

	def set_control(self, entity):
		self.game.add_console_message("Shifted control to "+repr(entity))
		if not issubclass(type(entity), thing.Controllable):
			raise ValueError("Attempted to shift control to an object that does not inherit from thing.Controllable")
		self.control = entity
		if hasattr(entity,"inventory"):
			self.game.add_control_inventory_panel()

	def get_control(self):
		return self.control

	# ~~~ ~~~ ~~~ v Misc. methods v ~~~ ~~~ ~~~

	def setup_debug_environment(self):
		G = self.game
		self.add_board("dbg", board.Board(self, v.Vector(12,7)))
		self.set_active_board("dbg")
		self["dbg"].add_all(G.mods["basic"].Grass)
		G.do_cmd("make basic.Player");G.do_cmd("place last 3 3")
		G.do_cmd("make basic.Telepad 10 5 dbg");G.do_cmd("place last 4 2")
		G.do_cmd("place basic.StoneWall 1 2")
		G.do_cmd("place basic.StoneWall 1 3")
		G.do_cmd("place basic.StoneWall 2 2")
		G.do_cmd("place basic.StoneWall 2 3")
		G.do_cmd("place basic.StoneWall 2 4")
		G.do_cmd("place basic.StoneWall 2 5")
		G.do_cmd("place basic.StoneWall 3 5")
		G.do_cmd("place basic.StoneWall 4 3")
		G.do_cmd("place basic.DebugTile 4 4")
		G.do_cmd("place basic.DebugTile 11 6")