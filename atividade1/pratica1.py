import random

class Ambiente:
    grid = [[]]
    init = []
    objective = []

    # inicializa o grid n por m (4 <= n,m <= 15), sendo '.' um caminho livre e '#' um obstáculo, 
    # após inicializar todos os obstaculos e caminhos livres, gera um ponto aleatório para ser o inicio(A) e outro para ser o objetivo(B)
    # por fim, gera um caminho livre entre o ponto de inicio e o de objetivo
    def __init__(self):
        n = random.randint(4, 15)
        m = random.randint(4, 15)
        self.__initializeGrid(n, m)
        self.__selectInit()
        self.__selectObjective()
        self.__makeSolutionPath()
    
    def __initializeGrid(self, n, m):
        self.grid = [[random.choice(['.', '#']) for _ in range(m)] for _ in range(n)]

    def __selectInit(self):
        n = len(self.grid)
        m = len(self.grid[0])
        self.init = [random.randint(0, n-1), random.randint(0, m-1)]
        self.grid[self.init[0]][self.init[1]] = 'A'

    def __selectObjective(self):
        n = len(self.grid)
        m = len(self.grid[0])
        while True:
            self.objective = [random.randint(0, n-1), random.randint(0, m-1)]
            if (self.objective != self.init): break
        self.grid[self.objective[0]][self.objective[1]] = 'B'

    def __makeSolutionPath(self):
        current = self.init
        while True:
            # 0 -> cima
            # 1 -> baixo
            # 2 -> esquerda
            # 3 -> direita
            nextMove = random.randint(0,3)
            if (nextMove == 0 and current[0]-1 >= 0): 
                current = [current[0]-1,current[1]]
            if (nextMove == 1 and current[0]+1 < len(self.grid)): 
                current = [current[0]+1,current[1]]
            if (nextMove == 2 and current[1]-1 >= 0): 
                current = [current[0],current[1]-1]
            if (nextMove == 3 and current[1]+1 < len(self.grid[0])):
                current = [current[0],current[1]+1]
            
            if (current == self.objective): break
            if (current != self.init): self.grid[current[0]][current[1]] = '.'

    def do(self, func):
        self.grid = func(self.grid)
        return self.grid

class AgenteBFS:
    def __init__(self, perception, walk_symbol):
        self.l_limit, self.r_limit, self.u_limit, self.d_limit = [0, len(perception[0])-1, 0, len(perception)-1]
        self.walk_symbol = walk_symbol
        self.objective_found = False
        self.__findInitAndObjective(perception)

    def __findInitAndObjective(self, perception):
        for i in range(len(perception)):
            for j in range(len(perception[0])):
                if (perception[i][j] == 'A'): self.currents = [(i,j)]
                if (perception[i][j] == 'B'): self.objective = (i,j)
                if (hasattr(self, 'currents') and hasattr(self, 'objective')): return
    
    def __move(self, current, perception):
        if (self.__valid_move('L', current, perception)):
            next_coord = (current[0], current[1]-1)
            perception[next_coord[0]][next_coord[1]] = self.walk_symbol
            self.currents.append(next_coord)

        if (self.__valid_move('R', current, perception)):
            next_coord = (current[0], current[1]+1)
            perception[next_coord[0]][next_coord[1]] = self.walk_symbol
            self.currents.append(next_coord)

        if (self.__valid_move('U', current, perception)):
            next_coord = (current[0]-1, current[1])
            perception[next_coord[0]][next_coord[1]] = self.walk_symbol
            self.currents.append(next_coord)

        if (self.__valid_move('D', current, perception)):
            next_coord = (current[0]+1, current[1])
            perception[next_coord[0]][next_coord[1]] = self.walk_symbol
            self.currents.append(next_coord)

        return perception

    def __valid_move(self, direction, coord, perception):
        res = False

        if direction == 'L':
            next_x = coord[1] - 1
            if (next_x >= self.l_limit):
                if (perception[coord[0]][next_x] == "."):
                    res = True
                elif (perception[coord[0]][next_x] == "B"):
                    self.objective_found = True

        elif direction == 'R':
            next_x = coord[1] + 1
            if (next_x <= self.r_limit):
                if (perception[coord[0]][next_x] == "."):
                    res = True
                elif (perception[coord[0]][next_x] == "B"):
                    self.objective_found = True

        elif direction == 'U':
            next_y = coord[0] - 1
            if (next_y >= self.u_limit):
                if (perception[next_y][coord[1]] == "."):
                    res = True
                elif (perception[next_y][coord[1]] == "B"):
                    self.objective_found = True

        elif direction == 'D':
            next_y = coord[0] + 1
            if (next_y <= self.d_limit):
                if (perception[next_y][coord[1]] == "."):
                    res = True
                elif (perception[next_y][coord[1]] == "B"):
                    self.objective_found = True

        return res

    def select_action(self, perception):
        action = [row[:] for row in perception]

        if (not self.objective_found):
            chields = self.currents[:]

            for current in chields:
                self.currents.pop(0)
                action = self.__move(current, action)

        return action
        
a = Ambiente()
b = AgenteBFS(a.do(lambda a : a), '^')

while (not b.objective_found):
    print(*a.do(b.select_action), sep="\n")
    print("\n=======\n")