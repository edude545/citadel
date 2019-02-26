import entity

class Player(entity.Entity):
	def __init__(self, name="Player"):
		super().__init__("player", name)