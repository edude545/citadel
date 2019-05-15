import vector as v

def direction_int_to_vector(n):
	if n == 0: # south
		return v.Vector(0,1)
	elif n == 1: # west
		return v.Vector(-1,0)
	elif n == 2: # north
		return v.Vector(0,-1)
	elif n == 3: # east
		return v.Vector(1,0)
	raise ValueError("direction_int_to_vector expects integer between 0 and 3")