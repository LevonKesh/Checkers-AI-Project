import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (245, 106, 0)
WHITE = (245, 214, 198)
BLACK = (102, 67, 31)
BLUE = (230, 87, 87)
GREY = (128,128,128)
MINIMAX = True

CROWN = pygame.transform.scale(pygame.image.load('crown.png'), (44, 25))