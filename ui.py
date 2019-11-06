import pygame
import colors

font_height = 10
do_antialias = True

pygame.font.init()
default_font = pygame.font.Font(pygame.font.get_default_font(), font_height)


def common_draw(self, surface, dest):
	surface.blit(self.render(), dest)
def qrender(text,color=colors.text):
	return default_font.render(text, do_antialias, color)


class UIElement:
	draw = common_draw
	def __init__(self,pos=None):
		# Given attribute game
		self.hidden = False
		self.pos = pos
		if self.pos is not None:
			size = self.render().get_size()
			self.bound = (pos[0]+size[0],pos[1]+size[1])
	def on_click(self,button,pos): # 1 is LMB, 3 is RMB
		pass
	def toggle_visibility(self):
		self.hidden = not self.hidden
	def in_bounds(self,pos): # don't call this unless the element has a specified pos
		return self.pos[0] <= pos[0] <= self.bound[0] and self.pos[1] <= pos[1] <= self.bound[1]

class Monitor(UIElement):
	height = font_height + 2
	def __init__(self, func, pos=None):
		self.func = func
		super().__init__(pos=pos)

	def render(self):
		return qrender(str(self.func()))

class ItemStackPanel(UIElement):

	slot_width = 32
	slot_height = 32

	def __init__(self, inventory, index, pos=None):
		self.inventory = inventory
		self.index = index
		self.stack = self.get_stack()
		super().__init__(pos=pos)

	def render(self):
		base = pygame.surface.Surface((self.slot_width,self.slot_height))
		base.fill(colors.inv_panel_slots, (0, 0, self.slot_width, self.slot_height))
		if not self.stack.is_empty():
			base.blit(qrender(str(self.stack.get_item()),color=colors.black),(1,1))
			base.blit(qrender(str(self.stack.get_count()),color=colors.black),(1,self.slot_height-10))
		return base

	def get_stack(self):
		return self.inventory[self.index]

class InventoryPanel(UIElement):

	gap = 4

	def __init__(self, inventory, size, pos=None):
		self.size = size # :: w,h in slots
		self.slot_panels = [] # :: [(ItemStackPanel, (sx,sy))]
		self.inventory = inventory

		slots,x,y = 0,self.gap,self.gap
		i = 0
		for slot_pos in self.iter_slot_pos():
			self.slot_panels.append((ItemStackPanel(self.inventory,i),slot_pos))
			i += 1
			if i == len(self.inventory): break

		self.height = self.size[1] + 2
		super().__init__(pos=pos)

	def iter_slot_pos(self):
		x,y = 0,0
		while y <= self.size[1]:
			yield (self.gap+x*(ItemStackPanel.slot_width+self.gap),self.gap+y*(ItemStackPanel.slot_height+self.gap))
			x += 1
			if x == self.size[0]:
				x = 0; y += 1

	def on_click(self,button,pos):
		x,y = 0,0
		for pair in self.slot_panels: # (slot, (x,y))
			ex,ey=(x+1)*(ItemStackPanel.slot_width+self.gap),(y+1)*(ItemStackPanel.slot_height+self.gap)
			if pair[1][0] <= pos[0] <= ex and pair[1][1] <= pos[1] <= ey:
				if self.game.cursor_has_item() and pair[0].get_stack().can_merge_with(self.game.cursor_itemstack_panel.get_stack()) and pair[0] is not self.game.cursor_itemstack_panel:
					pair[0].get_stack().merge(self.game.cursor_itemstack_panel.get_stack())
					self.game.cursor_itemstack_panel.get_stack().clear()
					self.game.cursor_cancel()
				elif not pair[0].get_stack().is_empty():
					self.game.cursor_pickup(pair[0])
				break
			x += 1
			if x == self.size[0]:
				x=0;y+=1

	def render(self):
		base = pygame.surface.Surface((self.size[0]*(ItemStackPanel.slot_width+self.gap)+self.gap,self.size[1]*(ItemStackPanel.slot_height+self.gap)+self.gap))
		base.fill(colors.inv_panel_backdrop)
		x,y = self.gap,self.gap
		for pair in self.slot_panels:
			base.blit(pair[0].render(),pair[1])
		return base