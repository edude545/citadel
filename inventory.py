class Inventory(list):

	# Extends list to act as an array of ItemStacks

	def __init__(self, size):
		self.size = size # :: int
		self.add_stack(size)

	def __repr__(self):
		return "Inventory"+super().__repr__()
	__str__ = __repr__

	def add_stack(self, n=1):
		for i in range(n):
			self.append(ItemStack())

	def add(self, item, n=1): # add to earliest valid itemstack in inventory, return indicates if the items were successfully added (UNFINISHED)
		for stack in self:
			if stack.matches(item) or stack.matches(None):
				stack.add(n,item=item); return
		self.add_stack(); self[-1].add(n)

	def add_to_slot(self, index, item, n):
		self[index].add(n, item=item)

	def remove(self, item, n=1): # remove n from the last instance of itemstack of "item" in inventory
		pass

	def remove_from_slot(self, index, item, n):
		pass # NYI

	def get_amount(self, item=None):
		pass # NYI

	def get_free_space(self):
		pass # NYI

	def get_size(self):
		return self.size


class ItemStack:

	max_size = -1

	def __init__(self, item=None, count=0):
		self.item = item
		self.count = count

	def __repr__(self):
		if self.item is None:
			return "____"
		return str(self.count) + "*" + str(self.item)
	__str__ = __repr__

	# ~~~ ~~~ v Attribute access

	def get_item(self):
		return self.item
	def set_item(self, item):
		self.item = item
	def is_empty(self):
		return self.matches(None)

	def get_count(self):
		return self.count
	def set_count(self, n):
		self.count = n
	def change_count(self, n):
		self.count += n

	def matches(self, item):
		return self.item == item

	def can_merge_with(self, stack):
		return self.get_item() == stack.get_item() or self.is_empty() or stack.is_empty()

	def get_max_size(self):
		return self.max_size

	# ~~~ ~~~ v Item management

	def add(self, n, item=None): # returns number of items that were successfully added
		if item is None: item = self.item
		if self.item is None:
			self.set_item(item)
		self.change_count(n)

	def remove(self, n):
		self.change_count(-n)
		if self.count < 0:
			self.set_count(0)

	def sort(self):
		pass # NYI

	def merge(self, stack): # no checking - use can_merge_with first
		if self.is_empty():
			self.set_item(stack.get_item())
		self.add(stack.get_count())

	def clear(self):
		self.set_item(None)
		self.set_count(0)