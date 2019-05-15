import pygame
import os

import mod


class ModRegistry:

	def __init__(self, *files):
		self.mods = {}
		self.img_ext = ".png"

		for name in os.listdir("mods"):
			if name[0] != "_": # ignore mods that have an underscore at the starts of their names
				self[name] = mod.Mod(name)

	def __getitem__(self, index):
		return self.mods[index]
	def __setitem__(self, index, val):
		self.mods[index] = val

	def __getattr__(self, attr):
		return self[attr]


	def get_mod_names(self):
		return list(self.mods)