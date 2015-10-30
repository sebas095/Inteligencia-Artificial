import re
import random

class ELIZA(object):
	def __init__(self):
		self.keys = map(lambda x: re.compile(x[0], re.INGNORECASE), gPats)
		self.values = map(lambda x: x[1], gPats)

	#take a string and replace any input word(dict.keys()) for its asnwer in dict.values()
	#para caro: tomar una cadena, reemplazar cualquier palabra en entrada en dict.keys() por su correspondiente dict.values()
	def translate(self, str, dict):
		words = string.split(string.lower(st))
		keys = dict.keys()
		for i in range(len(words)):
			if words[i] in keys:
				words[i] = dict[words[i]]
			return string.join(words)

	def respond(self, str):
		#encontrar coincidencias
		for i in range(len(self.keys)):
			match = self.keys[i].match(str)
			if match:
				#int ()
				resp = random.choice(self.values[i])
				pos = string.find(resp, '%')
				while pos > -1:
					num = string.atoi(resp[pos+1:pos+2])
					resp = resp[:pos] + self.translate(match.group(num), gReflections)+resp[pos+2:]
					pos = string.find(resp, '%')
				if resp[-2:] == '?.': resp = resp[:-2]+'.'
				if resp[-2:] == '??': resp = resp[:-2]+'?'
				return resp

	def command_interface():
		print "hola _"
		s = ''
		therapist = ELIZA()
		while s != 'salir':
			try: raw_input(">")
			except EOFError:
				S = 'SALIR'
				print s
			while s[-1] in '!.': s = [:-1]
			print therapist.respond(s)

