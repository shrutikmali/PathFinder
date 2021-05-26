import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (234, 255, 0)
GREY = (170, 170, 170)
BLACK = (0, 0, 0)
LIGHT_BLUE = (196, 238, 245)
WIDTH = 600
PIXEL_SIZE = 25
PIXEL_X = WIDTH // PIXEL_SIZE # PIXEL_X is the dimension of array
startPlaced = False
endPlaced = False
clock = pygame.time.Clock()

INSTRUCTION1 = "Place start and end nodes on the grid using left mouse button"
INSTRUCTION2 = "A cell can be reset by right mouse button"
INSTRUCTION3A = "Place barriers by holding down left mouse button and dragging"
INSTRUCTION3B = "the mouse"
INSTRUCTION4 = "Press 'Space' to start the visualizer"
INSTRUCTION5 = "Press 'c' to clear the grid"


class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.canVisit = True
        self.visited = False
        self.colour = WHITE
        self.isStart = False
        self.isEnd = False
        self.predecessor = None
        self.neighbourList = []
    
    def createNeighbourList(self, graph):
        # Right
        if self.y + 1 < PIXEL_X:
            self.neighbourList.append(graph[self.x][self.y + 1])
        # Left
        if self.y - 1 >= 0:
            self.neighbourList.append(graph[self.x][self.y - 1])
        # Top
        if self.x - 1 >= 0:
            self.neighbourList.append(graph[self.x  - 1][self.y])
        # Bottom
        if self.x + 1 < PIXEL_X:
            self.neighbourList.append(graph[self.x + 1][self.y])

def createGraph():
    graph = []
    for i in range(PIXEL_X):
        graph.append([])
        for j in range(PIXEL_X):
            graph[i].append(None)
    
    for i in range(PIXEL_X):
        for j in range(PIXEL_X):
            newNode = Node(i, j)
            graph[i][j] = newNode

    for i in range(PIXEL_X):
        for j in range(PIXEL_X):
            graph[i][j].createNeighbourList(graph)

    return graph

