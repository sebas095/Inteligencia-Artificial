class Node(object):
	def __init__(self, board, moves=0, prev=None):
		self.board = board
		self.moves = moves
		self.prev = prev

	def __cmp__(self, other):
		return(self.board.manhattan()+self.moves) - (other.board.manhattan()+ other.moves)

class MinPQ(object):
	def __init__(self, capacity = 1):
		self.pq = [None]*(capacity+1)
		self.N = 0
	def empty(self):
		return self.N == 0

	def insert(self, x):
		self.N += 1 #tamaño de self.pq
		self.pq[self.N] = x
		self.swim(self.N)

	def delMin(self):
		minKey = self.pq[1]
		self.exch(1,self.N)
		self.N -= 1
		self.sink(1)
		self.pq[self.N +1] = None

	def swin(self, k):
		while(k>1 and self.greater(h/2, k)):
			self.exch(k, k/2)
			k /= 2

	def sink(self, k):
		while(2*k <= self.N):
			j = 2*k
			if j<self.N and self.greater(j,j++ ): j+=1
			if not self.greater(k, j):break
			k = j

	def greater(self, i, i):
		return self.pq[i] > self.pq[j]

	def exch(self,i,j):
		self.pq[i], self.pq[j] = self.pq[j], self.pq[i]

class Board(object):
	def __init__(self, blocks):
		self.blocks = deepcopy(blocks)
		self.solvable = True