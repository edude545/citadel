import pygame
import os
import sys
import time
import colors



class Mod:

	def __init__(self, path, game, res=32):
		self.game = game

		assets_path = "mods\\"+path+"\\assets"
		things_path = "mods\\"+path+"\\things"

		if os.path.isdir(assets_path):
			for asset_file_name in os.listdir(assets_path):
				if asset_file_name[0] != "_":
					name, ext = asset_file_name.split(".")[-2:]
					if ext == "png":
						self.add(Spritesheet(pygame.image.load(assets_path + "\\" + asset_file_name), name, res=32), name)

		if os.path.isdir(things_path):
			sys.path.insert(0, things_path)
			for thing_file_name in os.listdir(things_path):
				if thing_file_name[0] != "_": # every file not starting with _ is considered to be a thing file and will be interpreted as such

					name = thing_file_name.split(".")[0]
					thing_file = __import__(name)

					if not hasattr(thing_file, name):
						raise Exception("Module \"" + name + "\" has no class with that name")

					thing_class = getattr(thing_file, name)

					if hasattr(thing_class, "spritesheet"):
						thing_class.spritesheet = self.lookup(thing_class.spritesheet)
						if not hasattr(thing_class, "sprite"):
							thing_class.sprite = 0

					self.add(thing_class, name)
			del(sys.path[0])

	def __getitem__(self, index):
		index = index.split(".",1)
		if index[0] == "assets":
			return self.lookup_asset(index[1])
		elif index[0] == "things":
			return self.lookup_thing(index[1])
		raise KeyError("Couldn't find "+index[0]+"."+index[1])

	def lookup(self, name):
		if hasattr(self,name): return getattr(self,name)

	def add(self, element, name):
		setattr(self,name,element)

	def call_hook(self, name):
		getattr(self,name)(self.game)

	def preload(self, game): pass
	def onload(self, game): pass
	def onregistryload(self, game): pass
	def onquit(self, game): pass



class Spritesheet:
	def __init__(self, raw, name, res=32): # raw is a pygame Surface object that represents an unprocessed spritesheet
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

