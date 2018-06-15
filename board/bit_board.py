import numpy as np
from board.board import Board

#%%cython
import cython

class BitBoard():


    PARSER = ','

    def __init__(self):
        #石の数
        self._nstone = 0
        #ボードのサイズ 変更できるようにする予定
        self._board_size = 8
        #黒ボード
        self._bl_board = 0x0000000000000000
        #白ボード
        self._wh_board = 0x0000000000000000
        #石を置ける場所だけフラグ
        self._puttable_map = 0x0000000000000000
        #init liberty
        self._liberty = [[8 for i in range(self._board_size + 2)] for j in range(self._board_size + 2)]
        self._liberty[1][1] = self._liberty[1][self._board_size] = self._liberty[self._board_size][1] = self._liberty[self._board_size][self._board_size] = 3
        for i in range(2, self._board_size):
            self._liberty[1][i] = self._liberty[i][1] = self._liberty[self._board_size][i] = self._liberty[i][self._board_size] = 5
        #各ターンでボードを保存
        self._bl_board_history = []
        self._wh_board_history = []
        self.input_history = []
        #石を置ける場所が入っている
        self._puttable_list = []


    def get_opponent(self, bow):
        """
        敵ユーザの番号を返す
        """
        return bow % 2 + 1


    def set_stone(self, x, y, bow):
        """
        x座標とy座標の和coord_sumの位置に，bowで指定された石をおく
        """
        y *= self._board_size

        if bow == 1:
            self._bl_board = self._bl_board & (1 << (x + 8*y))
        elif bow == 2:
            self._wh_board = self._wh_board & (1 << (x + 8*y))

    def get_stone(self, x, y, bow):
        """
        指定されたbowの盤面のcoord_sumの状態を判定
        """
        if bow == 1:
            return (self._bl_board >> (x + 8*y)) & 0b1
        elif bow == 2:
            return (self._wh_board >> (x + 8*y)) & 0b1


    def get_player(self, x, y):
        """
        指定された座標に置かれている石をおいたプレイヤーを返す
        """
        if(self.get_stone(x, y, 1) == 1):
            return 1
        elif(self.get_stone(x, y, 2) == 1):
            return 2
        else:
            return 0


    def get_player(self, x, y):
        """
        指定された座標に置かれている石をおいたプレイヤーを返す
        """
        if(self.get_stone(x, y, 1) == 1):
            return 1
        elif(self.get_stone(x, y, 2) == 1):
            return 2
        else:
            return 0


    def undo_board(self, x, y):
        self.pop_board_history(1)
        self.pop_board_history(2)
        self.set_board(self._bl_board_history[-1], 1)
        self.set_board(self._wh_board_history[-1], 2)
        self.change_liberty(x, y, 1)


    def get_board_size(self):
        """
        ボードのサイズをゲット
        """
        return self._board_size


    def get_input_history(self):
        return self.input_history


    def set_board(self, board, bow):
        if bow == 1:
            self._bl_board = board
        elif bow == 2:
            self._wh_board = board


    def append_board_history(self, board, bow):
        if bow == 1:
            self._bl_board_history.append(board)
        elif bow == 2:
            self._wh_board_history.append(board)


    def append_input_history(self, x, y):
        coord = np.array([x,y])
        self.input_history.append(coord)


    def pop_board_history(self, bow):
        if bow == 1:
            self._bl_board_history.pop()
        elif bow == 2:
            self._wh_board_history.pop()


    def init_board(self, file_path):
        """
        csvファイルを元に，ボードを初期化
        """
        with open(file_path) as f:
            for i, row in enumerate(f):
                col = row.split(self.PARSER)
                for j, stone in enumerate(col):
                    if stone == '1':
                        self._bl_board |= (1<< (j+8*i))
                        self.change_liberty(i, j, -1)
                    elif stone == '2':
                        self._wh_board |= (1<< (j+8*i))
                        self.change_liberty(i, j, -1)

            self.append_board_history(self._bl_board, 1)
            self.append_board_history(self._wh_board, 2)


    def init_board_from_board(self, board):
        """
        Boardオブジェクトを元に盤面を初期化
        """
        board_size = board.get_board_size()
        for i in range(board_size):
            for j in range(board_size):
                stone = board.get_stone(np.array([i,j]))
                if stone == 1:
                    self._bl_board = self._bl_board | (1<<(i+j*8))
                elif stone == 2:
                    self._wh_board = self._bl_board | (1<<(i+j*8))


    def get_board_half(self, bow):
        if bow == 1:
            return self._bl_board
        elif bow == 2:
            return self._wh_board


    def display_board(self):
        """
        boardを表示
        """

        tmp_bl_board = self.get_board_half(1)
        tmp_wh_board = self.get_board_half(2)

        tmp_pt_board = self._puttable_map

        print(" ", end="")
        for i in range(self._board_size):
            print(" {}".format(i), end="")
        print("")
        bar = "-"*18
        print(bar)
        for i in range(self._board_size):
            print("{}|".format(i), end="")
            for j in range(self._board_size):
                coord = j + i*8
                stone = " "
                if tmp_bl_board >> coord & 1 == 1:
                    stone = "B"
                elif tmp_wh_board >> coord & 1 == 1:
                    stone = "W"
                elif tmp_pt_board >> coord & 1 == 1:
                    stone = "*"

                print("{}|".format(stone), end="")
            print("")

        for i in range(8):
            for j in range(8):
                print(self.get_liberty(j, i), end='')
            print('')


    def listing_puttable(self, bow):
        """
        石を置ける場所のリストを作成
        """
        atk_board = self.get_board_half(bow)
        opp = self.get_opponent(bow)
        opp_board = self.get_board_half(opp)

        #左右端の番人
        horizontal_watch_board = opp_board & 0x7e7e7e7e7e7e7e7e
        #上下端の番人
        vertical_watch_board = opp_board & 0x00FFFFFFFFFFFF00
        #全端の番人
        all_side_watch_board = opp_board & 0x007e7e7e7e7e7e00
        #空きマスにフラグがたったボード
        blank_board = ~(atk_board | opp_board)

        #8方向チェック (・一度に返せる石は最大6つ ・高速化のためにforを展開)
        #左方向
        tmp = horizontal_watch_board & (atk_board << 1)
        tmp |= horizontal_watch_board & (tmp << 1)
        tmp |= horizontal_watch_board & (tmp << 1)
        tmp |= horizontal_watch_board & (tmp << 1)
        tmp |= horizontal_watch_board & (tmp << 1)
        tmp |= horizontal_watch_board & (tmp << 1)
        legal_board = blank_board & (tmp << 1)

        #右方向
        tmp = horizontal_watch_board & (atk_board >> 1)
        tmp |= horizontal_watch_board & (tmp >> 1)
        tmp |= horizontal_watch_board & (tmp >> 1)
        tmp |= horizontal_watch_board & (tmp >> 1)
        tmp |= horizontal_watch_board & (tmp >> 1)
        tmp |= horizontal_watch_board & (tmp >> 1)
        legal_board |= blank_board & (tmp >> 1)

        #上
        tmp = vertical_watch_board & (atk_board << 8)
        tmp |= vertical_watch_board & (tmp << 8)
        tmp |= vertical_watch_board & (tmp << 8)
        tmp |= vertical_watch_board & (tmp << 8)
        tmp |= vertical_watch_board & (tmp << 8)
        tmp |= vertical_watch_board & (tmp << 8)
        legal_board |= blank_board & (tmp << 8)

        #下
        tmp = vertical_watch_board & (atk_board >> 8)
        tmp |= vertical_watch_board & (tmp >> 8)
        tmp |= vertical_watch_board & (tmp >> 8)
        tmp |= vertical_watch_board & (tmp >> 8)
        tmp |= vertical_watch_board & (tmp >> 8)
        tmp |= vertical_watch_board & (tmp >> 8)
        legal_board |= blank_board & (tmp >> 8)

        #右斜め上
        tmp = all_side_watch_board & (atk_board << 7)
        tmp |= all_side_watch_board & (tmp << 7)
        tmp |= all_side_watch_board & (tmp << 7)
        tmp |= all_side_watch_board & (tmp << 7)
        tmp |= all_side_watch_board & (tmp << 7)
        tmp |= all_side_watch_board & (tmp << 7)
        legal_board |= blank_board & (tmp << 7)

        #左斜め上
        tmp = all_side_watch_board & (atk_board << 9)
        tmp |= all_side_watch_board & (tmp << 9)
        tmp |= all_side_watch_board & (tmp << 9)
        tmp |= all_side_watch_board & (tmp << 9)
        tmp |= all_side_watch_board & (tmp << 9)
        tmp |= all_side_watch_board & (tmp << 9)
        legal_board |= blank_board & (tmp << 9)

        #右斜め下
        tmp = all_side_watch_board & (atk_board >> 9)
        tmp |= all_side_watch_board & (tmp >> 9)
        tmp |= all_side_watch_board & (tmp >> 9)
        tmp |= all_side_watch_board & (tmp >> 9)
        tmp |= all_side_watch_board & (tmp >> 9)
        tmp |= all_side_watch_board & (tmp >> 9)
        legal_board |= blank_board & (tmp >> 9)

        #左斜め下
        tmp = all_side_watch_board & (atk_board >> 7)
        tmp |= all_side_watch_board & (tmp >> 7)
        tmp |= all_side_watch_board & (tmp >> 7)
        tmp |= all_side_watch_board & (tmp >> 7)
        tmp |= all_side_watch_board & (tmp >> 7)
        tmp |= all_side_watch_board & (tmp >> 7)
        legal_board |= blank_board & (tmp >> 7)

        self._puttable_map = legal_board


    def is_puttable(self, x, y):
       if self._puttable_map >> (x + 8*y) & 0b1 == 1:
           return True
       else:
           return False

    def get_puttable_map(self):
        return self._puttable_map


    def get_puttable_list(self):
        """
        石を置ける場所のリストをゲット
        """
        self._puttable_list = []
        for i in range(self._board_size):
            for j in range(self._board_size):
                if self.is_puttable(i, j):
                    self._puttable_list.append(np.array([i,j]))

        return self._puttable_list


    def transfer(self, put, way):
        if way == 0: #上
            return (put << 8) & 0xffffffffffffff00
        elif way == 1: #右上
            return (put << 7) & 0x7f7f7f7f7f7f7f00
        elif way == 2: #右
            return (put >> 1) & 0x7f7f7f7f7f7f7f7f
        elif way == 3: #右下
            return (put >> 9) & 0x007f7f7f7f7f7f7f
        elif way == 4: #下
            return (put >> 8) & 0x00ffffffffffffff
        elif way == 5: #左下
            return (put >> 7) & 0x00fefefefefefefe
        elif way == 6: #左
            return (put << 1) & 0xfefefefefefefefe
        elif way == 7: #左上
            return (put << 9) & 0xfefefefefefefe00
        else:
            return 0


    def is_in_puttable_list(self, x, y):
        if self._puttable_map >> (x + 8*y) & 0b1 != 0:
            return True
        else:
            return False


    def is_no_puttable(self):
        if self._puttable_map == 0:
            return True
        else:
            return False


    def count_stone(self, bow):
        if bow == 1:
            nbit = (self._bl_board & 0x5555555555555555) + (( self._bl_board >> 1 ) & 0x5555555555555555)
            nbit = (nbit & 0x3333333333333333) + (( nbit >> 2 ) & 0x3333333333333333)
            nbit = (nbit & 0x0f0f0f0f0f0f0f0f) + (( nbit >> 4 ) & 0x0f0f0f0f0f0f0f0f)
            nbit = (nbit & 0x00ff00ff00ff00ff) + (( nbit >> 8 ) & 0x00ff00ff00ff00ff)
            nbit = (nbit & 0x0000ffff0000ffff) + (nbit >> 16 & 0x0000ffff0000ffff)
            return (nbit & 0x00000000ffffffff) + (nbit >> 32)
        elif bow == 2:
            nbit = (self._wh_board & 0x5555555555555555) + (( self._wh_board >> 1 ) & 0x5555555555555555)
            nbit = (nbit & 0x3333333333333333) + (( nbit >> 2 ) & 0x3333333333333333)
            nbit = (nbit & 0x0f0f0f0f0f0f0f0f) + (( nbit >> 4 ) & 0x0f0f0f0f0f0f0f0f)
            nbit = (nbit & 0x00ff00ff00ff00ff) + (( nbit >> 8 ) & 0x00ff00ff00ff00ff)
            nbit = (nbit & 0x0000ffff0000ffff) + (( nbit >> 16 ) & 0x0000ffff0000ffff)
            return (nbit & 0x00000000ffffffff) + (nbit >> 32)



    def change_liberty(self, x, y, pm):
        # reduce liberty
        x += 1
        y += 1
        self._liberty[x][y-1] += pm
        self._liberty[x-1][y-1] += pm
        self._liberty[x-1][y] += pm
        self._liberty[x-1][y+1] += pm
        self._liberty[x][y+1] += pm
        self._liberty[x+1][y+1] += pm
        self._liberty[x+1][y] += pm
        self._liberty[x+1][y-1] += pm


    def put_stone(self, x, y, bow):
        #着手した場合のボードを生成
        atk_board = self.get_board_half(bow)
        opp_board = self.get_board_half(self.get_opponent(bow))
        opp = self.get_opponent(bow)

        rev = 0
        put = 0b1 << ( x + 8*y )
        for way in range(self._board_size):
            tmp_rev = 0
            mask = self.transfer(put, way)

            while (mask != 0) and ((mask & opp_board) != 0):
                tmp_rev |= mask
                mask = self.transfer(mask, way)

            if (mask & atk_board) != 0 :
                rev |= tmp_rev

        #反転する
        atk_board ^= put | rev
        opp_board ^= rev

        #reduce liberty
        self.change_liberty(x, y, -1)

        # reflect
        self.set_board(atk_board, bow)
        self.set_board(opp_board, opp)
        self.append_board_history(atk_board, bow)
        self.append_board_history(opp_board, opp)
        self.append_input_history(x,y)


    def get_liberty(self, x, y):
        x += 1
        y += 1
        return self._liberty[x][y]


    def create_board(self):
        board = Board()

        for x in range(self._board_size):
          for y in range(self._board_size):
            if self.get_stone(x, y, 1) == 1:
              board.set_stone(x, y, 1)
            elif self.get_stone(x, y, 2) == 1:
              board.set_stone(x, y, 2)
            if self.is_puttable(x, y):
                board.append_puttable(x, y)

        return board
