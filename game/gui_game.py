#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from tkinter import *
from tkinter import ttk

import copy

from PIL import Image
from PIL import ImageTk

import numpy as np

from board.board import Board
from board.bit_board import BitBoard
from game.base_game import BaseGame

class GuiGame(BaseGame, Frame):

    BK_IMG = "game/img/black2.gif"
    WH_IMG = "game/img/white2.gif"
    PT_IMG = "game/img/puttable2.gif"
    BG_IMG = "game/img/background2.gif"
    B_IMG = "game/img/B.gif"
    W_IMG = "game/img/W.gif"
    BK_U_IMG = "game/img/undoB.gif"
    WH_U_IMG = "game/img/undoW.gif"
    WH_BG = "game/img/wh_bg.gif"
    BK_BG = "game/img/wh_bg.gif"

    def __init__(self, **kwargs):
        self._root = Tk()
        self._root.title("Othello")
        self._root.geometry("900x900")
        super(GuiGame, self).__init__()
        super(BaseGame, self).__init__(self._root)
        board = kwargs['board']
        if board is not None:
            self._board = board
            board_size = board.get_board_size()
        self._window_size = 800
        self._grid_size = int( (self._window_size*0.8)/(board_size+1) )
        self._button_map = []
        self._atk_label = None
        self._bl_count_label = None
        self._wh_count_label = None
        #button image settings
        tmp_img = Image.open(GuiGame.BK_IMG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._bk_img = ImageTk.PhotoImage(tmp_img)

        tmp_img = Image.open(GuiGame.WH_IMG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._wh_img = ImageTk.PhotoImage(tmp_img)

        tmp_img = Image.open(GuiGame.PT_IMG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._pt_img = ImageTk.PhotoImage(tmp_img)

        tmp_img = Image.open(GuiGame.BG_IMG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._bg_img = ImageTk.PhotoImage(tmp_img)

        tmp_img = Image.open(GuiGame.B_IMG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._b_img = ImageTk.PhotoImage(tmp_img)

        tmp_img = Image.open(GuiGame.W_IMG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._w_img = ImageTk.PhotoImage(tmp_img)

        tmp_img = Image.open(GuiGame.BK_U_IMG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._bl_u_img = ImageTk.PhotoImage(tmp_img)

        tmp_img = Image.open(GuiGame.WH_U_IMG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._wh_u_img = ImageTk.PhotoImage(tmp_img)

        tmp_img = Image.open(GuiGame.BK_BG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._bk_bg_img = ImageTk.PhotoImage(tmp_img)

        tmp_img = Image.open(GuiGame.WH_BG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._wh_bg_img = ImageTk.PhotoImage(tmp_img)

    def print_state(self, x, y, bow):
        print('turn: {}'.format(self._turn))
        if bow == 1:
            color = 'black'
        elif bow ==2:
            color = 'white'

        print(color + ' player put stone on ' + '{}, {}'.format(x, y))
        self._board.display_board()
        """
        for i in range(8):
            for j in range(8):
                print(self._board.get_liberty(i,j), end='')
            print('')
        """

    def game_process(self, event, x, y, bow):
        self.append_history(np.array([x, y], dtype='uint64'), bow)
        self._board.put_stone(x, y, bow)
        self.set_nstone()
        opp = self.get_opponent(bow)
        self._board.listing_puttable(opp)
        self.print_state(x, y, bow)
        if self._board.is_no_puttable():
            self._board.listing_puttable(bow)
            if self._board.is_no_puttable():
                print('game finished')
                self.display_gui_board()
                self.end_game()
            else:
                print('nowhere to put stone')
                print(str(opp) + ' pass')
                self.next_turn(is_pass = True)
                self.display_gui_board()
                self.input_coord(bow)
        else:
            self.next_turn(is_pass = False)
            self.display_gui_board()
            self.input_coord(opp)

    def undo_process(self):
        input_list = self._input_history
        if len(input_list) != 0:
            tmp_coord = self._input_history.pop()
            self._board.undo_board(tmp_coord[0], tmp_coord[1])
            bow = self._input_user_history.pop()
            print(bow)
            if bow == 1:
                self._user1.pop_history()
            elif bow == 2:
                self._user2.pop_history()
            self._turn -= 1
            #when undo the first putting, error occur
            if len(self._input_user_history) != 0:
                self._attacker = bow
            else:
                self._attacker = 1
            self.set_nstone()
            self._board.listing_puttable(self._attacker)
            self.display_gui_board()
            self.input_coord(self._attacker)


    def init_gui_board(self):
        self.configure(bg='black')
        self.grid(column=0, row=0)
        bsize = self._board.get_board_size()
        self._button_map = [[ Button() for i in range(bsize)] for j in range(bsize)]
        for x, btns in enumerate(self._button_map):
            for y, btn in enumerate(btns):
                btn.configure(height = self._grid_size, width = self._grid_size)
                btn.grid(column=x, row=y, padx=0, pady=0, ipadx=0, ipady=0)

        start_button = Button(height = 4, width=8, text='start', command=self.start_process, background='#FFFFFF', foreground="#000000")
        start_button.grid(column=8, row=8)

        undo_button  = Button(command=lambda: self.undo_process())
        undo_button.configure(height = self._grid_size, width = self._grid_size, image=self._bl_u_img)
        undo_button.grid(column=bsize, row=3, padx=0, pady=0, ipadx=0, ipady=0)

        self._atk_label = Label(width=self._grid_size, height=self._grid_size, image=self._b_img)
        self._atk_label.grid(column=bsize, row=0, ipadx=0, ipady=0)

        self._bl_count_label = Label(height = 4, width=8, text=str(self._user1.get_nstone()), bg='#000000', foreground="#FFFFFF")
        self._bl_count_label.grid(column=bsize, row=1, ipadx=0, ipady=0)
        self._wh_count_label = Label(height = 4, width=8, text=str(self._user1.get_nstone()), bg='#FFFFFF', foreground="#000000")
        self._wh_count_label.grid(column=bsize, row=2, ipadx=0, ipady=0)


    def display_gui_board(self):
        bsize = self._board.get_board_size()
        grid_size = self._grid_size

        tmp_board = self._board

        for i in range(bsize):
            for j in range(bsize):
                img = self._bg_img
                if tmp_board.get_stone(i, j, 1) == 1:
                    img = self._bk_img
                elif tmp_board.get_stone(i, j, 2) == 1:
                    img = self._wh_img
                elif tmp_board.is_puttable(i, j):
                    img = self._pt_img

                self._button_map[i][j].configure(image=img)

        if self._attacker == 1:
            img = self._b_img
            self._atk_label.configure(image=img)
        elif self._attacker == 2:
            img = self._w_img
            self._atk_label.configure(image=img)
        self._bl_count_label.configure(text=str(self._user1.get_nstone()))
        self._wh_count_label.configure(text=str(self._user2.get_nstone()))

        self._root.update()



    def enable_gui_board(self, bow):

        bsize = self._board.get_board_size()
        tmp_board = self._board

        for i in range(bsize):
            for j in range(bsize):
                if tmp_board.is_puttable(i, j):
                    command = lambda event, row=i, col=j: self.game_process(event, row, col, bow)
                    self._button_map[i][j].bind("<Button-1>", command)
                else:
                    self._button_map[i][j].unbind("<Button-1>")

    def start_process(self):
        self._board.listing_puttable(self._attacker)
        #ボードを表示
        self.init_gui_board()
        self.display_gui_board()
        self.input_coord(self._attacker)

    def start_game(self):
        """
        ゲーム開始までの処理
        """
        print("player {}'s attack".format(self._attacker))
        self._root.configure(bg="#000000")
        self.init_gui_board()
        self.display_gui_board()
        self._root.mainloop()


    def end_game(self):
        """
        ゲーム終了時の処理．勝敗と石の数を表示．
        """

        if self._user1.get_nstone() > self._user2.get_nstone():
            print("Black Win!")
        elif self._user1.get_nstone() < self._user2.get_nstone():
            print("White Win!")
        else:
            print("DRAW!")

def main():
    root = Tk()
    root.title("Othello")
    root.geometry("800x800")
    b = Board()
    b.init_board('init.csv')
    g = GuiBoard(board=b, master=root)
    g.display_gui_board()

    root.mainloop()


if __name__ == '__main__':
    main()
