import pygame
import time

class ModRegistry:

	def __init__(self, *files):
		self.data = {}
		self.img_ext = ".png"
		for name in files:
			self.load_spritesheet(name)

	def __getitem__(self, index):
		return self.data[index]
	def __setitem__(self, index, val):
		self.data[index] = val

	def load(self, file):
		self[file] = pygame.image.load(self.genpath(file))





def dbg_show(img_reg):
	pygame.init();screen=pygame.display.set_mode(img.get_size());screen.blit(img_reg,(0,0));pygame.display.flip();time.sleep(2)