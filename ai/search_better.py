import copy
import math

import numba
import cython

from ai import eval_test
from ai import book_manager
from board.bit_board import BitBoard

class Search():
    def __init__(self, board, own, opponent, turn, game):
        self._turn = turn
        self._own = own
        self._opponent = opponent
        self._index = None
        self._board = board
        self._game = game
        self._depth = 6
        if(turn >= 0 and turn <= 50):
            self._eval = eval_test.MidEvaluator(board)
        else:
            self._eval = eval_test.WLDEvaluator()

    def search(self):
        self.bm = book_manager.BookManager(self._own)
        tmp = self.alpha_beta(self._board, self._own, -math.inf, math.inf, self._depth)
        return tmp, self._index[0], self._index[1]

    #alpha beta algorithm
    def alpha_beta(self, board, atk, alpha, beta, depth):
        if depth == 0:
            return  self._eval.evaluate(board, atk)

        if(atk == self._own):
            board.listing_puttable(atk)
            legals = board.get_puttable_list()
            #print("find : ", self.bm.find(board, self._game))
            if len(legals) != 0:
                # for coord in legals:
                for coord in self.bm.find(board, self._game):
                    tmp_board = copy.deepcopy(board)
                    tmp_board.put_stone(int(coord[0]), int(coord[1]), atk)
                    score = self.alpha_beta(tmp_board, self._opponent, alpha, beta, depth-1)
                    if score > alpha:
                        alpha = score
                        if depth==self._depth:
                            self._index = coord
                    if depth==self._depth:
                    #beta cut
                    if alpha >= beta:
                        break
                return alpha
            else:
                tmp_board = copy.deepcopy(board)
                return max([alpha, self.alpha_beta(tmp_board, self._opponent, alpha, beta, depth-1)])
        else:
            board.listing_puttable(atk)
            legals = board.get_puttable_list()
            if len(legals) != 0:
                # for coord in legals:
                for coord in self.bm.find(board, self._game):
                    tmp_board = copy.deepcopy(board)
                    tmp_board.put_stone(int(coord[0]), int(coord[1]), self._opponent)
                    score = self.alpha_beta(tmp_board, self._own, alpha, beta, depth-1)
                    if score < beta:
                        beta = score
                    if alpha >= beta:
                        break
                return beta
            else:
                tmp_board = copy.deepcopy(board)
                return min([beta, self.alpha_beta(tmp_board, self._own, alpha, beta, depth-1)])


    #nega scout algorithm
    def nega_scout(self, board, atk, alpha, beta, depth):
        if(depth == 0):
            return  self._eval.evaluate(board, self._opponent)

    def move_ordering(self, node, board, atk, depth):
        if depth == 0:
            return  self._eval.evaluate(board, atk)
        board.listing_puttable(akt)
