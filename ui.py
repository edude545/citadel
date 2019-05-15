import pygame
import colors

font_height = 10
do_antialias = True

pygame.font.init()
default_font = pygame.font.Font(pygame.font.get_default_font(), font_height)


def common_draw(self, surface, dest):
	surface.blit(self.render(), dest)
def qrender(text):
	return default_font.render(text, do_antialias, colors.text)


class UIElement:
	draw = common_draw
	def __init__(self):
		self.hidden = False
	def toggle_visibility(self):
		self.hidden = not self.hidden


class Monitor(UIElement):

	def __init__(self, func, pos=None):
		super().__init__()
		self.func = func
		self.height = font_height + 2
		self.pos = pos

	def render(self):
		return qrender(str(self.func()))