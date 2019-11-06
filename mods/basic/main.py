import mod

class Basic(mod.Mod):

	def onload(game):
		game.add_console_message("basic has been loaded!")
		print("OK")