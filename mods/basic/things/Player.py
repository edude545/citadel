import thing
import inventory

class Player(thing.ControllableEntity):

	unique = True

	def __init__(self):
		super().__init__()
		self.inventory = inventory.Inventory(size=50)

	spritesheet = "player"