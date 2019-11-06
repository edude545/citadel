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



def smartcast(val):
	if "." in val:
		try: return float(val)
		except ValueError: pass
	try: return int(val)
	except ValueError: pass
	return val


keyboard_replace_dict = {
	"<":"\\",
	"\\":"#",
}
keyboard_shift_dict = {
	"`":"¬","1":"!","2":"\"","3":"£","4":"$","5":"%","6":"^","7":"&","8":"*","9":"(","0":")","-":"_","=":"+",
	"[":"{","]":"}",
	";":":","'":"@","#":"~",
	"\\":"|",",":"<",".":">","/":"?",
}