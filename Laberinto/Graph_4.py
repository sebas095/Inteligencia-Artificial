# UNIVERSIDAD TECNOLOGICA DE PEREIRA
# TALLER #1 DE IA
# SEBASTIAN DUQUE RESTREPO
# 1112783873

from collections import deque
from random import shuffle, randrange
import copy
 
lab = []

def make_maze(w = 16, h = 8):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]
 
    def walk(x, y):
        vis[y][x] = 1
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)
 
    walk(randrange(w), randrange(h))
    for (a, b) in zip(hor, ver):
        lab.append(str(''.join(a + ['s'] + b)))
 
def matrix_maze():
    make_maze()
    maze = {}
    contx = 0
    conty = 0
    countF = 0
    flag = True
    for i in range(len(lab)):
        maze[contx] = {}
        for j in range(len(lab[i])):
            if lab[i][j] == 's':
                contx += 1
                maze[contx] = {}
                conty = 0
                flag = False
                continue
            maze[contx][conty] = lab[i][j]
            conty +=1
            if flag:
                countF +=1
        contx += 1
        conty = 0
        flag = False

    x = len(maze.keys())
    y = len(maze[0])
    maze[1][0] = 'I' # Representa el inicio del laberinto
    maze[x-3][y-1] = 'F' #Representa la salida del laberinto
    return maze

def view_maze(maze):
	s = ""
	for i in maze:
		for j in maze[i]:
			s += maze[i][j]
		print s
		s = ""

def inic(l,value, h=18, w=49):
	aux = []
	for i in range(h):
		for j in range(w):
			aux.append(value)
		l.append(aux)
		aux = []

class Graph:
	def __init__(self, v):
		self.v = v
		self.adj = {}
		for i in range(v):
			self.adj[i] = {}
	
	def addEdge(self,v,w):
		self.adj[v][w] = 1
		self.adj[w][v] = 1

	def adjacents(self,v):
		return self.adj[v]

class DFS:
	def __init__(self,G,x,y,prev,maze,h=18,w=49):
		self.marked = []
		self.path = []
		inic(self.marked,False)
		self.dfs(G,x,y,prev,maze,h,w)

	def dfs(self,G,x,y,prev,maze,h,w):
		dx = [0, 0, 1, -1 ] #incremento en coordenada x
		dy = [1, -1, 0, 0 ] #incremento en coordenada y
		stack = []
		stack.append([x,y,-1])
		inic(prev,[-2,-2,-2])
		prev[x][y] = [-1,-1,-1]
		while stack:
			current = stack.pop()
			self.path.append(current)
			if G.adj[current[0]][current[1]] == 'F':
				self.pprint(current[0],current[1],prev,maze)
				break
			self.marked[current[0]][current[1]] = True
			for i in range(4):
				nx = dx[i] + current[0]
				ny = dy[i] + current[1]
				if nx>=0 and nx<h and ny>=0 and ny<w and not G.adj[nx][ny]=='0' and not self.marked[nx][ny]:
					stack.append([nx,ny,0])
					prev[nx][ny] = current

	def pprint(self,x,y,prev,maze):
		maze[1][1] = '*'
		i = x
		j = y
		print prev[i][j][2]
		while not prev[i][j][2] == -1:
			if maze[i][j] != 'F':
				maze[i][j] = '*'
			x = i
			y = j
			i = prev[x][y][0]
			j = prev[x][y][1]		
		view_maze(maze)


class BFS:
	def __init__(self,G,x,y,prev,maze,h=18,w=49):
		self.marked = []
		self.bfs(G,x,y,prev,maze,h,w)

	def bfs(self,G,x,y,prev,maze,h,w):
		dx = [0, 0, 1, -1 ] #incremento en coordenada x
		dy = [1, -1, 0, 0 ] #incremento en coordenada y
		inicial = [x,y,0]
		q = deque()
		q.append(inicial)
		inic(self.marked,False)
		inic(prev,[-2,-2,-2])
		prev[x][y] = [-1,-1,-1]
		while q:
			visited = q.pop()
			if G.adj[visited[0]][visited[1]] == 'F':
				self.pprint(visited[0],visited[1],prev,maze)
				return visited[2]
			self.marked[visited[0]][visited[1]] = True
			for i in range(4):
				nx = dx[i] + visited[0]
				ny = dy[i] + visited[1]
				if nx>=0 and nx<h and ny>=0 and ny<w and not G.adj[nx][ny]=='0' and not self.marked[nx][ny]:
					adyacente = [nx,ny, visited[2]+1]
					q.append(adyacente)
					prev[nx][ny] = visited
		return -1			

	def pprint(self,x,y,prev,maze):
		i = x
		j = y
		print prev[i][j][2]
		while not prev[i][j][2] == -1:
			if maze[i][j] != 'F':
				maze[i][j] = 'O'
			x = i
			y = j
			i = prev[x][y][0]
			j = prev[x][y][1]		
		view_maze(maze)

		
def convertToGraph(G, maze):
	G.adj = copy.deepcopy(maze)
	for i in G.adj:
		for j in G.adj[i]:
			if G.adj[i][j] == ' ':
				G.adj[i][j] = '1' #representa una arista de i->j
				continue
			elif G.adj[i][j] != 'I' and G.adj[i][j] != 'F':
				G.adj[i][j] = '0'


#Guardar la ruta en BFS
prev = []
prev2 = []
#Inicializar el grafo
#1 0 ---> posicion de inicio
#15 48 --> posicion final
g = Graph(17)
maze1 = matrix_maze()
maze2 = copy.deepcopy(maze1)
convertToGraph(g,maze1)
print "LABERINTO ORIGINAL: "
view_maze(maze1)
print "BFS:"
print "Pasos recorridos para salir del laberinto: "
bfs = BFS(g,1,0,prev,maze1)
print "DFS:"
dfs = DFS(g,1,0,prev2,maze2)
		
