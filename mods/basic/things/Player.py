import thing

class Player(thing.ControllableEntity):

	spritesheet = "player"

	def __init__(self, board):
		super().__init__(board)
		board.game.set_control(self)