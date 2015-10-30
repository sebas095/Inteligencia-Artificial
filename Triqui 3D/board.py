import copy

class Board (object):

	def __init__(self):
		self.board = [['.','.','.'],['.','.','.'],['.','.','.']]

	def put(self,i,j,element):
		self.board[i][j] = element

	def isAllow(self,i,j):
		if i<0 or j <0 or i>2 or j>2:  
			return False
		if self.board[i][j] != '.':
			return False
		return True

	def isFull(self):
		for i in range(3):
			for j in range(3):
				if self.board[i][j] == '.':
					return False
		return True

	def succesors(self, element):
		succesors = []
		for i in range(3):
			for j in range(3):
				if self.board[i][j] == '.':
					tmp = []
					tmp = copy.deepcopy(self.board)
					tmp[i][j] = element
					succesors.append(tmp)
		return succesors

	def mostrar(self):
		vecinos = self.succesors('X')
		print "Original:"
		for i in range(3):
			aux = ""
			for j in range(3):
				aux += self.board[i][j]+" "
			print aux

		print "Vecinos:"
		for k in range(len(vecinos)):
			print
			s = ""
			for i in range(3):
				s = ""
				for j in range(3):
					s += vecinos[k][i][j]+" "
				print s

	def __str__(self):
		s = ""
		for i in range(3):
			for j in range(3):
				if self.board[i][j] == '.':
					if i<2:
						s+= "__"
					else:
						s+= "  "
				elif self.board[i][j] != '.':
					if i<2:
						s+='_' 
					else:
						s+=' '
					s += self.board[i][j]
				if j<2:
					s+='|'
			s +='\n'
		return s

  