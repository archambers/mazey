import pygame
import random
from collections import deque

pygame.init()

HEIGHT, WIDTH = 700, 1000
ROWS, COLS = 70, 100
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


two_d = [[Square(i % COLS, j % ROWS) for i in range(COLS)] for j in range(ROWS)]
square_list = [square for row in two_d for square in row]


def create_adj(square_list):
    adj_list = {square: set() for square in square_list}
    for square in adj_list:
        for assoc in square_list:
            if square.y == assoc.y:
                if abs(square.x - assoc.x) == 1 and assoc.color != BLACK:
                    adj_list[square].add(assoc)
            if square.x == assoc.x:
                if abs(square.y - assoc.y) == 1 and assoc.color != BLACK:
                    adj_list[square].add(assoc)
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


def rtdfs(start, end, adj):
    stack = [start]
    visited = set()
    path = {}
    while stack:
        curr = stack.pop()
        visited.add(curr)
        nbrs = []
        for neighbor in adj[curr]:
            if neighbor not in visited:
                stack.append(neighbor)
                path[neighbor] = curr
                nbrs.append(neighbor)
        yield (curr, nbrs, path)


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
    def __init__(self):
        self.s_l = [[Square(col % COLS, row % ROWS) for col in range(COLS)]
                    for row in range(ROWS)]
        self.flat = [square for row in self.s_l for square in row]

    def draw(self):
        for square in square_list:
            square.draw()

    def create_maze(self):
        for square in square_list:
            square.color = BLACK
        seed = random.choice(square_list)
        stack = [seed]
        seed.color = WHITE
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

            # allows player to draw or remove walls by clicking mouse on square
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                two_d[y // ROW_H][x // COL_W].swap_color()
                # for square in square_list:
                #     if square.x * COL_W < x < (square.x * COL_W + square.width):
                #         if square.y * ROW_H < y < (square.y * ROW_H + square.height):
                #             square.swap_color()

            if event.type == pygame.KEYDOWN:

                # starts dfs maze solver
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

                if event.key == pygame.K_p:
                    adj = create_adj(square_list)
                    p = rtdfs(start, end, adj)
                    finished = False
                    counter = 0
                    path = None
                    while not finished:
                        cont = next(p)
                        if cont[0] == end:
                            break
                        if counter > 0:
                            cont[0].color = PURPLE
                        for n in cont[1]:
                            if n == end:
                                finished = True
                                path = cont[2]
                                break
                            n.color = CYAN
                        counter += 1
                        board.draw()
                        pygame.display.update()
                        clock.tick(30)

                    selected = end
                    counter2 = 0
                    while selected is not start:
                            if counter2 > 0:
                                selected.color = YELLOW
                            selected = path[selected]
                            counter2 += 1


                # starts bfs maze solver
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

                # allows player to reset the board with the same maze
                elif event.key == pygame.K_r:
                    for square in square_list:
                        if square.color != BLACK:
                            square.color = WHITE
                    start = end = None

                # allows player to set start by hovering
                # over square and pressing s
                elif event.key == pygame.K_s:
                    x, y = pygame.mouse.get_pos()
                    square = two_d[y // ROW_H][x // COL_W]
                    if square.color == WHITE:
                        square.color = GREEN
                        start = square
                    else:
                        square.color = WHITE
                        start = None
                    # for square in square_list:
                    #     if square.x * COL_W < x < (square.x * COL_W + square.width):
                    #         if square.y * ROW_H < y < (square.y * ROW_H + square.height):
                    #             if square.color == WHITE:
                    #                 square.color = GREEN
                    #                 start = square
                    #             else:
                    #                 square.color = WHITE
                    #                 start = None

                # allows player to set goal by hovering
                # over square and pressing e
                elif event.key == pygame.K_e:
                    x, y = pygame.mouse.get_pos()
                    square = two_d[y // ROW_H][x // COL_W]
                    if square.color == WHITE:
                        square.color = RED
                        end = square
                    else:
                        square.color = WHITE
                        end = None

                # allows player to draw a new maze and reset
                elif event.key == pygame.K_d:
                    start = end = None
                    board.create_maze()


        WIN.fill(BLACK)
        board.draw()

        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()

