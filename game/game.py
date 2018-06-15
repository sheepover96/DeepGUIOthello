from board.board import Board
from user.user import User
from board.gui_board import GuiBoard
import numpy as np
import eval_test

class Game():
    """
    in this class, game process is written
    オセロゲームの処理を書いています．
    先攻ユーザと後攻ユーザ，ボードのオブジェクトを与えて動かす．
    bowはblack or whiteの略です
    """

    def __init__(self):
        #preceding attack user 先攻ユーザ
        self.__user1 = None
        #after attack user 後攻ユーザ
        self.__user2 = None
        #board 石をおくボードオブジェクト
        self.__board = None
        #GUI ボード
        self.__gui_board = None
        #turn 何ターン目かを格納
        self.__turn = 0
        #input coord 今まで石を置いた座標を格納
        self.__input_list = []
        #now attacker 現在の攻撃ユーザ　先攻１，後攻２
        self.__attacker = 1
        #game keeper flag ゲームの終了判定をするフラッグ
        self.__flag = False

    def get_attacker(self):
        return self.__attacker

    def set_gui_board(self, board):
        self.__gui_board = board

    def set_user(self, user, user_id):
        """
        ユーザを設定するメソッド．
        userにUserオブジェクト，user_idに先攻１か後攻２かを入れる
        """
        if user_id == 1:
            self.__user1 = user
        elif user_id == 2:
            self.__user2 = user
        else:
            print("only user1 or user2 can be assigned")

    def append_input(self, coord, bow):
        """
        ユーザの入力した座標を，Userオブジェクトに追加する（戻る用）
        """
        if bow == 1:
            self.__user1.append_input(coord)
        if bow == 2:
            self.__user2.append_input(coord)

    def set_board(self, board):
        """
        Boardオブジェクトのセッター
        """
        self.__board = board
        print(self.__board)

    def set_nstone(self, nstone, bow):
        """
        ユーザオブジェクトに，獲得している石の個数をセットする
        """
        if bow == 1:
            self.__user1.set_nstone(nstone)
        elif bow == 2:
            self.__user2.set_nstone(nstone)

    def print_nstone(self):
        """
        黒石と白石の数を表示
        """
        nstone1 = self.__user1.get_nstone()
        nstone2 = self.__user1.get_nstone()
        print("Black: {}\nWhite: {}".format(nstone1, nstone2))

    def input_coord(self):
        """
        ユーザに座標を入力させる．GUIでの実装をする予定
        """
        while True:

            print('input coorddinate x')
            coordx = int( input('coord x:') )

            print('input coorddinate x')
            coordy = int(input('coord y:'))

            coord = np.array([coordx, coordy])
            print(coord)

            #置ける場所かどうか判定．置けるなら履歴に追加する
            if self.__board.is_in_puttable_list(coordx, coordy):
                self.__input_list.append( coord )
                break
            else:
                print("unable to put stone there")
                continue

    def put_stone(self, x, y, bow):
        #石をおく
        self.__board.put_stone(x, y, bow)

    def start_game(self, board):
        """
        ゲームの流れが書いてあるメソッド
        """
        evaluate = eval_test.MidEvaluator(board, 1)
        while True:
            #置ける場所を探す
            self.__board.listing_puttable(self.__attacker)
            #ボードを表示
            self.__board.display_board()
            #GUIボードを表示
            #self.__gui_board.display_board()

            print("player {}'s attack".format(self.__attacker))

            #ゲームの終了判定
            #置ける場所がないとフラグがたつ
            if self.__board.is_no_puttable():
                if flag:
                    print("game finished!")
                    break;
                else:
                    flag = True
                    print("nowhere to put stone")
                    self.__turn += 1
                    self.__attacker = self.__turn % 2 + 1
                    continue
            else:
                flag = False

            #ユーザに入力させる
            self.input_coord()

            #入力座標の履歴の最後尾を取り出し，そこに石をおく．
            self.put_stone(int(self.__input_list[-1][0]), int(self.__input_list[-1][1]), self.__attacker)

            print(evaluate.evaluate(board, self.__attacker, 1))

            #石の数を数えてユーザにセット
            self.set_nstone(self.__board.count_stone(self.__attacker), self.__attacker)

            #ターンを増やし，攻撃を変更
            self.__turn += 1
            self.__attacker = self.__turn % 2 + 1

    def end_game(self):
        """
        ゲーム終了時の処理．勝敗と石の数を表示．
        """

        if nstone1 > nstone2:
            print("Black Win!")
        elif nstone1 < nstone2:
            print("White Win!")
        else:
            print("DRAW!")
