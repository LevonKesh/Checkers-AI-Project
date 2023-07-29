from datetime import datetime

import pygame

from alpha_beta import alpha_beta
from constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, MINIMAX
from checker import Game
from minimax import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)


    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            if MINIMAX:
                now = datetime.now().timestamp()
                value, new_board = minimax(game.get_board(), 4, WHITE, game)
                print("Passed: ", datetime.now().timestamp() - now )
            else:
                now = datetime.now().timestamp()
                value, new_board = alpha_beta(game.get_board(),5, float('-inf'), float('inf'), True, game)
                print("Passed: ", datetime.now().timestamp() - now )
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()


main()