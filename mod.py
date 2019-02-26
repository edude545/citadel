class Mod:

	def __init__(self, path):
		self.module = __import__(path)

		self.assets = {}
		self.thing_classes = {}


	def lookup_asset(self, name):
		if name in self.assets:
			return self.assets[name]
	def lookup_thing_class(self, name):
		if name in self.thing_classes:
			return self.thing_classes[name]


	def add_asset(self, asset, name):
		self.assets[name] = asset
	def add_thing_class(self, thing_class, name):
		self.thing_classes[name] = thing_class


	def load_spritesheet(self, spritesheet, res=32):
		if spritesheet.get_width() > res or spritesheet.get_height() > res:
			cnt = 0
			for y in range(0, spritesheet.get_height(), res):
				for x in range(0, spritesheet.get_width(), res):
					self[file+"_"+str(cnt)] = spritesheet.subsurface(pygame.Rect(x,y,res,res))
					cnt += 1