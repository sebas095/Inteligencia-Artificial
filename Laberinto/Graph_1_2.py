from collections import deque

class Graph:
	def __init__(self, v):
		self.v = v
		self.adj = {}
		for i in range(v):
			self.adj[i] = set([])
	
	def addEdge(self,v,w):
		self.adj[v].add(w)
		self.adj[w].add(v)

	def adjacents(self,v):
		return self.adj[v]

class DFS:
	def __init__(self, G, s, t):
		self.marked = []
		self.path = []
		for i in range(G.v):
			self.marked.append(False) 
		self.path.append(s)
		self.marked[s] = True
		self.dfs(G,s, t)

	def dfs(self,G,v,t):
		flag = False
		for w in G.adjacents(v):
			if not self.marked[w]:
				self.marked[w] = True
				self.path.append(w)
				if w == t:
					return True
				else:
					flag = self.dfs(G,w,t)
					if not flag:
						self.path.pop()
		return flag


class BFS:
	def __init__(self,G,s,t):
		self.marked = []
		self.path = []
		for i in range(G.v):
			self.marked.append(False) 
		self.path.append(s)
		self.marked[s] = True
		self.bfs(G,s,t)

	def bfs(self,G,v,t):
		q = deque()
		q.append(v)

		while q:
			visited = q.pop()
			for w in G.adjacents(visited):
				if not self.marked[w]:
					self.marked[w] = True
					self.path.append(w)
					q.append(w)
					if w == t:
						return




g = Graph(13)
g.addEdge(0,5)
g.addEdge(4,3)
g.addEdge(0,1)
g.addEdge(9,12)
g.addEdge(6,4)
g.addEdge(5,4)
g.addEdge(0,2)
g.addEdge(11,12)
g.addEdge(9,10)
g.addEdge(0,6)
g.addEdge(7,8)
g.addEdge(9,11)
g.addEdge(5,3)

dfs = DFS(g,0, 4)
print "DFS path:",dfs.path

bfs = BFS(g,0,4)
print "BFS path:",bfs.path
		
