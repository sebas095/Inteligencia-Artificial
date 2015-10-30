import os
import random
from board import *

class Triqui (object):

	def __init__(self):
		self.table = Board() 
		self.player = 1  #Human:1 Machine:0
		self.ganador = -1 #Human:1 Machine:2 Empate:0
		self.tabHuman = 'O'
		self.tabMachine = 'X'
		self.level = 0 # Level: 0 Facil, Level: 1 Dificil
		self.turn = 0 # Turno: 0 juega primero el humano, Turno: 1 juega primero la maquina

	def __str__(self):
		return self.table.__str__()

	def win(self, symbol):
		#diagonales
		if self.table.board[0][0] == symbol and self.table.board[1][1] == symbol and self.table.board[2][2] == symbol:
			return True
		elif self.table.board[2][0] == symbol and self.table.board[1][1] == symbol and self.table.board[0][2] == symbol:
			return True
		#filas
		elif self.table.board[0][0] == symbol and self.table.board[0][1] == symbol and self.table.board[0][2] == symbol:
			return True
		elif self.table.board[1][0] == symbol and self.table.board[1][1] == symbol and self.table.board[1][2] == symbol:
			return True
		elif self.table.board[2][0] == symbol and self.table.board[2][1] == symbol and self.table.board[2][2] == symbol:
			return True
		#columnas
		elif self.table.board[0][0] == symbol and self.table.board[1][0] == symbol and self.table.board[2][0] == symbol:
			return True
		elif self.table.board[0][1] == symbol and self.table.board[1][1] == symbol and self.table.board[2][1] == symbol:
			return True
		elif self.table.board[0][2] == symbol and self.table.board[1][2] == symbol and self.table.board[2][2] == symbol:
			return True
		else: return False

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

	def checkMove(self):
		pos = self.read()
		i = pos[0]
		j = pos[1]
		if self.table.isAllow(i,j):
			if self.moveHuman(i,j):
				return
		else:
			print "La posicion ",i," ",j," no se encuentra disponible, intente de nuevo:\n"
			pos = self.read()
			i = pos[0]
			j = pos[1]
			while not self.table.isAllow(i,j):
				print "La posicion ",i," ",j," no se encuentra disponible, intente de nuevo:\n"
				pos = self.read()
				i = pos[0]
				j = pos[1]
			self.moveHuman(i,j)

	def moveRandom(self):
		i = random.randint(0,2)
		j = random.randint(0,2)
		while not self.table.isAllow(i,j):
			i = random.randint(0,2)
			j = random.randint(0,2)
		self.movePC(i,j)

	def moveHuman(self,i,j):
		os.system('cls')
		self.table.put(i,j,self.tabHuman)
		print self.getBoard()

	def movePC(self,i,j):
		os.system('cls')
		self.table.put(i,j,self.tabMachine)
		print self.getBoard()


	def minimo(self):
		if self.win(self.tabMachine):
			return 1
		if not self.win(self.tabMachine) and not self.win(self.tabHuman) and self.table.isFull():
			return 0
		aux = 9999
		mejor = 9999
		for i in range (3): 
			for j in range(3):
				if self.table.board[i][j] == '.':
					self.table.board[i][j] = self.tabHuman #HUMANO
					aux = self.maximo()
					if aux < mejor:
						mejor = aux
					self.table.board[i][j] = '.'
		return mejor

	def maximo(self):
		if self.win(self.tabHuman):
			return -1
		if not self.win(self.tabMachine) and not self.win(self.tabHuman) and self.table.isFull():
			return 0

		aux = -9999
		mejor = -9999
		for i in range (3):
			for j in range(3):
				if self.table.board[i][j] == '.':
					self.table.board[i][j] = self.tabMachine 
					aux = self.minimo()
					if aux > mejor:
						mejor=aux
					self.table.board[i][j] = '.'
		return mejor

	def bestmove(self):
		posi = 0
		posj = 0
		aux = -9999
		mejor = -9999
		for i in range (3):
			for j in range(3):
				if self.table.board[i][j] == '.':
					self.table.board[i][j] = self.tabMachine
					aux = self.minimo()
					if aux > mejor:
						mejor = aux
						posi = i
						posj = j
					self.table.board[i][j] = '.'
		self.movePC(posi,posj)
	
	def getBoard(self):
		return self.table

	def score(self):
		if self.ganador == 1:
			return "GANASTE!!"
		else:
			if self.ganador == 2:
				return "PERDISTE :( !!"
			else:
				return "EMPATE!!"

	def read(self):
		print "Ingrese coordenadas (i,j) para hacer realizar la jugada: "
		i = int(input("Ingrese i: "))
		j = int(input("Ingrese j: "))
		return [i,j]

	def play(self):
		print "TABLERO:"
		print self.getBoard()
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
			if self.turn == 0: #humano
				if not self.table.isFull():
					self.checkMove()
					if self.win(self.tabHuman): 
						self.ganador = 1
						break
				#else:
				if not self.table.isFull():
					if self.level == 0: #facil
						self.moveRandom()
					elif self.level == 1:
						self.bestmove()
					if self.win(self.tabMachine):
						self.ganador = 2
						break
				elif self.table.isFull():
					self.ganador = 0
					break

			elif self.turn == 1: #machine
				if not self.table.isFull():
					if self.level == 0:
						self.moveRandom()
					elif self.level == 1:
						self.bestmove()
					if self.win(self.tabMachine):
						self.ganador = 2
						break
				#else:
				if not self.table.isFull():
					self.checkMove()
					if self.win(self.tabHuman):
						self.ganador = 1
						break
				elif self.table.isFull():
					self.ganador = 0
					break
			
		print self.score()


#PRUEBAS!
#tri = Triqui()
#print "TABLERO:"
#print tri.getBoard()
'''while tri.ganador == -1:
	if tri.win(tri.tabHuman):
		tri.ganador = 1
		break
	elif tri.win(tri.tabMachine):
		tri.ganador = 2
		break
	tri.checkMove()
	tri.moveRandom()
print tri.score()
tri.play()'''
#tri.play()


