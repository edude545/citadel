import pygame
import os
import sys

import mod


class ModRegistry:

	def __init__(self, game):
		self.game = game
		self.mods = {}
		self.img_ext = ".png"

		for name in os.listdir("mods"):
			if name[0] != "_": # ignore mods that have an underscore at the starts of their names
				sys.path.insert(0,"mods\\"+name)
				self[name] = __import__(name).Mod(name,self.game)
				del(sys.path[0])
				self.game.add_console_message("HOOK: onload, "+name)
				self[name].call_hook("onload")
		del(sys.path[0])

		self.call_hooks("onregistryload")

	def __iter__(self):
		for k in self.mods:
			yield self.mods[k]

	def __getitem__(self, index):
		return self.mods[index]
	def __setitem__(self, index, val):
		self.mods[index] = val

	def quick_thing_lookup(self, name): # name should look like "basic.DebugTile"
		name = name.split(".")
		return self[name[0]].lookup(name[1])

	def get_mod_names(self):
		return list(self.mods)

	def call_hooks(self, name):
		self.game.add_console_message("HOOK: "+name)
		for mod in self:
			mod.call_hook(name)