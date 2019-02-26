import vector as v

import mod_registry

import game
import board

imgs = image_registry.ImageRegistry("basic_tiles", "blank", "player")
mapobjects.assign_images(imgs)

g = game.Game()
g.do_pygame_init()

b = board.Board(g, v.Vector(50,40))
b.add_all("f_stone_tile")

g.active_board = b

g.launch()