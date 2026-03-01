import pygame
import random
import math
import time
from queue import PriorityQueue

pygame.init()

WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Pathfinding Agent")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
GREY = (200,200,200)

ROWS = 30
COLS = 30
CELL = WIDTH // COLS

class Node:
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.x = col * CELL
        self.y = row * CELL
        self.color = WHITE
        self.neighbors = []
        self.parent = None
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")

    def draw(self):
        pygame.draw.rect(WIN,self.color,(self.x,self.y,CELL,CELL))
        pygame.draw.rect(WIN,GREY,(self.x,self.y,CELL,CELL),1)

    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < ROWS-1 and grid[self.row+1][self.col].color != BLACK:
            self.neighbors.append(grid[self.row+1][self.col])
        if self.row > 0 and grid[self.row-1][self.col].color != BLACK:
            self.neighbors.append(grid[self.row-1][self.col])
        if self.col < COLS-1 and grid[self.row][self.col+1].color != BLACK:
            self.neighbors.append(grid[self.row][self.col+1])
        if self.col > 0 and grid[self.row][self.col-1].color != BLACK:
            self.neighbors.append(grid[self.row][self.col-1])

def make_grid():
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(COLS):
            grid[i].append(Node(i,j))
    return grid

def draw_grid(grid):
    WIN.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw()
    pygame.display.update()

def heuristic(a,b,type):
    if type == "manhattan":
        return abs(a.row - b.row) + abs(a.col - b.col)
    else:
        return math.sqrt((a.row-b.row)**2 + (a.col-b.col)**2)

def reconstruct_path(current,draw):
    cost = 0
    while current.parent:
        current = current.parent
        if current.parent:
            current.color = GREEN
        cost += 1
        draw()
    return cost

def a_star(draw,grid,start,end,h_type):
    count = 0
    open_set = PriorityQueue()
    start.g = 0
    start.f = heuristic(start,end,h_type)
    open_set.put((start.f,count,start))

    visited_nodes = 0
    start_time = time.time()

    while not open_set.empty():
        current = open_set.get()[2]

        if current == end:
            total_cost = reconstruct_path(end,draw)
            end_time = time.time()
            return True, visited_nodes, total_cost, (end_time-start_time)*1000

        for row in grid:
            for node in row:
                node.update_neighbors(grid)

        for neighbor in current.neighbors:
            temp_g = current.g + 1
            if temp_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = temp_g
                neighbor.h = heuristic(neighbor,end,h_type)
                neighbor.f = neighbor.g + neighbor.h
                count += 1
                open_set.put((neighbor.f,count,neighbor))
                if neighbor != end:
                    neighbor.color = YELLOW

        if current != start:
            current.color = BLUE
            visited_nodes += 1

        draw()

    return False, visited_nodes, 0, 0

def greedy(draw,grid,start,end,h_type):
    count = 0
    open_set = PriorityQueue()
    open_set.put((heuristic(start,end,h_type),count,start))
    visited = set()
    visited_nodes = 0
    start_time = time.time()

    while not open_set.empty():
        current = open_set.get()[2]

        if current == end:
            total_cost = reconstruct_path(end,draw)
            end_time = time.time()
            return True, visited_nodes, total_cost, (end_time-start_time)*1000

        visited.add(current)

        for row in grid:
            for node in row:
                node.update_neighbors(grid)

        for neighbor in current.neighbors:
            if neighbor not in visited:
                neighbor.parent = current
                count += 1
                open_set.put((heuristic(neighbor,end,h_type),count,neighbor))
                neighbor.color = YELLOW

        if current != start:
            current.color = BLUE
            visited_nodes += 1

        draw()

    return False, visited_nodes, 0, 0

def random_obstacles(grid,density):
    for row in grid:
        for node in row:
            if random.random() < density:
                node.color = BLACK

def main():
    grid = make_grid()
    start = grid[0][0]
    end = grid[ROWS-1][COLS-1]
    start.color = RED
    end.color = GREEN

    run = True
    algorithm = "astar"
    heuristic_type = "manhattan"

    while run:
        draw_grid(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row = pos[1] // CELL
                col = pos[0] // CELL
                if grid[row][col] != start and grid[row][col] != end:
                    grid[row][col].color = BLACK

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid = make_grid()
                    start = grid[0][0]
                    end = grid[ROWS-1][COLS-1]
                    start.color = RED
                    end.color = GREEN

                if event.key == pygame.K_SPACE:
                    if algorithm == "astar":
                        result = a_star(lambda: draw_grid(grid),grid,start,end,heuristic_type)
                    else:
                        result = greedy(lambda: draw_grid(grid),grid,start,end,heuristic_type)

                    print("Visited:",result[1])
                    print("Cost:",result[2])
                    print("Time(ms):",result[3])

                if event.key == pygame.K_1:
                    algorithm = "astar"

                if event.key == pygame.K_2:
                    algorithm = "greedy"

                if event.key == pygame.K_m:
                    heuristic_type = "manhattan"

                if event.key == pygame.K_e:
                    heuristic_type = "euclidean"

                if event.key == pygame.K_o:
                    random_obstacles(grid,0.3)

    pygame.quit()

main()
#minor changes
