from triqui import *

formato = '''         _____________
        / 1 / 2 / 3 / |
       /___/___/___/  |
      / 4 / 5 / 6 /   |    <-- TOP(1)
     /___/___/___/    |
    / 7 / 8 / 9 /     |
   /___/___/___/      |
   |       |___|______|
   |      / 11 /|12 / 13 /
   |     /___/_|_/___/|
   |    / 14 / 15|/ 16 / |    <-- MIDDLE(2)
   |   /___/___|___/  |
   |  / 17 / 18 /|19 /   |
   |_/___/___/_|_/    |
   |     |_____|______|
   |     / 21 / |22 / 23 /
   |    /___/__|_/___/ 
   |   / 24 / 25 |/ 26 /      <-- BOTTOM(3)
   |  /___/____|___/   
   | / 27 / 28 / |29 /    
   |/___/___/__|_/'''  

class Triqui3D (object):

	def __init__(self):
		#self.sheet = 1 # 1:top 2:middle 3;bottom
		self.top = Triqui()
		self.middle = Triqui()
		self.bottom = Triqui()
		self.state = [self.top, self.middle, self.bottom]
		self.player = 1  #Human:1 Machine:0
		self.ganador = -1 #Human:1 Machine:2 Empate:0
		self.tabHuman = 'O'
		self.tabMachine = 'X'
		self.level = 0 # Level: 0 Facil, Level: 1 Dificil
		self.turn = 0 # Turno: 0 juega primero el humano, Turno: 1 juega primero la maquina

	def __str__(self):
		#Para modificar formato
		draw = formato

		top = self.top.table.board
		middle = self.middle.table.board
		bottom = self.bottom.table.board

		#TOP
		for i in range(3):
			for j in range(3):
				draw = draw.replace(str((j+1)+(3*i)),top[i][j],1)
				if top[i][j] == '.':
					draw = draw.replace('.',' ',1)
		#MIDDLE
		for i in range(3):
			for j in range(3):
				draw = draw.replace(str((j+1)+(3*i)+10),middle[i][j],1)
				if middle[i][j] == '.':
					draw = draw.replace('.',' ',1)
		#BOTTOM
		for i in range(3):
			for j in range(3):
				draw = draw.replace(str((j+1)+(3*i)+20),bottom[i][j],1)
				if bottom[i][j] == '.':
					draw = draw.replace('.',' ',1)

		return draw


	def put(self, sheet,i,j,element):
		self.getBoards(sheet).table.board[i][j] = element

	def getBoards(self, sheet):
		if sheet == 1:
			return self.top
		if sheet == 2:
			return self.middle
		if sheet == 3:
			return self.bottom

	def firstTurn(self):
		l = raw_input("Elija nivel de dificultad (FACIL/DIFICIL)o(F/D): ")
		l = l.upper()
		if l == "FACIL" or l == "F":
			self.level = 0
		if l == "DIFICIL" or l == "D":
			self.level = 1
		msj = raw_input("Desea hacer la primera jugada? (S/N): ")
		if msj.upper() == 'S' or msj.upper() == 'SI':
			self.turn = 0 #Inicia el humano
			self.chooseTab()
		else:
			self.turn = 1 #Inicia la maquina

	def chooseTab(self):
		if self.turn == 0:
			tab = raw_input("Elija el simbolo con el que desea jugar X/O: ")
			if tab.upper() == 'X':
				self.tabHuman = 'X'
				self.tabMachine = 'O'
		else:
			self.tabHuman = 'O'
			self.tabMachine = 'X'

	def isAllow(self,sheet,i,j):
		if i<0 or j <0 or i>2 or j>2 or sheet<1 or sheet>3:  
			return False
		if self.getBoards(sheet).table.board[i][j] != '.':
			return False
		return True

	def checkMove(self):
		pos = self.read()
		sheet = pos[0]
		i = pos[1]
		j = pos[2]
		if self.isAllow(sheet,i,j):
			if self.moveHuman(sheet,i,j):
				return
		else:
			print "En el tablero ",sheet," la posicion ",i," ",j," no se encuentra disponible, intente de nuevo:\n"
			pos = self.read()
			sheet = pos[0]
			i = pos[1]
			j = pos[2]
			while not self.isAllow(sheet,i,j):
				print "En el tablero ",sheet," la posicion ",i," ",j," no se encuentra disponible, intente de nuevo:\n"
				pos = self.read()
				sheet = pos[0]
				i = pos[1]
				j = pos[2]
			self.moveHuman(sheet,i,j)

	def moveRandom(self):
		sheet = random.randint(1,3)
		i = random.randint(0,2)
		j = random.randint(0,2)
		while not self.isAllow(sheet,i,j):
			sheet = random.randint(1,3)
			i = random.randint(0,2)
			j = random.randint(0,2)
		self.movePC(sheet,i,j)

	def moveHuman(self,sheet,i,j):
		os.system('cls')
		self.put(sheet,i,j,self.tabHuman)
		print self.__str__()

	def win_capa(self, capa, symbol):
		#diagonales
		if capa[0][0] == symbol and capa[1][1] == symbol and capa[2][2] == symbol:
			# print True
			return True
		elif capa[2][0] == symbol and capa[1][1] == symbol and capa[0][2] == symbol:
			# print True
			return True
		#filas
		elif capa[0][0] == symbol and capa[0][1] == symbol and capa[0][2] == symbol:
			# print True
			return True
		elif capa[1][0] == symbol and capa[1][1] == symbol and capa[1][2] == symbol:
			# print True
			return True
		elif capa[2][0] == symbol and capa[2][1] == symbol and capa[2][2] == symbol:
			# print True
			return True
		#columnas
		elif capa[0][0] == symbol and capa[1][0] == symbol and capa[2][0] == symbol:
			# print True
			return True
		elif capa[0][1] == symbol and capa[1][1] == symbol and capa[2][1] == symbol:
			# print True
			return True
		elif capa[0][2] == symbol and capa[1][2] == symbol and board[2][2] == symbol:
			# print True
			return True
		else: 
			# print False
			return False

	def win(self, state,symbol):
		if self.win_capa(state[0],symbol) or self.win_capa(state[1],symbol) or self.win_capa(state[2],symbol):
			return True
		 
		for i in range(3):
			for j in range(3):
				if state[0][i][j] == symbol and state[1][i][j] == symbol and state[2][i][j] == symbol:
					return True
		if state[0][0][0] == symbol and state[1][1][1] == symbol and state[2][2][2] == symbol:
			return True
		if state[0][0][0] == symbol and state[1][0][1] == symbol and state[2][0][2] == symbol:
			return True
		if state[0][0][0] == symbol and state[1][1][0] == symbol and state[2][2][0] == symbol:
			return True
		if state[0][0][1] == symbol and state[1][1][1] == symbol and state[2][2][1] == symbol:
			return True
		if state[0][0][2] == symbol and state[1][1][1] == symbol and state[2][2][0] == symbol:
			return True
		if state[0][0][2] == symbol and state[1][0][1] == symbol and state[2][0][0] == symbol:
			return True
		if state[0][0][2] == symbol and state[1][1][2] == symbol and state[2][2][2] == symbol:
			return True
		if state[0][1][2] == symbol and state[1][1][1] == symbol and state[2][1][0] == symbol:
			return True
		if state[0][2][2] == symbol and state[1][1][1] == symbol and state[2][0][0] == symbol:
			return True
		if state[0][2][2] == symbol and state[1][2][1] == symbol and state[2][2][0] == symbol:
			return True
		if state[0][2][1] == symbol and state[1][1][1] == symbol and state[2][0][1] == symbol:
			return True
		if state[0][2][0] == symbol and state[1][1][1] == symbol and state[2][0][2] == symbol:
			return True
		if state[0][2][0] == symbol and state[1][1][0] == symbol and state[2][0][0] == symbol:
			return True
		if state[0][2][0] == symbol and state[1][2][1] == symbol and state[2][2][2] == symbol:
			return True
		if state[0][1][0] == symbol and state[1][1][1] == symbol and state[2][1][2] == symbol:
			return True
		else:
			return False 

	def getSuccesors(self, state, symbol):
		lista = []
		superior = []
		medio = []
		bottom = []
		tmp = [superior, medio, bottom]

		for z in range(3):
			for i in range(3):
				for j in range(3):
					if state[z][i][j] == ".":
						state[z][i][j] = symbol
						tmp = [state[0], state[1], state[2]]
						state[z][i][j] = "."
						lista.append(tmp)

		return lista

	# state terna
	def minimax(self, state, player, alpha, beta):
		if self.win(state, self.tabMachine):
			return 1
		if self.win(state, self.tabHuman):
			return -1
		# player en 1 hace max
		if player:
			for each in self.getSuccesors(state, self.tabMachine):
				aux = self.minimax(each, False, alpha, beta)
				if aux > alpha:
					alpha = aux
					if beta <= alpha:
						return beta
			return alpha
		else:
			for each in self.getSuccesors(state, self.tabHuman):
				aux = self.minimax(each, True, alpha, beta)
				if aux < beta:
					beta = aux
					if alpha >= beta:
						return alpha
			return beta

	def bestmove(self):
		flag1 = False
		flag2 = False
		posz = 0
		posi = 0
		posj = 0
		alpha = -10
		beta =  10
		aux = 0
		for z in range(3):
			if flag1:
				break
			for i in range (3):
				if flag2:
					break
				for j in range(3):
					if self.state[z].table.board[i][j] == '.':
						self.state[z].table.board[i][j] = self.tabMachine
						tmp = [self.state[0].table.board, self.state[1].table.board, self.state[2].table.board]
						aux = self.minimax(tmp, False, alpha, beta)
						self.state[z].table.board[i][j] = '.'
						if aux > alpha:
							alpha = aux
							if beta <= alpha:
								flag1 = True
								flag2 = True
								break
							posz = z
							posi = i
							posj = j
		self.movePC(posz,posi,posj)

	def movePC(self,sheet,i,j):
		os.system('cls')
		self.put(sheet,i,j,self.tabMachine)
		print self.__str__()
		
	def isFull(self):
		for i in range(3):
			for j in range(3):
				if self.top.table.board[i][j] == '.' or self.middle.table.board[i][j] == '.' or self.bottom.table.board[i][j] == '.':
					return False
		return True

	def score(self):
		if self.ganador == 1:
			return "\nGANASTE!!"
		else:
			if self.ganador == 2:
				return "\nPERDISTE :( !!"
			else:
				return "\nEMPATE!!"

	def read(self):
		print "Ingrese el tablero y las coordenadas (i,j) para hacer realizar la jugada: "
		sheet = int(input("Ingrese el tablero (1/2/3): "))
		i = int(input("Ingrese i: "))
		j = int(input("Ingrese j: "))
		return [sheet,i,j]


	def play(self):
		print "TABLERO: hey"
		print self.__str__()
		self.firstTurn()
		if self.turn == 1: #Inicia la maquina
			self.moveRandom()
			self.checkMove()
		if self.turn == 0: #Inicia el humano
			self.checkMove()
			if self.level == 0:
				self.moveRandom()
			else: 
				self.bestmove()
		while True:
			tmp = [self.state[0].table.board, self.state[1].table.board, self.state[2].table.board]
			if self.turn == 0: #humano
				if not self.isFull():
					self.checkMove()
					if self.win(tmp ,self.tabHuman): 
						self.ganador = 1
						break
				#else:
				if not self.isFull():
					if self.level == 0: #facil
						self.moveRandom()
					elif self.level == 1:
						pass
						self.bestmove()
					if self.win(tmp, self.tabMachine):
						self.ganador = 2
						break
				elif self.isFull():
					self.ganador = 0
					break

			elif self.turn == 1: #machine
				if not self.isFull():
					if self.level == 0:
						self.moveRandom()
					elif self.level == 1:
						pass
						self.bestmove()
					if self.win(tmp, self.tabMachine):
						self.ganador = 2
						break
				#else:
				if not self.isFull():
					self.checkMove()
					if self.win(tmp, self.tabHuman):
						self.ganador = 1
						break
				elif self.isFull():
					self.ganador = 0
					break
			
		print self.score()

#https://www.ocf.berkeley.edu/~yosenl/extras/alphabeta/alphabeta.html

tri3D = Triqui3D()
print "hola"
tri3D.play()