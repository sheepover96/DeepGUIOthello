import numpy as np

class Board():

    #置けるか判定をするときに使うベクトル
    _vec = np.array([\
            [1,0],
            [1,-1],
            [1,1],
            [-1,0],
            [-1,1],
            [-1,-1],
            [0,1],
            [0,-1]
        ])

    parser = ","

    def __init__(self):
        #石の数
        self._nstone = 0
        #ボードのサイズ 変更できるようにする予定
        self._board_size = 8
        #石をおくボードを表す二次元numpy array
        self._board = np.zeros((self._board_size, self._board_size))
        #各ターンでのボードの形を保存する
        self._board_history = []
        #puttable list: points are contained
        #石を置ける場所が入っている
        self._puttable_list = []

    def get_opponent(self, bow):
        """
        敵ユーザの番号を返す
        """
        return bow % 2 + 1

    def append_puttable(self, x, y):
        self._puttable_list.append(np.array([x, y]))

    def get_board(self):
        """
        boardのgetter
        """
        return self._board

    def set_stone(self, x, y, bow):
        """
        指定されたcoordinateにbowの石を置く
        """
        if x < 8 and x >= 0 and y < 8 and y >= 0:
            self._board[x, y] = bow
        else:
            print("out of board size")

    def get_stone(self, x, y):
        """
        指定されたcoorddinateの石をみる
        """
        if x < 8 and x >= 0 and y < 8 and y >= 0:
            return self._board[x, y]
        else:
            return -1

    def get_board_size(self):
        """
        ボードのサイズをゲット
        """
        return self._board_size

    def init_board(self, file_path):
        """
        csvファイルを元に，ボードを初期化
        """
        with open(file_path) as f:
            for i, row in enumerate(f):
                col = row.split(self.parser)
                self._board[i,] = col

    def is_puttable(self, x, y, bow):
        """
        coorddinateにbowの石を置けるか判定
        """

        coord = np.array([x, y])

        if self.get_stone(x, y) != 0:
            return False

        opp = self.get_opponent(bow)

        for i in range(8):
            tmp_coord = coord.copy()
            tmp_coord += self._vec[i]
            tmp_x = tmp_coord[0]
            tmp_y = tmp_coord[1]

            if self.get_stone(tmp_x, tmp_y) in [0,-1,bow]:
                continue

            while True:
                tmp_coord += self._vec[i]

                if tmp_x > 7 or tmp_y < 0:
                    break

                if tmp_x > 7 or tmp_y < 0:
                    break

                if self.get_stone(tmp_x, tmp_y) == 0:
                    break

                if self.get_stone(tmp_x, tmp_y) == bow:
                    return True

        return False


    def listing_puttable(self, bow):
        """
        石を置ける場所を全てリストに入れる
        """
        self._puttable_list = []
        for i in range(self._board_size):
            for j in range(self._board_size):
                coord = np.array([i, j])
                if self.is_puttable(i, j, bow):
                    self._puttable_list.append(coord)

    def get_puttable_list(self):
        """
        石を置ける場所のリストをゲット
        """
        return self._puttable_list

    def is_in_puttable_list(self, x, y):
        """
        石を置けるか判定．こっちの方が速い．
        """
        coord = np.array([x, y])
        for puttable in self._puttable_list:
            if (coord==puttable).all():
                return True

        return False

    def is_no_puttable(self):
        if len(self._puttable_list) == 0:
            return True
        else:
            return False


    def put_stone(self, x, y, bow):
        """
        石を置く．
        """
        opp = self.get_opponent(bow)
        self._board_history.append(self._board.copy())
        self.set_stone(x, y, bow)
        coord = np.array([x, y])

        for i in range(8):
            tmp_coord = coord.copy()
            tmp_coord += self._vec[i]

            if self.get_stone(tmp_coord) in [0,-1,bow]:
                continue

            while True:
                tmp_coord += self._vec[i]

                if tmp_coord[0] > 7 or tmp_coord[0] < 0:
                    break

                if tmp_coord[1] > 7 or tmp_coord[1] < 0:
                    break

                if self.get_stone(tmp_coord) == bow:
                    while True:
                        tmp_coord -= self._vec[i]
                        if self.get_stone(tmp_coord) == bow:
                            break
                        self.set_stone(tmp_coord[0], tmp_coord[1],  bow)
                    break

    def count_stone(self, bow):
        """
        bowの石の数を数える
        """
        return np.count_nonzero(bow - self._board)


    def display_board(self):
        """
        boardを表示
        """
        tmp_board = self._board.copy()
        for puttable in self._puttable_list:
            tmp_board[puttable[0], puttable[1]] = -1

        print(" ", end="")
        for i in range(self._board_size):
            print(" {}".format(i), end="")
        print("")
        bar = "-"*18
        print(bar)
        for i in range(self._board_size):
            print("{}|".format(i), end="")
            for j in range(self._board_size):
                tstn = int(tmp_board[i,j])
                stone = " "
                if tstn == 1:
                    stone = "B"
                elif tstn == 2:
                    stone = "W"
                elif tstn == -1:
                    stone = "*"

                print("{}|".format(stone), end="")
            print("")

if __name__ == '__main__':
    b = Board()
    b.init_board("init.csv")

