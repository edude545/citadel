import pygame
import os
import sys
import time
import colors
import dmap



class Mod:

	def __init__(self, path, res=32):
		module = __import__("mods." + path)

		self.assets = dmap.DMap()
		self.things = dmap.DMap()

		assets_path = "mods\\" + path + "\\assets"
		things_path = "mods\\" + path + "\\things"

		for asset_file_name in os.listdir(assets_path):
			if asset_file_name[0] != "_":
				name, ext = asset_file_name.split(".")[-2:]
				if ext == "png":
					self.add_asset(Spritesheet(pygame.image.load(assets_path + "\\" + asset_file_name), name, res=32), name)

		sys.path.insert(0, things_path)
		for thing_file_name in os.listdir(things_path):
			if thing_file_name[0] != "_": # every file not starting with _ is considered to be a thing file and will be interpreted as such
				name = thing_file_name.split(".")[0]
				thing_file = __import__(name)
				if hasattr(thing_file, name):
					thing_class = getattr(thing_file, name)
					if hasattr(thing_class, "spritesheet"):
						thing_class.spritesheet = self.lookup_asset(thing_class.spritesheet)
						if hasattr(thing_class, "sprite"):
							thing_class.sprite = thing_class.spritesheet[thing_class.sprite]
					self.add_thing(thing_class, name)
				else:
					raise Exception("Module \"" + name + "\" has no class with that name")

	def __getitem__(self, index):
		index = index.split(".",1)
		if index[0] == "assets":
			return self.lookup_asset(index[1])
		elif index[0] == "things":
			return self.lookup_thing(index[1])
		raise KeyError("Couldn't find "+index[0]+"."+index[1])

	def lookup_asset(self, name):
		if name in self.assets:
			return self.assets[name]
	def lookup_thing(self, name):
		if name in self.things:
			return self.things[name]

	def add_asset(self, asset, name):
		self.assets[name] = asset
	def add_thing(self, thing, name):
		self.things[name] = thing




class Spritesheet:
	def __init__(self, raw, name, res=32): # raw is a pygame Surface object that represents an unprocessed spritesheet
		self.raw = raw
		self.name = name
		self.res = res

		self.sprites = []

		cnt = 0
		for y in range(0, raw.get_height(), res):
			for x in range(0, raw.get_width(), res):
				self.sprites.append(raw.subsurface(pygame.Rect(x,y,res,res)))
				cnt += 1

	def __getitem__(self, index):
		return self.sprites[index]

	def __iter__(self):
		for sprite in self.sprites:
			yield sprite


	# Debug function - shows the raw spritesheet, then all of its sprites in succession
	def dbg_show(self):
		pygame.init()
		tmp=pygame.display.set_mode((self.raw.get_width(), self.raw.get_height()))
		tmp.blit(self.raw, (0,0))
		pygame.display.flip()
		time.sleep(2)
		for sprite in self:
			tmp.fill(colors.black)
			tmp.blit(sprite, (0,0))
			pygame.display.flip()
			time.sleep(1)
		pygame.quit()

