import pygame
from constants import *
from board import Board
from algorithms import rtdfs, rtbfs, rtastar, rtastarm

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("grid")
clock = pygame.time.Clock()

# preset = [[1 if random.random() > 0.6 else 0 for _ in range(COLS)] for _ in range(ROWS)]


def main():
    run = True
    board = Board()
    start, end = None, None
    board.create_maze()
    # adj = board.create_adj()
    changed = False

    algos = {'dfs': rtdfs, 'bfs': rtbfs, 'astar': rtastar, 'astarm': rtastarm}

    def run_maze_solver(algo, start, end):
        # p = algos[algo](start, end, adj)
        p = algos[algo](start, end, board.two_d)
        finished = False
        counter = 0
        path = None
        while not finished:
            cont = next(p)
            if cont[0] == end:
                break
            if counter > 0:
                cont[0].color = CHECKED
            for n in cont[1]:
                if n == end:
                    finished = True
                    path = cont[2]
                    break
                n.color = FRONTIER
            counter += 1
            board.draw()
            pygame.display.update()
            # clock.tick(60)
        print(f'{counter} squares explored via {algo}')

        selected = end
        counter2 = 0
        while selected is not start:
            if counter2 > 0:
                selected.color = PATH
            selected = path[selected]
            counter2 += 1
        print(f'{algo} path is {counter2} long')

    while run:

        # if changed:
        #     adj = board.create_adj()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # allows player to draw or remove walls by clicking mouse on square
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                board.two_d[y // ROW_H][x // COL_W].swap_color()
                changed = True


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    run_maze_solver('dfs', start, end)
                    changed = False

                if event.key == pygame.K_o:
                    run_maze_solver('bfs', start, end)
                    changed = False

                if event.key == pygame.K_i:
                    run_maze_solver('astar', start, end)
                    changed = False

                if event.key == pygame.K_u:
                    run_maze_solver('astarm', start, end)

                # allows player to reset the board with the same maze
                elif event.key == pygame.K_r:
                    board.clear()

                # allows player to set start by hovering
                # over square and pressing s
                elif event.key == pygame.K_s:
                    x, y = pygame.mouse.get_pos()
                    square = board.two_d[y // ROW_H][x // COL_W]
                    if square.color == REG:
                        square.color = START
                        start = square
                    else:
                        square.color = REG
                        start = None

                # over square and pressing e
                elif event.key == pygame.K_e:
                    x, y = pygame.mouse.get_pos()
                    square = board.two_d[y // ROW_H][x // COL_W]
                    if square.color == REG:
                        square.color = END
                        end = square
                    else:
                        square.color = REG
                        end = None

                # allows player to draw a new maze and reset
                elif event.key == pygame.K_d:
                    start = end = None
                    board.create_maze()
                    changed = True


        WIN.fill(BLACK)
        board.draw()

        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()

