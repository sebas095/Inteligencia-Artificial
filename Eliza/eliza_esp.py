# -*- coding: utf-8 -*-
import string
import re
import random
import knowledge_base as kb 

class Eliza(object):

	def __init__(self):
		self.keys = map(lambda x: re.compile(x[0], re.IGNORECASE), gPats)
		self.values = map(lambda x: x[1], gPats)

	def translate(self, str, dict):
		words = string.split(string.lower(str))
		keys = dict.keys()
		for i in range(len(words)):
			if words[i] in keys:
				words[i] = dict[words[i]]
		return string.join(words)

	def respond(self, str):
		for i in range(len(self.keys)):
			match = self.keys[i].match(str)
			if match:
				resp = random.choice(self.values[i])
				pos = string.find(resp,'%')
				while pos > -1:
					num = string.atoi(resp[pos+1 : pos+2])
					resp = resp[:pos] + self.translate(match.group(num), gReflections) + resp[pos+2 :]
					pos = string.find(resp,'%')
				if resp[-2:] == '?.': resp = resp[:-2] + '.'
				if resp[-2:] == '??': resp = resp[:-2] + '?'
				return resp

gReflections = kb.verbs
gPats = kb.queries

def begin_chat():
	#DATOS --> http://deixilabs.com/elizadata.js
	#      --> http://deixilabs.com/aliziadata.js
	print "\n\t\t\t\t  ELIZA\n"
	print "|"+"="*75+"|"
	print '|  Charla con ELIZA en español de lo que desees.'+(' '*27)+'|'
	print "|"+'='*75+"|"	
	print "\nELIZA:  Hola. ¿Como te sientes hoy?"
	s = ""
	terapista = Eliza()
	while s.lower() != 'salir':
		try:
			s = raw_input("TÚ:    ")
		except EOFError:
			s = "salir"
			print s
		while s[-1] in "!.": s = s[:-1]
		print "ELIZA:  "+terapista.respond(s)

if __name__ == "__main__":
	begin_chat()