import pygame
import random
from constants import *
from board import Square
from algorithms import rtdfs, rtbfs, rtastar

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("grid")
clock = pygame.time.Clock()

# preset = [[1 if random.random() > 0.6 else 0 for _ in range(COLS)] for _ in range(ROWS)]


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
    adj = create_adj(square_list)

    algos = {'dfs': rtdfs, 'bfs': rtbfs, 'astar': rtastar}

    def run_maze_solver(algo, start, end):
        p = algos[algo](start, end, adj)
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
            clock.tick(60)
        print(f'{counter} squares explored via {algo}')

        selected = end
        counter2 = 0
        while selected is not start:
            if counter2 > 0:
                selected.color = YELLOW
            selected = path[selected]
            counter2 += 1
        print(f'{algo} path is {counter2} long')

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # allows player to draw or remove walls by clicking mouse on square
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                two_d[y // ROW_H][x // COL_W].swap_color()


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    run_maze_solver('dfs', start, end)

                if event.key == pygame.K_o:
                    run_maze_solver('bfs', start, end)

                if event.key == pygame.K_i:
                    run_maze_solver('astar', start, end)

                # allows player to reset the board with the same maze
                elif event.key == pygame.K_r:
                    for square in square_list:
                        if square.color not in {BLACK, GREEN, RED}:
                            square.color = WHITE

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

