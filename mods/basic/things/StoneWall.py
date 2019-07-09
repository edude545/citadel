import thing

class StoneWall(thing.Tile):
	
	passable = False

	spritesheet = "TileConnectionTest"
	sprite = 0

	def interact(self, entity):
		print(self.board.get_moore_neighbourhood_tiles(self.pos))