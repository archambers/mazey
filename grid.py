import pygame
import random
from collections import deque

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 90, 90
ROW_H = HEIGHT // ROWS
COL_W = WIDTH // COLS
PAD = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 128, 128)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("grid")
clock = pygame.time.Clock()

preset = [[1 if random.random() > 0.6 else 0 for _ in range(COLS)] for _ in range(ROWS)]


class Square:
    def __init__(self, x, y):
        if preset[y][x] == 1:
            self.color = BLACK
        else:
            self.color = WHITE
        self.width = COL_W - PAD
        self.height = ROW_H - PAD
        self.x = x
        self.y = y

    def swap_color(self):
        if self.color == WHITE:
            self.color = BLACK
        else:
            self.color = WHITE

    def draw(self):
        pygame.draw.rect(WIN, self.color, (self.x * COL_W, self.y * ROW_H, self.width, self.height))


square_list = [Square(i % COLS, j % ROWS) for i in range(COLS) for j in range(ROWS)]


def create_adj(square_list):
    adj_list = {square: [] for square in square_list}
    for square in adj_list:
        for assoc in square_list:
            if square.y == assoc.y:
                if abs(square.x - assoc.x) == 1 and assoc.color != BLACK:
                    adj_list[square].append(assoc)
            if square.x == assoc.x:
                if abs(square.y - assoc.y) == 1 and assoc.color != BLACK:
                    adj_list[square].append(assoc)
    return adj_list

def create_adj_2(square_list):
    adj_list = {square: [] for square in square_list}
    for square in adj_list:
        for assoc in square_list:
            if square.y == assoc.y:
                if abs(square.x - assoc.x) == 2 and assoc.color != WHITE:
                    adj_list[square].append(assoc)
            if square.x == assoc.x:
                if abs(square.y - assoc.y) == 2 and assoc.color != WHITE:
                    adj_list[square].append(assoc)
    return adj_list


def dfs(start, end, adj):
    stack = [start]
    visited = set()
    path = {}
    while stack:
        curr = stack.pop()
        visited.add(curr)
        for neighbor in adj[curr]:
            if neighbor not in visited:
                stack.append(neighbor)
                path[neighbor] = curr
                neighbor.color = PURPLE
                if neighbor == end:
                    return path
    print('no path')
    return False


def bfs(start, end, adj):
    stack = deque()
    stack.append(start)
    visited = set()
    path = {}
    while stack:
        curr = stack.popleft()
        visited.add(curr)
        for neighbor in adj[curr]:
            if neighbor not in visited:
                stack.append(neighbor)
                path[neighbor] = curr
                neighbor.color = CYAN
                if neighbor == end:
                    return path
    print('no path')
    return False


class Board:
    def draw(self):
        for square in square_list:
            square.draw()

    def create_maze(self):
        for square in square_list:
            square.color = BLACK
        stack = [square_list[0]]
        square_list[0].color = WHITE
        adj = create_adj_2(square_list)
        while stack:
            idx = random.randint(0, len(stack) - 1)
            curr = stack.pop(idx)
            for neighbor in adj[curr]:
                if neighbor.color == BLACK:
                    stack.append(neighbor)
                    neighbor.color = WHITE
                    for square in square_list:
                        if square.x == ((curr.x + neighbor.x) // 2) and (square.y == (curr.y + neighbor.y) // 2):
                            square.color = WHITE






def main():
    run = True
    board = Board()
    start, end = None, None
    board.create_maze()

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for square in square_list:
                    if square.x * COL_W < x < (square.x * COL_W + square.width):
                        if square.y * ROW_H < y < (square.y * ROW_H + square.height):
                            square.swap_color()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    adj = create_adj(square_list)
                    p = dfs(start, end, adj)
                    selected = end
                    counter = 0
                    if p:
                        while selected is not start:
                            if counter > 0:
                                selected.color = BLUE
                            selected = p[selected]
                            counter += 1
                    else:
                        print('no solution')
                    print(f'dfs length: {counter}')

                elif event.key == pygame.K_BACKSPACE:
                    adj = create_adj(square_list)
                    p = bfs(start, end, adj)
                    selected = end
                    counter = 0
                    if p:
                        while selected is not start:
                            if counter > 0:
                                selected.color = YELLOW
                            selected = p[selected]
                            counter += 1
                    else:
                        print('no solution')
                    print(f'bfs length: {counter}')

                elif event.key == pygame.K_r:
                    for square in square_list:
                        if square.color != BLACK:
                            square.color = WHITE
                    start = end = None

                elif event.key == pygame.K_s:
                    x, y = pygame.mouse.get_pos()
                    for square in square_list:
                        if square.x * COL_W < x < (square.x * COL_W + square.width):
                            if square.y * ROW_H < y < (square.y * ROW_H + square.height):
                                if square.color == WHITE:
                                    square.color = GREEN
                                    start = square
                                else:
                                    square.color = WHITE
                                    start = None

                elif event.key == pygame.K_e:
                    x, y = pygame.mouse.get_pos()
                    for square in square_list:
                        if square.x * COL_W < x < (square.x * COL_W + square.width):
                            if square.y * ROW_H < y < (square.y * ROW_H + square.height):
                                if square.color == WHITE:
                                    square.color = RED
                                    end = square
                                else:
                                    square.color = WHITE
                                    end = None


        WIN.fill(BLACK)
        board.draw()

        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()

