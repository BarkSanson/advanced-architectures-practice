import sys

from message_manager import MessageManager
from player import Player
from board import Board, Piece


def main():

    if len(sys.argv) != 2:
        print("Usage: python main.py <player_type>")
        return

    player_piece = Piece(sys.argv[1])

    board = Board()
    message_manager = MessageManager()
    player = Player(player_piece, message_manager, board)

    player.play()


if __name__ == "__main__":
    main()
