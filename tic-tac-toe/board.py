import enum


class Piece(enum.Enum):
    NONE = ' '
    X = 'X'
    O = 'O'


class Board:
    BOARD_SIZE = 3

    def __init__(self):
        self.board = [[Piece.NONE for _ in range(Board.BOARD_SIZE)] for _ in range(Board.BOARD_SIZE)]

    def get_piece(self, row, col):
        return self.board[row][col]

    def set_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_cell_empty(self, row, col):
        return self.board[row][col] == Piece.NONE

    def is_full(self):
        for row in range(Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                if self.is_cell_empty(row, col):
                    return False

        return True

    def is_victory(self) -> Piece:
        if self._check_victory(Piece.X):
            return Piece.X

        if self._check_victory(Piece.O):
            return Piece.O

        return Piece.NONE

    def _check_victory(self, piece_type):
        return (self._is_row_win(piece_type)
                or self._is_col_win(piece_type)
                or self._is_diag_win(piece_type))

    def _is_row_win(self, piece_type):
        for row in range(Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                if self.board[row][col] != piece_type:
                    return False

        return True

    def _is_col_win(self, piece_type):
        for col in range(Board.BOARD_SIZE):
            for row in range(Board.BOARD_SIZE):
                if self.board[row][col] != piece_type:
                    return False

        return True

    def _is_diag_win(self, piece_type):
        if all(self.board[i][i] == piece_type for i in range(Board.BOARD_SIZE)):
            return True

        if all(self.board[i][Board.BOARD_SIZE - i - 1] == piece_type for i in range(Board.BOARD_SIZE)):
            return True

        return False

    def __str__(self):
        result = "+---+---+---+"
        for row in range(Board.BOARD_SIZE):
            result += "\n| "
            for col in range(Board.BOARD_SIZE):
                result += self.board[row][col].value + " | "

            result += "\n+---+---+---+"

        return result
