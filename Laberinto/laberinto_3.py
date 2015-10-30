from random import shuffle, randrange
 
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
    for i in range(len(lab)):
        maze[contx] = {}
        for j in range(len(lab[i])):
            if lab[i][j] == 's':
                contx += 1
                maze[contx] = {}
                conty = 0
                continue
            maze[contx][conty] = lab[i][j]
            conty +=1
        contx += 1
        conty = 0

    s = ""
    #maze[1][0] = 'I'
    #maze[15][48] = 'F'
    for i in maze:
        for j in maze[i]:
            s += maze[i][j]
        print s
        s = ""
    
    return maze

matrix_maze()
