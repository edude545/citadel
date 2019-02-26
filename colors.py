def complement(color):
	return (255-color[0], 255-color[1], 255-color[2])



black = (0, 0, 0)
white = (255, 255, 255)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)



backdrop = black
text = complement(backdrop)


def change_backdrop(color):
	global backdrop; global text
	backdrop = color; text = complement(backdrop)