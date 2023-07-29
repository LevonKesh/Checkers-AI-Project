import pygame
from constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, GREY
from piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, (255, 255, 255), (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 and piece.color == WHITE:
            piece.make_king()
            self.white_kings += 1
        elif row == 0 and piece.color == RED:
            piece.make_king()
            self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, RED))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def is_in_board(self, row, col):
        if 0 <= row < ROWS and 0 <= col < ROWS:
            return True
        else:
            return False

    def is_free(self, row, col):
        return self.board[row][col] == 0

    def up_left_move(self, row, col):
        moves = {}
        if self.is_in_board(row - 1, col - 1) and self.is_free(row - 1, col - 1):
            moves[(row - 1, col - 1)] = []
        return moves

    def up_right_move(self, row, col):
        moves = {}
        if self.is_in_board(row - 1, col + 1) and self.is_free(row - 1, col + 1):
            moves[(row - 1, col + 1)] = []
        return moves

    def down_left_move(self, row, col):
        moves = {}
        if self.is_in_board(row + 1, col - 1) and self.is_free(row + 1, col - 1):
            moves[(row + 1, col - 1)] = []
        return moves

    def down_right_move(self, row, col):
        moves = {}
        if self.is_in_board(row + 1, col + 1) and self.is_free(row + 1, col + 1):
            moves[(row + 1, col + 1)] = []
        return moves

    ## QUEEN MOVES
    def queen_up_left(self, row, col, piece, shift_possible=False):
        moves = {}
        if self.up_left_move(row, col) and not shift_possible:
            moves.update(self.up_left_move(row, col))
            moves.update(self.queen_up_left(row - 1, col - 1, piece))

        elif not self.is_in_board(row - 1, col - 1):
            return moves
        elif self.board[row][col].color != piece.color:
            moves = {**moves,
                     **self.up_left_jump(row, col, piece, moves),
                     **self.queen_up_left(row - 2, col - 2, piece, shift_possible=shift_possible),
                     **self.queen_up_right(row - 2, col - 2, piece, shift_possible=not shift_possible),
                     **self.queen_down_left(row - 2, col - 2, piece, shift_possible=not shift_possible),
                     **self.queen_down_right(row - 2, col - 2, piece, shift_possible=not shift_possible)
                     }

        return moves

    def queen_up_right(self, row, col, piece, shift_possible=False):
        moves = {}
        if self.up_left_move(row, col) and not shift_possible:
            moves.update(self.up_left_move(row, col))
            moves.update(self.queen_up_left(row - 1, col + 1, piece))

        elif not self.is_in_board(row - 1, col + 1):
            return moves
        elif self.board[row][col].color != piece.color:
            moves = {**moves,
                     **self.up_left_jump(row, col, piece, moves),
                     **self.queen_up_left(row - 2, col + 2, piece, shift_possible=not shift_possible),
                     **self.queen_up_right(row - 2, col + 2, piece, shift_possible=shift_possible),
                     **self.queen_down_left(row - 2, col + 2, piece, shift_possible=not shift_possible),
                     **self.queen_down_right(row - 2, col + 2, piece, shift_possible=not shift_possible)
                     }

        return moves

    def queen_down_left(self, row, col, piece, shift_possible=False):
        moves = {}
        if self.up_left_move(row, col) and not shift_possible:
            moves.update(self.up_left_move(row, col))
            moves.update(self.queen_up_left(row + 1, col - 1, piece))

        elif not self.is_in_board(row + 1, col - 1):
            return moves
        elif self.board[row][col].color != piece.color:
            moves = {**moves,
                     **self.up_left_jump(row, col, piece, moves),
                     **self.queen_up_left(row + 2, col - 2, piece, shift_possible=not shift_possible),
                     **self.queen_up_right(row + 2, col - 2, piece, shift_possible=not shift_possible),
                     **self.queen_down_left(row + 2, col - 2, piece, shift_possible=shift_possible),
                     **self.queen_down_right(row + 2, col - 2, piece, shift_possible=not shift_possible)
                     }

        return moves

    def queen_down_right(self, row, col, piece, shift_possible=False):
        moves = {}
        if self.up_left_move(row, col) and not shift_possible:
            moves.update(self.up_left_move(row, col))
            moves.update(self.queen_up_left(row + 1, col + 1, piece))

        elif not self.is_in_board(row + 1, col + 1):
            return moves
        elif self.board[row][col].color != piece.color:
            moves = {**moves,
                     **self.up_left_jump(row, col, piece, moves),
                     **self.queen_up_left(row + 2, col + 2, piece, shift_possible=not shift_possible),
                     **self.queen_up_right(row + 2, col + 2, piece, shift_possible=not shift_possible),
                     **self.queen_down_left(row + 2, col + 2, piece, shift_possible=not shift_possible),
                     **self.queen_down_right(row + 2, col + 2, piece, shift_possible=shift_possible)
                     }

        return moves

    def up_left_jump(self, row, col, piece, moves: dict):
        if self.is_in_board(row - 2, col - 2)\
                and self.is_in_board(row - 1, col - 1)\
                and not self.is_free(row - 1, col - 1) \
                and self.is_free(row - 2, col - 2) \
                and piece.color != self.board[row - 1][col - 1].color:
            val = moves.get((row, col), [])
            val.append(self.get_piece(row - 1, col - 1))
            moves[(row - 2, col - 2)] = val
            if row == 0 and not piece.king:
                piece.king = True
                return {**moves,
                        **self.queen_down_left(row, col, piece, True),
                        **self.queen_down_right(row, col, piece, True)}
            if piece.king:
                return moves
            moves = {**moves,
                     **self.up_left_jump(row - 2, col - 2, piece, moves),
                     **self.up_right_jump(row - 2, col - 2, piece, moves),
                     **self.down_left_jump(row - 2, col - 2, piece, moves)}

        return moves

    def up_right_jump(self, row, col, piece, moves: dict):
        if self.is_in_board(row - 2, col + 2)\
                and self.is_in_board(row - 1, col + 1)\
                and not self.is_free(row - 1, col + 1) \
                and self.is_free(row - 2, col + 2) \
                and piece.color != self.board[row - 1][col + 1].color:
            val = moves.get((row, col), [])
            val.append(self.get_piece(row - 1, col + 1))
            moves[(row - 2, col + 2)] = val
            if row == 0 and not piece.king:
                piece.king = True
                return {**moves,
                        **self.queen_down_left(row, col, piece, True),
                        **self.queen_down_right(row, col, piece, True)}
            if piece.king:
                return moves
            moves = {**moves,
                     **self.up_left_jump(row - 2, col + 2, piece, moves),
                     **self.up_right_jump(row - 2, col + 2, piece, moves),
                     **self.down_right_jump(row - 2, col + 2, piece, moves)}

        return moves

    def down_left_jump(self, row, col, piece, moves: dict):
        if self.is_in_board(row + 2, col - 2) \
                and self.is_in_board(row + 1, col - 1) \
                and not self.is_free(row + 1, col - 1) \
                and self.is_free(row + 2, col - 2) \
                and piece.color != self.board[row + 1][col - 1].color:

            val = moves.get((row, col), [])
            val.append(self.get_piece(row + 1, col - 1))
            moves[(row + 2, col - 2)] = val
            if row == 7 and not piece.king:
                piece.king = True
                return {**moves,
                        **self.queen_up_left(row, col, piece, True),
                        **self.queen_up_right(row, col, piece, True)}
            if piece.king:
                return moves
            moves = {**moves,
                     **self.up_left_jump(row + 2, col - 2, piece, moves),
                     **self.down_right_jump(row + 2, col - 2, piece, moves),
                     **self.down_left_jump(row + 2, col - 2, piece, moves)}

        return moves

    def down_right_jump(self, row, col, piece, moves: dict):
        if self.is_in_board(row + 2, col + 2)\
                and self.is_in_board(row + 1, col + 1)\
                and not self.is_free(row + 1, col + 1) \
                and self.is_free(row + 2, col + 2) \
                and piece.color != self.board[row + 1][col + 1].color:
            val = moves.get((row, col), [])
            val.append(self.get_piece(row + 1, col + 1))
            moves[(row + 2, col + 2)] = val
            if piece.king:
                return moves
            if row == 7 and not piece.king:
                piece.king = True
                return {**moves,
                        **self.queen_up_left(row, col, piece, True),
                        **self.queen_up_right(row, col, piece, True)}
            moves = {**moves,
                     **self.down_left_jump(row + 2, col + 2, piece, moves),
                     **self.down_right_jump(row + 2, col + 2, piece, moves),
                     **self.up_right_jump(row + 2, col + 2, piece, moves)}

        return moves

    def all_jumps(self, row, col, piece):
        moves = {**self.up_left_jump(row, col, piece, {}),
                 **self.up_right_jump(row, col, piece, {}),
                 **self.down_left_jump(row, col, piece, {}),
                 **self.down_right_jump(row, col, piece, {})}
        return moves

    def get_valid_moves(self, piece):
        row, col = piece.row, piece.col
        moves = {}
        if piece != 0:
            if piece.king:
                moves = {**self.queen_up_left(row, col, piece),
                         **self.queen_up_right(row, col, piece),
                         **self.queen_up_right(row, col, piece),
                         **self.queen_up_right(row, col, piece)}

            elif piece.color == WHITE:
                forward_moves = {**self.up_left_move(row, col), **self.up_right_move(row, col)}
                jumping_moves = self.all_jumps(row, col, piece)
                moves = {**forward_moves, **jumping_moves}

            elif piece.color == RED:
                forward_moves = {**self.down_left_move(row, col), **self.down_right_move(row, col)}
                jumping_moves = self.all_jumps(row, col, piece)
                moves = {**forward_moves, **jumping_moves}
            if moves.values():
                max_len_move = len(max(moves.values(), key=len))
            else:
                max_len_move = 0
            moves = {k: v for k, v in moves.items() if len(v) >= max_len_move}
            return moves
        else:
            return {}

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces


    def red_evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 2 - self.red_kings * 2)

    def white_evaluate(self):
        return self.red_left - self.white_left + (self.red_left * 2 - self.white_left * 2)
