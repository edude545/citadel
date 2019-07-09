import thing

class DebugTile(thing.Thing):

	spritesheet = "rg"
	sprite = 0
	passable = False

	def interact(self, entity):
		self.sprite = int(not self.sprite)