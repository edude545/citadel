import vector as v

import mod_registry

import board
import thing
import game
import ui

mods = mod_registry.ModRegistry()
print("Loaded mods: " + str(mods.get_mod_names()))

g = game.Game()

g.add_cmd("echo", [str], lambda game,args: game.add_console_message(args[0]))

g.add_cmd("ghost", [], lambda game,args:game.control.toggle_ghost())

def _(game,args): game.gametime = 0
g.add_cmd("resetgametime", [], _)

def _(game,args): args[0]=args[0].split(".",1); game.active_board.add_from_class(mods[args[0][0]]["things."+args[0][1]], v.Vector(args[1],args[2]))
g.add_cmd("place", [str, int, int],  _)

def _(game,args):
	for th in game.control.get_facing_location():
		if issubclass(type(th),thing.Tile):
			game.add_console_message(str(game.active_board.get_moore_neighbourhood_tiles(th.pos)))
g.add_cmd("gmn", [], _)

g.add_ui_element(ui.Monitor(lambda:""if g.ticking else"(paused)",pos=v.Vector(1237,2)))
g.add_ui_element(ui.Monitor(lambda:"gametime: "+str(g.gametime)))
g.add_ui_element(ui.Monitor(lambda:g.console_input,pos=v.Vector(935,700)))
g.add_ui_element(ui.Monitor(lambda:g.console_messages[-1]if g.console_messages!=[]else "",pos=v.Vector(912,688)))
g.add_ui_element(ui.Monitor(lambda:">>> "if g.console_is_selected else"",pos=v.Vector(912,700)))

g.do_pygame_init()

b = board.Board(g, v.Vector(12,7))
b.add_all(mods.basic.things.StoneTileFloor)
 
g.active_board = b

# pre-launch commands
g.do_cmd("place basic.Player 3 3")
g.do_cmd("place basic.StoneWall 1 2")
g.do_cmd("place basic.StoneWall 1 3")
g.do_cmd("place basic.StoneWall 2 2")
g.do_cmd("place basic.StoneWall 2 3")
g.do_cmd("place basic.StoneWall 2 4")
g.do_cmd("place basic.StoneWall 2 5")
g.do_cmd("place basic.StoneWall 3 5")
g.do_cmd("place basic.StoneWall 4 3")
g.do_cmd("place basic.DebugTile 4 4")
g.do_cmd("place basic.DebugTile 11 6")
"""for a in range(0,11):
	for b in range(0,5):
		g.do_cmd("place basic.StoneWall "+str(a)+" "+str(b))"""

g.launch()