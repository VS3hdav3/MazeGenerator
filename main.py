import pygame
import math
import random
pygame.init()

win_width = 800
win_height = 800

w = 10

cols = math.floor(win_width/w)
rows = math.floor(win_height/w)

grid = []
current = None
next = None
stack = []
class Cell():
    def __init__(self, i, j):
        self.row = i
        self.col = j
        self.walls = [True, True, True, True] # [Top, Right, Bottom, Left]
        self.visited = False
        self.isCurrent = False
    
    def show(self, win, color = None):
        x = self.col * w
        y = self.row * w
        #pygame.draw.rect(win, (255, 255, 255), (x, y, w, w), 1)
        if color:
            pygame.draw.rect(win, color, (x + 1, y + 1, w, w))
        else:
            if self.visited:
                pygame.draw.rect(win, (50, 205, 50), (x + 1, y + 1, w, w))
            if self.isCurrent:
                pygame.draw.rect(win, (220, 20, 60), (x + 1, y + 1, w, w))
        
        if self.walls[0]:
            pygame.draw.line(win, (255, 255, 255), (x, y), (x + w, y)) #Horizontal Top
        if self.walls[1]:
            pygame.draw.line(win, (255, 255, 255), (x + w, y), (x + w, y + w)) #Vertical Right
        if self.walls[2]:
            pygame.draw.line(win, (255, 255, 255), (x + w, y + w), (x, y + w)) #Horizontal Bottom
        if self.walls[3]:
            pygame.draw.line(win, (255, 255, 255), (x, y + w), (x, y)) #Vertical Left

    def checkNeighbors(self):
        neighbors = []
        top_index = index(self.col, self.row - 1)  
        right_index = index(self.col + 1, self.row)
        bottom_index = index(self.col, self.row + 1)
        left_index = index(self.col - 1, self.row)
        
        if top_index != -1:
            top = grid[top_index]
            if not top.visited:
                neighbors.append(top)
        
        if right_index != -1:
            right = grid[right_index]
            if not right.visited:
                neighbors.append(right)
        
        if bottom_index != -1:
            bottom = grid[bottom_index]
            if not bottom.visited:
                neighbors.append(bottom)
        
        if left_index != -1:
            left = grid[left_index]
            if not left.visited:
                neighbors.append(left)
        
        if len(neighbors) > 0:
            r = random.randint(0, len(neighbors) - 1)
            return neighbors[r]
        else:
            return -1
    
def index(i, j):
    if (i < 0 or j < 0 or i > cols - 1 or j > rows - 1):
        return -1
    else:
        return i + j * cols

def removeWalls():
    global current
    global next
    x = current.col - next.col
    if x == 1:
        current.walls[3] = False
        next.walls[1] = False
    elif x == -1:
        current.walls[1] = False
        next.walls[3] = False
    
    y = current.row - next.row
    if y == 1:
        current.walls[0] = False
        next.walls[2] = False
    elif y == -1:
        current.walls[2] = False
        next.walls[0] = False    

def draw(win):
    global current
    global next
    for cell in grid:
        cell.show(win)
    
    current.visited = True
    #Step 1
    next = current.checkNeighbors()
    if (next != -1):
        next.visited = True
        current.isCurrent = False
        #Step 2
        stack.append(current)
        #Step 3
        removeWalls()
        #Step 4
        current = next
        current.isCurrent = True
    elif (len(stack) > 0) :
        #Step 5
        current.isCurrent = False
        current = stack.pop()
        current.isCurrent = True

def main():
    global current
    win = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Maze Generator")
    win.fill([0, 0, 0])
    clock = pygame.time.Clock()
    
    for i in range(rows):
        for j in range(cols):
            grid.append(Cell(i, j))
    current = grid[0]
    current.isCurrent = True
    
    run = True 
    
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
        win.fill((0, 0, 0))
        draw(win)
        pygame.display.flip()
    pass

if __name__ == "__main__":
    main()