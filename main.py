import vector as v

import mod_registry

import board
import thing
import game
import ui

g = game.Game()

g.load_mods()

def _(game,args): game.gametime = 0 # resetgametime
g.add_cmd("resetgametime", [], _)

def _(game,args): # place
	if args[0] == "last":
		if game.last is None:
			print("No thing stored in memory")
		else:
			game.active_save.active_board.add(game.last, v.Vector(args[1],args[2]))
			game.last = None
	else:
		thing_class = game.mods.quick_thing_lookup(args[0])
		if thing_class.unique:
			game.add_console_message("Can't add "+thing_class.__name__+" directly because it is Unique - use make")
		else:
			game.active_save.active_board.add_from_class(thing_class, v.Vector(args[1],args[2]))
g.add_cmd("place", [str, int, int],  _)

def _(game,args): # make
	game.last = game.mods.quick_thing_lookup(args[0])(*args[1:])
g.add_cmd("make", None, _)

def _(game,args): # give
	thing_class = game.mods.quick_thing_lookup(args[0])
	if thing_class.unique:
		game.add_console_message("Can't give "+thing_class.__name__+" directly because it is Unique - use make")
	else:
		game.active_save.control.inventory.add(thing_class(),args[1])
g.add_cmd("give", [str, int], _)

def _(game,args): # gmn
	for th in game.control.get_facing_location():
		if issubclass(type(th),thing.Tile):
			game.add_console_message(str(game.active_board.get_moore_neighbourhood_tiles(th.pos)))
g.add_cmd("gmn", [], _)

g.add_cmd("save", [str], lambda game,args:game.save(args[0]))
g.add_cmd("load", [str], lambda game,args:game.load(args[0]))
g.add_cmd("autosave", [], lambda game,args:game.toggle_autosave())
g.add_cmd("active_save_name", [], lambda game,args:game.add_console_message(game.active_save_name))
g.add_cmd("hello", [], lambda game,args: game.add_console_message("Hello world!"))
g.add_cmd("echo", [str], lambda game,args: game.add_console_message(args[0]))
g.add_cmd("ghost", [], lambda game,args: game.active_save.control.toggle_ghost())
g.add_cmd("gametime", [], lambda game,args:game.add_console_message(game.active_save.get_gametime()))
g.add_cmd("sb", [], lambda game,args:game.add_console_message(str("Boards: "+str(game.active_save.boards if game.has_save_loaded() else "n/a"))))
g.add_cmd("sc", [], lambda game,args:game.add_console_message(str("Control: "+str(game.active_save.control if game.has_save_loaded() else "n/a"))))
g.add_cmd("ginv", [], lambda game,args:game.add_console_message(str(game.active_save.control.inventory)))

g.add_ui_element(ui.Monitor(lambda:""if g.ticking else"(paused)",pos=v.Vector(1237,2)))
g.add_ui_element(ui.Monitor(lambda:"gametime: "+(str(g.active_save.gametime) if g.active_save is not None else "n/a")))

g.add_ui_element(ui.Monitor(lambda:g.console_messages[-3]if len(g.console_messages)>=3 else "",pos=v.Vector(912,669)))
g.add_ui_element(ui.Monitor(lambda:g.console_messages[-2]if len(g.console_messages)>=2 else "",pos=v.Vector(912,680)))
g.add_ui_element(ui.Monitor(lambda:g.console_messages[-1]if len(g.console_messages)>=1 else "",pos=v.Vector(912,691)))
g.add_ui_element(ui.Monitor(lambda:">>> "if g.console_is_selected else"",pos=v.Vector(912,702)))
g.add_ui_element(ui.Monitor(lambda:g.console_input,pos=v.Vector(935,702)))


g.do_pygame_init()

# here the game is prepared but not launched; can run commands here
g.new_save(); g.active_save.setup_debug_environment()

#g.do_cmd("load debug")

g.do_cmd("give basic.Stick 3")
g.do_cmd("give basic.Stick 5")
g.do_cmd("give basic.StoneWall 3")
g.do_cmd("give basic.DebugTile 5")

# ~~~

g.launch()