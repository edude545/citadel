import thing

class DebugTile(thing.Thing):

	# debug object - impassable but not actually a tile
	# can be red or green, toggles when interacted with

	spritesheet = "rg"
	sprite = 0
	passable = False

	def interact(self, entity):
		self.sprite = int(not self.sprite)