import random

# vowels are False
# consonants are True

# 4 types of phonemes:
# ff:  v -> p -> v
# ft:  v -> p -> v
# tf:  c -> p -> v
# tt:  c -> p -> c

class Phonology:

	def __init__(self, length, vowels, consonants):
		self.length = length
		self.vowels = vowels
		self.consonants = consonants

	def generate_name(self):
		r = [random.choice(self.vowels+self.consonants)]

		for i in range(self.length):
			if r[-1] in self.consonants:
				r.append(random.choice(self.vowels))
			else:
				r.append(random.choice(self.consonants))

		return "".join(r)


v = False
c = True

dwemer = Phonology(5,("nch","k","bth","bthz","th","z","zh","gr"),("a","u","e"),)
dunmer = Phonology(4,("v","hl","d","gn","s","n","l","k","m","nn"),("aa","u","o","e"))
altmer = Phonology(6,("w","w","w","n","l","l","c","cl","n"),("a","aa","e","o","i"))
wizard = Phonology(6,("zz","zz","z","z","v","x","n","jj","j","sh"),("a","a","a","aa","uu","oo","o","i","ii","ai","ei"))
phoenix = Phonology(3,("q","k","qu","p","ph","phaib","beim","m","minim","laram","cyl"),("a","a","a","y","i","e"))

def preview(p):
	for i in range(4): print(p.generate_name(),end="   ")
	print("")

preview(dwemer)
preview(dunmer)
preview(altmer)
preview(wizard)
preview(phoenix)