import random

class Ambiente:
    grid = [[]]
    init = []
    objective = []

    # inicializa o grid n por n (2 <= n <= 10), sendo '.' um caminho livre e '#' um obstáculo, 
    # após inicializar todos os obstaculos e caminhos livres, gera um ponto aleatório para ser o inicio(A) e outro para ser o objetivo(B)
    # por fim, gera um caminho livre entre o ponto de inicio e o de objetivo
    def __init__(self):
        n = random.randint(2, 10)
        self.__initializeGrid(n)
        self.__selectInit()
        self.__selectObjective()
        self.__makeSolutionPath()
    
    def __initializeGrid(self, n):
        self.grid = [[random.choice(['.', '#']) for _ in range(n)] for _ in range(n)]

    def __selectInit(self):
        n = len(self.grid)
        self.init = [random.randint(0, n-1), random.randint(0, n-1)]
        self.grid[self.init[0]][self.init[1]] = 'A'

    def __selectObjective(self):
        n = len(self.grid)
        while True:
            self.objective = [random.randint(0, n-1), random.randint(0, n-1)]
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
            if (nextMove == 3 and current[1]+1 < len(self.grid)):
                current = [current[0],current[1]+1]
            
            if (current == self.objective): break
            if (current != self.init): self.grid[current[0]][current[1]] = '.'

    def display(self):
        for line in self.grid:
            print(line)

class Agente:
    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.__findInitAndObjective()

    def __findInitAndObjective(self):
        self.ambiente.display()
        for i in range(len(self.ambiente.grid)-1):
            for j in range(len(self.ambiente.grid)-1):
                if (self.ambiente.grid[i][j] == 'A'): self.init = [i,j]
                if (self.ambiente.grid[i][j] == 'B'): self.objective = [i,j]

a = Ambiente()
b = Agente(a)