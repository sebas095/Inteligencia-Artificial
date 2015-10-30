# solucion de un puzzle implementando A* 
# Fecha: 14/09/2015
# Autores:
# Leiver Andres Campeon B.
# Sebastian Duque Restrepo
# version: 5.0

import copy
from Queue import PriorityQueue

class Board(object):

	def __init__(self, blocks):
		self.blocks = copy.deepcopy(blocks)


	def size(self):
		return len(self.blocks)

	def hamming(self):
		hamming = 0
		pos = 1
		for i in range(self.size()):
			for j in range(self.size()):
				if self.blocks[i][j] != 0 and self.blocks[i][j] != pos:
					hamming += 1
				pos += 1
		return hamming

	def manhattan(self):
		manhattan = 0
		for i in range(self.size()):
			for j in range(self.size()):
				if self.blocks[i][j] == 0: continue
				row = (self.blocks[i][j] - 1) / self.size()
				col = (self.blocks[i][j] - 1) - self.size() * row
				manhattan += abs(row - i) + abs(col - j)
		return manhattan

	def isGoal(self):
		return self.manhattan() == 0

	def invCount(self):
		inversions = 0
		m = []
		for i in range(self.size()):
			for j in range(self.size()):
				m.append(self.blocks[i][j])
				
		for i in range(len(m)):
			for j in range(i+1,len(m)):
				if(m[i] and m[j]) and m[i] > m[j]:
					inversions += 1
		return inversions
		
	def isSolvable(self):
		cont = self.invCount()
		return cont%2 == 0

	def equal(self, prev):
		if type(prev) == dict:
			for i in prev:
				if prev[i].blocks == self.blocks:
					return True
		else:
			for i in prev:
				if i.blocks == self.blocks:
					return True
		return False


	def neighbors(self):
		aux = PriorityQueue()
		neighbors = []
		dx = [0, 0, 1, -1 ]
		dy = [1, -1, 0, 0 ]
		posx = 0
		posy = 0
		for i in range(self.size()):
			for j in range(self.size()):
				if self.blocks[i][j] == 0:
					posx = i
					posy = j
					break

		for k in range(4):
			nx = posx + dx[k]
			ny = posy + dy[k]
			if nx >= 0 and nx < self.size() and ny >= 0 and ny < self.size():
				tmp = copy.deepcopy(self.blocks)
				tmp[posx][posy] = tmp[nx][ny]
				tmp[nx][ny] = 0
				b = Board(tmp)
				aux.put((b.hamming(),b))

		while not aux.empty():
			neighbors.append(aux.get()[1])
		return neighbors


	def __str__(self):
		out = ""#'%r\n\n' % self.size()
		for i in range(self.size()):
			for j in range(self.size()):                
				out += ' %r' % self.blocks[i][j] if self.blocks[i][j] != 0 else '  ' 
			out += '\n'
		return out

class Solver(object):

	def __init__(self, board):
		self.steps = []
		self.state = board


	def sacar(self, elem, lista):
		li_tmp = []
		for x in lista:
			if x != elem:
				li_tmp.append(x)

		lista = li_tmp

	def solution(self):    
		opened = [self.state]
		closed = []
		norepeat = []
		q = PriorityQueue()
		#tableros solucion, pasos
		cero = Board([[0,0,0],[0,0,0],[0,0,0]])
		path = {}
		path[self.state] = cero
		level = 0
		q.put(((level,self.state.hamming()-level),self.state))
		while not q.empty():
			current = q.get()
			opened.remove(current[1])

			if current[1].isSolvable():
				if current[1].isGoal():
					x = current[1]
					tam = 0
					solve = copy.deepcopy(x)
					self.steps.append(solve)
					while path[x] != cero:
						self.steps.append(path[x])
						x = path[x]
						tam += 1

					step = 0
					print "TABLERO: "
					print self.steps.pop()
					while self.steps:
						step += 1
						print "Step ",step,":"
						print self.steps.pop()
					return True

				else:
					for succesor in current[1].neighbors():
						if not succesor.equal(norepeat) and succesor.isSolvable() and (not succesor.equal(opened) and not succesor.equal(closed)) and not succesor.equal(path):
							norepeat.append(succesor)
							path[succesor] = current[1]
							opened.append(succesor)
							q.put(((current[0][1] + 1,(succesor.hamming()-(current[0][1] + 1))), succesor))
					
					closed.append(current[1])

		print "No es solucionable"

def read():
	# recibimos la longitud del tablero NxN
	n = int(input())
	tmp = []
	table = []
	#entrada por teclado o archivo:
	for i in range(n):
		tmp.append(raw_input())

	#convertimos el string a una matriz por ahora de caracteres
	for i in range(len(tmp)):
		table.append(tmp[i].split(" "))
	
	#casteamos los caracteres a enteros
	for i in range(len(table)):
		for j in range(len(table[i])):
			aux = int(table[i][j])
			table[i][j] = aux

	return table
	
if __name__ == '__main__':
	import sys
	# Lectura por teclado o archivo:
	#b = Board(read())
	# # faciles
	# b = Board([[2,8,3],[1,6,4],[7,0,5]])
	# b = Board([[0,2,3],[1,4,6],[7,5,8]])
	# b = Board([[0,1,3],[4,2,5],[7,8,6]])
	# b = Board([[1,8,2],[0,4,3],[7,6,5]])
	# b = Board([[2,8,3],[1,6,4],[7,0,5]])
	#No solucionables 
	# b = Board([[1,2,3],[4,5,6],[8,7,0]])

	#puzzles mas dificiles:
	b = Board([[8,6,7],[2,5,4],[3,0,1]])
	# b = Board([[6,0,5],[8,7,4],[3,2,1]])
	# b = Board([[7,2,4],[5,0,6],[8,3,1]])
	# b = Board([[6,0,5],[8,7,4],[3,2,1]])
	# b = Board([[2,9,3,5],[8,11,12,7],[15,4,0,13],[6,1,10,14]])
	# b = Board([[15,3,7,13],
	# 		   [11,8,2,4],
	# 		   [6,10,5,0],
	# 		   [9,12,14,1]])
	sol = Solver(b)
	#print b.isSolvable()
	sol.solution()