import random
import copy
from connect4 import *

class Minimax(object):
    """ Minimax object that takes a current connect four board state
    """
    
    board = None
    finished = None
    winner = None
    colors = ["x", "o"]
    
    def __init__(self, board):
        # copy the board to self.board
        self.board = copy.deepcopy(board)
        self.finished = False
        self.winner = None


    def minimax(self, state, machine, alpha, beta):
        if(self.winner == self.colors[1]):
            return 1

        if(self.winner == self.colors[0]):
            return -1

        if (self.winner == None and self.finished == True):
            return 0
        if machine:
            for each in self.succesors(self.colors[1]):
                machine = False
                aux = self.minimax(state, machine, alpha, beta)
                if aux > alpha:
                    alpha = aux
                if beta <= alpha:
                    return beta
            return alpha
        else:
            for each in self.succesors(self.colors[0]):
                machine = True 
                aux = self.minimax(state, machine, alpha, beta)
                if aux < beta:
                    beta = aux
                if alpha >= beta:
                    return alpha
            return beta	
			

    def succesors(self, element):
        succesors = []
        for i in xrange(6):
            for col in xrange(7):
                if self.isLegalMove(col,self.board):
                    print self.board[i][col]
                    self.board[i][col] = element
                    tmp = []
                    tmp = copy.deepcopy(self.board)
                    self.board[i][col] = ' '
                    succesors.append(tmp)
        return succesors


    def isLegalMove(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """
        
        for i in xrange(6):
            if state[i][column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True
        
        # if we get here, the column is full
        return False

    def bestMove(self, state):
        flag = False
        colum = 0
        alpha = -10
        beta = 10
        aux = 0
        for col in xrange (7):
            if self.isLegalMove:
                self.board[col] = self.colors[1]
                aux = self.minimax(self.board, False,  alpha, beta)
                self.board[col] = ' '
                if aux > alpha:
                    alpha = aux
                    if beta <= alpha:
                        colum = col
                        flag = True
                        break
                    colum = col
        return colum