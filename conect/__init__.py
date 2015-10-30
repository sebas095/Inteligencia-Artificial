#Codigo base extraido de: https://github.com/erikackermann/Connect-Four

from connect4 import *

if __name__ == '__main__':
    
    g = Game()
    g.printState()
    exit = False
    while not exit:
        while not g.finished:
            g.nextMove()
        g.printState()
        break
