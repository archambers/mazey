from constants import *
import random
import pygame

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


class Square:
    def __init__(self, x, y):
        # if preset[y][x] == 1:
        #     self.color = BLACK
        # else:
        #     self.color = WHITE
        self.width = COL_W - PAD
        self.height = ROW_H - PAD
        self.x = x
        self.y = y
        self.color = WHITE

    def swap_color(self):
        if self.color == WHITE:
            self.color = BLACK
        else:
            self.color = WHITE

    def draw(self):
        pygame.draw.rect(WIN, self.color,
                         (self.x * COL_W, self.y * ROW_H,
                          self.width, self.height))