def drawGrid(window):
    for i in range(WIDTH // PIXEL_SIZE):
        # Draw horizontal lines
        pygame.draw.line(window, GREY, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE))
    
    for i in range((WIDTH // PIXEL_SIZE)+1):
        # Draw vertical lines:
        pygame.draw.line(window, GREY, (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, WIDTH))
        

def drawPixels(window, graph):
    for i in range(PIXEL_X):
        for j in range(PIXEL_X):
            pygame.draw.rect(window, graph[i][j].colour, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

def removePixel(x, y, graph):
    global startPlaced
    global endPlaced
    graph[x][y].canVisit = True
    graph[x][y].visited = False
    graph[x][y].colour = WHITE

    if graph[x][y].isStart:
        graph[x][y].isStart = False
        startPlaced = False
    if graph[x][y].isEnd:
        graph[x][y].isEnd = False
        endPlaced = False

def placePixel(x, y, board, graph):
    global startPlaced
    global endPlaced
    if not startPlaced and not graph[y][x].isEnd:
        pygame.draw.rect(board, BLUE, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
        graph[y][x].isStart = True
        graph[y][x].colour = BLUE
        startPlaced = True
    elif not endPlaced and not graph[y][x].isStart:
        pygame.draw.rect(board, GREEN, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
        graph[y][x].isEnd = True
        graph[y][x].colour = GREEN
        endPlaced = True
    elif graph[y][x].colour == WHITE:
        pygame.draw.rect(board, BLACK, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
        graph[y][x].canVisit = False
        graph[y][x].colour = BLACK
    pygame.display.update()

def BFS(graph, board, start):
    startNode = None
    for i in range(PIXEL_X):
        for j in range(PIXEL_X):
            if graph[i][j].isStart:
                startNode = graph[i][j]
                break
        if startNode != None:
            break
    # print(startNode)
    queue = []
    startNode.visited = True
    queue.append(startNode)
    while len(queue) != 0:
        front = queue.pop(0)
        if front.isEnd == True:
            drawPath(front, graph, board, start)
            break
        if front.isStart == False:
            front.colour = RED
        drawPixels(board, graph)
        drawGrid(board)
        pygame.display.update()
        
        for neighbour in front.neighbourList:
            if neighbour.visited == False and neighbour.canVisit == True:
                neighbour.visited = True
                if neighbour.isEnd == False:
                    neighbour.colour = RED
                neighbour.predecessor = front
                queue.append(neighbour)
                
def DFS(graph, board, start):
    startNode = None
    for i in range(PIXEL_X):
        for j in range(PIXEL_X):
            if graph[i][j].isStart:
                startNode = graph[i][j]
                break
        if startNode != None:
            break
    # print(startNode)
    stack = []
    startNode.visited = True
    stack.append(startNode)
    while len(stack) != 0:
        front = stack.pop()
        if front.isEnd == True:
            drawPath(front, graph, board, start)
            break
        if front.isStart == False:
            front.colour = RED
        drawPixels(board, graph)
        drawGrid(board)
        pygame.display.update()
        
        for neighbour in front.neighbourList:
            if neighbour.visited == False and neighbour.canVisit == True:
                neighbour.visited = True
                if neighbour.isEnd == False:
                    neighbour.colour = RED
                neighbour.predecessor = front
                stack.append(neighbour)


def drawPath(end, graph, board, start):
    currNode = end.predecessor
    while(currNode.predecessor != None and currNode.isStart == False):
        graph[currNode.x][currNode.y].colour = YELLOW
        currNode = currNode.predecessor
        drawPixels(board, graph)
        drawGrid(board)
        pygame.display.update()
    start = False

def main():
    pygame.time.wait(150)
    pygame.font.init()
    fontObj = pygame.font.SysFont('Arial', 22)
    global startPlaced
    global endPlaced
    board = pygame.display.set_mode((WIDTH + 150, WIDTH))
    start = False
    graph = createGraph()
    startNode = None
    endNode = None
    run = True
    option = 1
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if start:
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not start:
                    if startPlaced and endPlaced:
                        if option == 1:
                            BFS(graph, board, start)
                        elif option == 2:
                            DFS(graph, board,start)
                if event.key == pygame.K_c:
                    for i in range(PIXEL_X):
                        for j in range(PIXEL_X):
                            removePixel(i, j, graph)
                    startPlaced = False
                    endPlaced = False
                
                # if event.key == pygame.K_1:
                #     option = 1
                    
                # if event.key == pygame.K_2:
                #     pygame.time.wait(100)
                #     option = 2

        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()
        if mousePress[0] == True:
            # print("Left click")
            if(mousePos[0] < 600):
                placePixel(mousePos[0] // PIXEL_SIZE, mousePos[1] // PIXEL_SIZE, board, graph)
            elif mousePos[0] >= 625 and mousePos[0] <= 725 and mousePos[1] >= 60 and mousePos[1] <= 110:
                option = 1
                # print("BFS selected")
            elif mousePos[0] >= 625 and mousePos[0] <= 725 and mousePos[1] >= 120 and mousePos[1] <= 170:
                option = 2
                # print("DFS selected")
            elif mousePos[0] >= 600 and mousePos[0] <= 750 and mousePos[1] >= 500 and mousePos[1] <= 600:
                startScreen()
            
        elif mousePress[2] == True:
            # print("Right click")
            if(mousePos[0] < 600):
                removePixel(mousePos[1] // PIXEL_SIZE, mousePos[0] // PIXEL_SIZE, graph)
        board.fill(WHITE)
        pygame.draw.rect(board, LIGHT_BLUE, ((625, 60, 100, 50)))
        pygame.draw.rect(board, LIGHT_BLUE, ((625, 120, 100, 50)))
        if option == 1:
            pygame.draw.rect(board, GREEN, (635, 82, 10, 10))
        elif option == 2:
            pygame.draw.rect(board, GREEN, (635, 140, 10, 10))
        option_bfs = fontObj.render('BFS', True, (0,0,0))
        board.blit(option_bfs, (655, 74))
        option_dfs = fontObj.render('DFS', True, (0,0,0))
        board.blit(option_dfs, (655, 132))
        pygame.draw.rect(board, LIGHT_BLUE, (600, 500, 650, 600))
        home = fontObj.render('Home', True, (0, 0, 0))
        board.blit(home, (650, 540))
        drawPixels(board, graph)
        drawGrid(board)
        pygame.display.update()
        # clock.tick(60)

    pygame.quit()

def startScreen():
    pygame.font.init()
    fontObj = pygame.font.SysFont('Arial', 22)
    screen = pygame.display.set_mode((WIDTH, WIDTH))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()
        if mousePress[0] == True:
            if(mousePos[0] >= 150 and mousePos[0] <= 450 and mousePos[1] >= 100 and mousePos[1] <= 200):
                main()
            if(mousePos[0] >= 150 and mousePos[0] <= 450 and mousePos[1] >= 250 and mousePos[1] <= 350):
                instructionScreen()

        screen.fill(WHITE)
        title = fontObj.render('Path Finding Visualizer', True, (0,0,0))
        pygame.draw.rect(screen, LIGHT_BLUE, (150, 100, 300, 100))
        pygame.draw.rect(screen, LIGHT_BLUE, (150, 250, 300, 100))
        instructions = fontObj.render('Instructions', True, (0,0,0))
        start = fontObj.render('Start', True, (0,0,0))
        screen.blit(title, (210, 50))
        screen.blit(start, (280, 135))
        screen.blit(instructions, (257, 285))
        pygame.display.update()

def instructionScreen():
    pygame.font.init()
    fontObj = pygame.font.SysFont('Arial', 22)
    screen = pygame.display.set_mode((WIDTH, WIDTH))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        
        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()

        if mousePress[0] == True:
            if mousePos[0] >= 0 and mousePos[0] <= 600 and mousePos[1] >= 500 and mousePos[1] <= 600:
                startScreen()


        screen.fill(WHITE)
        title = fontObj.render('Instructions', True, (0,0,0))
        returnToHome = fontObj.render('Back to Home', True, (0, 0, 0))
        i1 = fontObj.render(INSTRUCTION1, True, (0, 0, 0))
        i2 = fontObj.render(INSTRUCTION2, True, (0, 0, 0))
        i3a = fontObj.render(INSTRUCTION3A, True, (0, 0, 0))
        i3b = fontObj.render(INSTRUCTION3B, True, (0, 0, 0))
        i4 = fontObj.render(INSTRUCTION4, True, (0, 0, 0))
        i5 = fontObj.render(INSTRUCTION5, True, (0, 0, 0))
        pygame.draw.rect(screen, LIGHT_BLUE, (0, 500, 600, 600))
        screen.blit(title, (250, 30))
        screen.blit(i1, (20, 100))
        screen.blit(i2, (20, 150))
        screen.blit(i3a, (20, 200))
        screen.blit(i3b, (20, 225))
        screen.blit(i4, (20, 270))
        screen.blit(i5, (20, 320))
        screen.blit(returnToHome, (245, 540))
        pygame.display.update()
    
startScreen()