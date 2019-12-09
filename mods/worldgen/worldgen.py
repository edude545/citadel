import board
import mod
import random


class Mod(mod.Mod):

	def onload(self,game):
		game.add_cmd("generate", [], lambda game,args:self.generate_world(game))

		game.add_console_message("Successfully loaded worldgen module")

	def onlaunch(self,game):
		pass

	def generate_world(self,game):
		C = game.do_cmd

		game.new_save()
		a_s = game.active_save

		a_s.add_board("overworld", board.Board(a_s, (32,32)))
		a_s.set_active_board("overworld")

		ow=a_s.get_board("overworld"); middle = ((ow.width()-1)//2,(ow.height()-1)//2)

		C("make basic.Player"); C("".join(("place last "+str(middle[0])+" "+str(middle[1]))))
		C("place_all basic.Grass")
		self.make_building(game,(3,3),"basic.StoneWall","basic.StoneTileFloor","basic.OldWoodenDoor")

	def make_room(self,game,corner,lx,ly,wall,floor,size_range=(4,12)):
		for x in range(lx):
			for y in range(ly):
				th = floor
				if x in (0,lx-1) or y in (0,ly-1):
					th = wall
				game.do_cmd("cplace "+th+" "+str(corner[0]+x)+" "+str(corner[0]+y))

	def make_building(self,game,corner,wall,floor,door,rooms=3,size_range=(4,12)):
		rlist = []
		d = 0
		for i in range(rooms):
			lx,ly = random.randint(0,size_range[0]), random.randint(0,size_range[1])
			rlist.append(((d,0),(lx,ly)))
			d += lx
		print(rlist)

	def add_room_to_building(self,room,building):
		pass