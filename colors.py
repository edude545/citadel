def complement(color):
	return tuple(abs(255-el) for el in color)

def set_backdrop(color):
	global backdrop; global text
	backdrop = color; text = complement(backdrop)

# (R, G, B)

black = (0, 0, 0)
white = (255, 255, 255)

lgray = (191, 191, 191)
gray = (127, 127, 127)
dgray = (63, 63, 63)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

pink = (255, 191, 191)
turquoise = (191, 255, 191)
lblue = (191, 191, 255)

orange = (255, 255, 0)
cyan = (0, 255, 255)
purple = (255, 0, 255)

navy = (0, 0, 63)
dgreen = (0, 127, 0)
dpurple = (127, 0, 127)

set_backdrop(black)

inv_panel_backdrop = dgray
inv_panel_slots = lgray