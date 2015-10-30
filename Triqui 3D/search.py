# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state
        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state
        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take
        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    fringe = util.Stack();
    visited = [];
    fringe.push((problem.getStartState(),[],0));

    while not fringe.isEmpty():
        node, actions, cost = fringe.pop();

        if(node in visited):
            continue;

        visited.append(node);

        if problem.isGoalState(node):
            return actions;

        for state, direction, cost in problem.getSuccessors(node):
            fringe.push((state, actions+[direction], cost));

    return [];


def breadthFirstSearch(problem):
    level_bfs={}
    parent_bfs={}
    level_bfs[problem.getStartState()]=0
    parent_bfs[problem.getStartState()]=None
    i=1
    fringe=[]
    fringe.append( (problem.getStartState(), []) )

    while fringe:
        next_adj=[]
        for node,actions in fringe:
            for coord, direction, cost in problem.getSuccessors(node):



                if not coord in level_bfs :
                    level_bfs[coord]=i
                    parent_bfs[coord]=node


                    next_adj.append( (coord,actions+[direction]) )


                    if problem.isGoalState(coord):
                        #----------------------------------------------------
                        # ciclo para mostrar  todos los nodos que visito el bfs con sus respectivos padres
                        #Formato para imprimir todo el arbol de busqueda (GraphViz)
                        #for parent,children in parent_bfs.iteritems():
                        #    print "\"",children,"\"","->","\"",parent,"\"" 
                        #----------------------------------------------------
                        return actions + [direction]
                    
            fringe=next_adj
            i+=1

    return []

'''
def breadthFirstSearch(problem):
    fringe = util.Queue()
    fringe.push( (problem.getStartState(), []) )

    visited = []
    while not fringe.isEmpty():
        node, actions = fringe.pop()

        for coord, direction, steps in problem.getSuccessors(node):
            #print actions
            if not coord in visited:
                if problem.isGoalState(coord):
                    return actions + [direction]
                fringe.push((coord, actions + [direction]))
                visited.append(coord)

    return []
'''

def uniformCostSearch(problem):
    fringe = util.PriorityQueue()
    fringe.push( (problem.getStartState(), []), 0)
    visited = []

    while not fringe.isEmpty():
        node, actions = fringe.pop()

        visited.append(node)
        if problem.isGoalState(node):
            return actions

        visited.append(node)

        for coord, direction, steps in problem.getSuccessors(node):
            if not coord in visited:
                new_actions = actions + [direction]
                fringe.push((coord, new_actions), problem.getCostOfActions(new_actions))

    return []
    
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    visited = []
    fringe = util.PriorityQueue()
    start = problem.getStartState()
    fringe.push( (start, []), heuristic(start, problem) )

    while not fringe.isEmpty():
        node, actions = fringe.pop()

        if problem.isGoalState(node):
            return actions

        visited.append(node)

        for coord, direction, cost in problem.getSuccessors(node):
            if not coord in visited:
                new_actions = actions + [direction]
                cost_acum = problem.getCostOfActions(new_actions) + heuristic(coord, problem)
                fringe.push( (coord, new_actions), cost_acum)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch