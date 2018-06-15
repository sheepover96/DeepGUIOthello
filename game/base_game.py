from board.board import Board
from user.user import User
import numpy as np

class BaseGame():
    """
    in this class, game process is written
    オセロゲームの処理を書いています．
    先攻ユーザと後攻ユーザ，ボードのオブジェクトを与えて動かす．
    bowはblack or whiteの略です
    """

    def __init__(self):
        #preceding attack user 先攻ユーザ
        self._user1 = None
        #after attack user 後攻ユーザ
        self._user2 = None
        #board 石をおくボードオブジェクト
        self._board = None
        #turn 何ターン目かを格納
        self._turn = 0
        #input coord 今まで石を置いた座標を格納
        self._input_history = []
        #input coord 今まで石を置いたユーザを格納
        self._input_user_history = []
        #now attacker 現在の攻撃ユーザ　先攻１，後攻２
        self._attacker = 1
        #game keeper flag ゲームの終了判定をするフラッグ
        self._flag = False

    def get_turn(self):
        return self._turn

    def get_attacker(self):
        return self._attacker

    def get_input_history(self):
        return self._input_history

    def get_opponent(self, bow):
        """
        敵ユーザの番号を返す
        """
        return bow % 2 + 1


    def set_user(self, user, user_id):
        """
        ユーザを設定するメソッド．
        userにUserオブジェクト，user_idに先攻１か後攻２かを入れる
        """
        if user_id == 1:
            self._user1 = user
        elif user_id == 2:
            self._user2 = user
        else:
            print("only user1 or user2 can be assigned")


    def append_history(self, coord, bow):
        """
        ユーザの入力した座標を，Userオブジェクトに追加する
        """
        if bow == 1:
            self._user1.append_history(coord)
        elif bow == 2:
            self._user2.append_history(coord)

        self._input_history.append(coord)
        self._input_user_history.append(bow)


    def set_board(self, board):
        """
        Boardオブジェクトのセッター
        """
        self._board = board
        print(self._board)

    def set_nstone(self):
        """
        ユーザオブジェクトに，獲得している石の個数をセットする
        """
        self._user1.set_nstone(self._board.count_stone(1))
        self._user2.set_nstone(self._board.count_stone(2))

    def print_nstone(self):
        """
        黒石と白石の数を表示
        """
        nstone1 = self._user1.get_nstone()
        nstone2 = self._user1.get_nstone()
        print("Black: {}\nWhite: {}".format(nstone1, nstone2))

    def input_coord(self, atk):
        """
        ユーザに座標を入力させる．GUIでの実装をする予定
        """
        if atk == 1:
            self._user1.input_coord(bow=atk, board=self._board, game=self)
        elif atk == 2:
            self._user2.input_coord(bow=atk, board=self._board, game=self)

    def put_stone(self, x, y, bow):
        #石をおく
        self._board.put_stone(x, y, bow)

    def next_turn(self, is_pass):
        #ターンを増やし，攻撃を変更
        self._turn += 1
        if not is_pass:
            self._attacker = self._attacker % 2 + 1

    def start_game(self):
        """
        ゲームの流れが書いてあるメソッド
        """
        pass

    def end_game(self):
        """
        ゲーム終了時の処理．勝敗と石の数を表示．
        """
        pass
