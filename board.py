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
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
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

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.king:
            moves.update(self._traverse_left(row - 1, -1, -1, piece.color, piece.king, left))
            moves.update(self._traverse_right(row - 1, -1, -1, piece.color, piece.king, right))
            moves.update(self._traverse_left(row + 1, ROWS, 1, piece.color, piece.king, left))
            moves.update(self._traverse_right(row + 1, ROWS, 1, piece.color, piece.king, right))
        else:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, piece.king, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, piece.king, right))
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, piece.king, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, piece.king, right))

        max_len_move = max([len(i) for i in moves.values()], default=100000)
        moves = {key: val for key, val in moves.items() if len(val) >= max_len_move}
        return moves

    def _traverse_left(self, start, stop, step, color, king, left, skipped=[]):
        moves = {}
        last = []
        allow_reverse = False
        for r in range(start, stop, step):
            if (r, left) in moves.keys():
                break
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if not king and not last and ((color == RED and step == 1) or (color == WHITE and step == -1)):
                    break

                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        if not king:
                            row = max(r - 3, -1)
                        else:
                            row = -1
                    else:
                        if not king:
                            row = min(r + 3, ROWS)
                        else:
                            row = ROWS
                    moves.update(self._traverse_left(r + step, row, step, color, king, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, king, left + 1, skipped=last))
                    if king and allow_reverse:

                        if row == ROWS:
                            moves.update(self._traverse_left(r - step, -1, -step, color, king, left - 1, skipped=last))
                        else:
                            moves.update(self._traverse_left(r - step, ROWS, -step, color, king, left - 1, skipped=last))
                if not king:
                    break
                allow_reverse = False
            elif current.color == color:
                break
            else:
                last = [current]
                allow_reverse = True

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, king, right, skipped=[]):
        moves = {}
        last = []
        allow_reverse = False
        for r in range(start, stop, step):
            if (r, right) in moves.keys():
                break
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if not king and not last and ((color == RED and step == 1) or (color == WHITE and step == -1)):
                    break
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        if not king:
                            row = max(r - 3, -1)
                        else:
                            row = -1
                    else:
                        if not king:
                            row = min(r + 3, ROWS)
                        else:
                            row = ROWS

                    # if not king:
                    moves.update(self._traverse_left(r + step, -1, step, color, king, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, king, right + 1, skipped=last))
                    if king and allow_reverse:
                        if row == ROWS:
                            moves.update(self._traverse_right(r - step, -1, -step, color, king, right + 1, skipped=last))
                        else:
                            moves.update(self._traverse_right(r - step, ROWS, -step, color, king, right + 1, skipped=last))
                if not king:
                    break
                allow_reverse = False
            elif current.color == color:
                break
            else:
                last = [current]
                allow_reverse = True

            right += 1

        return moves

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 2 - self.red_kings * 2)