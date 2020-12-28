import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (234, 255, 0)
GREY = (170, 170, 170)
BLACK = (0, 0, 0)
WIDTH = 700
PIXEL_SIZE = 20
PIXEL_X = WIDTH // PIXEL_SIZE
startPlaced = False
endPlaced = False

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
        # Draw vertical lines:
        pygame.draw.line(window, GREY, (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, WIDTH))
        # Draw horizontal lines
        pygame.draw.line(window, GREY, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE))
        

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

def aStar(graph, board, start):
    pass

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
    global startPlaced
    global endPlaced
    board = pygame.display.set_mode((WIDTH, WIDTH))
    start = False
    graph = createGraph()
    startNode = None
    endNode = None
    run = True
    option = 1
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
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
                
                if event.key == pygame.K_1:
                    print("BFS selected")
                    option = 1
                
                if event.key == pygame.K_2:
                    print("DFS selected")
                    option = 2

        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()
        if mousePress[0] == True:
            # print("Left click")
            placePixel(mousePos[0] // PIXEL_SIZE, mousePos[1] // PIXEL_SIZE, board, graph)
        elif mousePress[2] == True:
            # print("Right click")
            removePixel(mousePos[1] // PIXEL_SIZE, mousePos[0] // PIXEL_SIZE, graph)
        board.fill(WHITE)
        drawPixels(board, graph)
        drawGrid(board)
        pygame.display.update()

    pygame.quit()

main()