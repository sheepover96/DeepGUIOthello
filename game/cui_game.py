from board.board import Board
from user.user import User
from game.base_game import BaseGame
import numpy as np

class CuiGame(BaseGame):
    """
    GameのCUI実装
    """

    def __init__(self):
        super(CuiGame, self).__init__()

    def start_game(self):
        """
        ゲームの流れが書いてあるメソッド
        """
        while True:
            #置ける場所を探す
            self._board.listing_puttable(self._attacker)
            #ボードを表示
            self._board.display_board()

            print("player {}'s attack".format(self._attacker))

            #ゲームの終了判定
            #置ける場所がないとフラグがたつ
            if self._board.is_no_puttable():
                if flag:
                    print("game finished!")
                    break
                else:
                    flag = True
                    print("nowhere to put stone")
                    self.next_turn()
                    continue
            else:
                flag = False

            #ユーザに入力させる
            self.input_coord(self._attacker)

            #入力座標の履歴の最後尾を取り出し，そこに石をおく．
            self.put_stone(int(self._input_list[-1][0]), int(self._input_list[-1][1]), self._attacker)

            #石の数を数えてユーザにセット
            self.set_nstone()

            #ターンを増やし，攻撃を変更
            self.next_turn()

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
