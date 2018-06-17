from tkinter import *
from tkinter import ttk

from board.board import Board
from board.bit_board import BitBoard
from user.user import User
from user.ai_user import AiUser, RandomUser
from game.gui_game import GuiGame

#import eval_test

if __name__ == '__main__':

    BOARD_INIT_FILE = 'init/init.csv'

    user1 = User(1)
    user2 = AiUser(2)
    board = BitBoard()
    board.init_board(BOARD_INIT_FILE)
    game = GuiGame(board=board)
    game.set_user(user1, 1)
    game.set_user(user2, 2)
    game.set_board(board)

    # start game
    game.start_game()
    game.end_game()
