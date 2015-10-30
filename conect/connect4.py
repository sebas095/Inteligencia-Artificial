#Codigo base extraido de: https://github.com/erikackermann/Connect-Four

import random
from minimax import Minimax

class Game(object):
    """ Game object that holds state of Connect 4 board and game values
    """
    
    board = None
    round = None
    finished = None
    winner = None
    turn = None
    players = [None, None] 
    colors = ["x", "o"]

    
    def __init__(self):
        self.board = []
        self.round = 1
        self.finished = False
        self.winner = None
        self.players[0] = Player(self.colors[0])
        self.players[1] = AIPlayer(self.colors[1], 5) 
        self.turn = self.players[0]
        for i in xrange(6):
            self.board.append([])
            for j in xrange(7):
                self.board[i].append(' ')
    
    def newGame(self):
        """ Function to reset the game, but not the names or colors
        """
        self.round = 1
        self.finished = False
        self.winner = None
        
        # x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]
		
        self.board = []
        for i in xrange(6):
            self.board.append([])
            for j in xrange(7):
                self.board[i].append(' ')

    def switchTurn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
		    self.turn = self.players[0]

        # increment the round
        self.round += 1

    def nextMove(self):
        player = self.turn

        # there are only 42 legal places for pieces on the board
        # exactly one piece is added to the board each turn
        if self.round > 42:
            self.finished = True
            # this would be a stalemate :(
            return
        
        # move is the column that player want's to play
        move = player.move(self.board)

        for i in xrange(6):
            if self.board[i][move] == ' ':
                self.board[i][move] = player.color
                self.switchTurn()
                self.checkForFours()
                self.printState()
                return

        # if we get here, then the column is full
        print("Invalid move (column is full)")
        return
	
    def checkForFours(self):
        # for each piece in the board...
        for i in xrange(6):
            for j in xrange(7):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.verticalCheck(i, j):
                        self.finished = True
                        return
                    
                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontalCheck(i, j):
                        self.finished = True
                        return
                    
                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        print(slope)
                        self.finished = True
                        return
	    
    def verticalCheck(self, row, col):
        #print("checking vert")
        fourInARow = False
        consecutiveCount = 0
    
        for i in xrange(row, 6):
            if self.board[i][col] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color == self.board[row][col]:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
    
        return fourInARow
    
    def horizontalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0
        
        for j in xrange(col, 7):
            if self.board[row][j] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color == self.board[row][col]:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fourInARow
    
    def diagonalCheck(self, row, col):
        fourInARow = False
        count = 0
        slope = None

        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in xrange(row, 6):
            if j > 6:
                break
            elif self.board[i][j] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
			
        if consecutiveCount >= 4:
            count += 1
            slope = 'positive'
            if self.players[0].color == self.board[row][col]:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in xrange(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is decremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'negative'
            if self.players[0].color == self.board[row][col]:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            fourInARow = True
        if count == 2:
            slope = 'both'
        return fourInARow, slope
	
    def printState(self):
        print("Round: " + str(self.round))

        for i in xrange(5, -1, -1):
            print("\t"),
            for j in xrange(7):
                print("| " + str(self.board[i][j])),
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.finished:
            print("Game Over!")
            if self.winner != None:
                print(str(self.winner.type) + " is the winner")
            else:
                print("Game was a draw")

    
                
class Player(object):
    """ Player object.  This class is for human players.
    """
    
    type = None # possible types are "Human" and "AI"
    color = None
    def __init__(self, color):
        self.type = "Human"
        self.color = color
    
    def move(self, state):
        print("Human turn")
        column = None
        while column == None:
            try:
                choice = int(raw_input("Enter a move (by column number): ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Invalid choice, try again")
        return column


class AIPlayer(Player):
    """ AIPlayer object that extends Player
        The AI algorithm is minimax, the difficulty parameter is the depth to which 
        the search tree is expanded.
    """
    
    difficulty = None
    def __init__(self, color, difficulty=5):
        self.type = "AI"
        self.color = color
        self.difficulty = difficulty
        
    def move(self, state):
        print("Computer turn")
    
        m = Minimax(state)
        best_move, value = m.bestMove(self.difficulty, state, self.color)
        return best_move




