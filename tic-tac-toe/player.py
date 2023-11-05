import random
import threading
import time

from board import Board, Piece
from message_manager import MessageManager
from message import Message


class Player:
    def __init__(
            self,
            player_type: Piece,
            message_manager: MessageManager,
            board: Board):

        self.player_type = player_type
        self.board = board

        self.message_manager = message_manager
        self.message_manager.set_handler(self.handle_message)

        # Let player X always start
        self.turn = True if self.player_type == Piece.X else False
        self.turn_count = 1

        self.is_turn = threading.Condition()

        print("Hi! I'm player ", self.player_type.value)

    def play(self):
        time.sleep(5)

        while True:
            # This coordination is needed since self.handle_message
            # runs on a different thread
            with self.is_turn:
                while not self.turn:
                    self.is_turn.wait()

            # Check if the game ended after the other player's move
            victory = self.board.is_victory()
            if victory != Piece.NONE or self.board.is_full():
                break

            print(f"=================TURN {self.turn_count}=================")
            self._make_move()

            print(self.board)

            # Check if the game ended after my move
            victory = self.board.is_victory()
            if victory != Piece.NONE or self.board.is_full():
                break

            self.turn_count += 1
            self.turn = False

            time.sleep(1)

        if victory == self.player_type:
            print("**********I won!**********")
        elif victory == Piece.NONE:
            print("**********It's a draw!**********")
        else:
            print("**********I lost!**********")

        print(f"=================FINAL BOARD=================")
        print(self.board)

    def handle_message(self, message: Message):
        if message.player == self.player_type.value:
            return

        self.board.set_piece(message.row, message.col, Piece(message.player))

        with self.is_turn:
            self.turn = True
            self.is_turn.notify_all()

    def _make_move(self):
        # We ain't implementing an AI algorithm,
        # since it's a bit out of scope, so just pick a random cell
        # and place the piece there.
        row = random.randint(0, Board.BOARD_SIZE - 1)
        col = random.randint(0, Board.BOARD_SIZE - 1)

        while not self.board.is_cell_empty(row, col):
            row = random.randint(0, Board.BOARD_SIZE - 1)
            col = random.randint(0, Board.BOARD_SIZE - 1)

        self.board.set_piece(row, col, self.player_type)

        self.message_manager.send_move(Message(self.player_type.value, row, col))
