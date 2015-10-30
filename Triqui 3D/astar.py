import heapq

def Astar(graph, root, goal):
    frontier = [( 0,0, root, [])]
    explored = set()
    pair=()
    while True:
        (cost_heuris,cost_acum, v, path) = heapq.heappop(frontier)

        if v not in explored:
            path = path + [v]
            explored.add(v)
            if v == goal:
                return cost_acum, path

            for (next, pair) in graph[v].iteritems():
                c,h=pair
                heapq.heappush(frontier, (cost_heuris + c + h,cost_acum+c, next, path))
    
def main():
	graph= {'s':{'a':(2,3), 'b':(1,3)},       #'parent': 'adj_node':(cost,heuristic)
                'a':{'b':(1,3),'c':(3,1), 'd':(1,2)},
                'b':{'d':(5,2), 'goal':(10,0)},
                'c':{'goal':(7,0)},
                'd':{'goal':(4,0)} }

	print "(Cost, path) --> ",Astar(graph,'s','goal')

if __name__ == '__main__':
	main()
