import thing
import vector as v

class Telepad(thing.Thing):

	unique = True

	spritesheet = "Telepad"

	def __init__(self, target_x, target_y, target_board_key=None):
		super().__init__()
		self.target_location = v.Vector(target_x,target_y)
		self.target_board_key = target_board_key

	def step_on(self, entity):
		entity.teleport(self.target_location, self.target_board_key)