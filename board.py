from constants import *
import pygame
import random

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


class Square:
    def __init__(self, x, y):
        self.width = COL_W - PAD
        self.height = ROW_H - PAD
        self.x = x
        self.y = y
        self.color = REG

    def swap_color(self):
        if self.color == REG:
            self.color = WALL
        else:
            self.color = REG

    def draw(self):
        pygame.draw.rect(WIN, self.color,
                         (self.x * COL_W, self.y * ROW_H,
                          self.width, self.height))


class Board:
    def __init__(self):
        self.two_d = [[Square(col % COLS, row % ROWS) for col in range(COLS)]
                      for row in range(ROWS)]
        self.square_list = [square for row in self.two_d for square in row]

    def draw(self):
        for square in self.square_list:
            square.draw()

    def create_adj(self):
        adj_list = {square: set() for square in self.square_list}
        for square in adj_list:
            for assoc in self.square_list:
                if square.y == assoc.y:
                    if abs(square.x - assoc.x) == 1 and assoc.color != WALL:
                        adj_list[square].add(assoc)
                if square.x == assoc.x:
                    if abs(square.y - assoc.y) == 1 and assoc.color != WALL:
                        adj_list[square].add(assoc)
        return adj_list

    def create_adj_2(self, color):
        adj_list = {square: set() for square in self.square_list}
        for square in adj_list:
            for assoc in self.square_list:
                if square.y == assoc.y:
                    if abs(square.x - assoc.x) == 2 and assoc.color != color:
                        adj_list[square].add(assoc)
                if square.x == assoc.x:
                    if abs(square.y - assoc.y) == 2 and assoc.color != color:
                        adj_list[square].add(assoc)
        return adj_list

    def create_maze(self):
        for square in self.square_list:
            square.color = WALL
        seed = random.choice(self.square_list)
        stack = [seed]
        seed.color = REG
        adj = self.create_adj_2(REG)
        while stack:
            idx = random.randint(0, len(stack) - 1)
            curr = stack.pop(idx)
            for neighbor in adj[curr]:
                if neighbor.color == WALL:
                    stack.append(neighbor)
                    neighbor.color = REG
                    for square in self.square_list:
                        if square.x == ((curr.x + neighbor.x) // 2) and (square.y == (curr.y + neighbor.y) // 2):
                            square.color = REG

    def create_maze2(self, seeds):
        for square in self.square_list:
            square.color = WALL

        def make_seed():
            y, x = (((random.randint(0, ROWS) * 2) % ROWS), ((random.randint(0, COLS) * 2) % COLS))
            return self.two_d[y][x]

        stack = [make_seed() for _ in range(seeds)]
        adj = self.create_adj_2(REG)
        while stack:
            idx = random.randint(0, len(stack) - 1)
            curr = stack.pop(idx)
            for neighbor in adj[curr]:
                if neighbor.color == WALL or random.random() > 0.98:
                    stack.append(neighbor)
                    neighbor.color = REG
                    for square in self.square_list:
                        if square.x == ((curr.x + neighbor.x) // 2) and (square.y == (curr.y + neighbor.y) // 2):
                            square.color = REG

    def clear(self):
        for square in self.square_list:
            if square.color not in {WALL, START, END}:
                square.color = REG
