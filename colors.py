def complement(color):
	return tuple(abs(255-el) for el in color)

def set_backdrop(color):
	global backdrop; global text
	backdrop = color; text = complement(backdrop)

# (R, G, B)

black = (0, 0, 0)
white = (255, 255, 255)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

orange = (255, 255, 0)
cyan = (0, 255, 255)
purple = (255, 0, 255)

navy = (0, 0, 64)
dgreen = (0, 128, 0)
lblue = (192, 192, 255)
dpurple = (128, 0, 128)
lgray = (192, 192, 192)
dgray = (128, 128, 128)

backdrop = black
text = complement(backdrop)