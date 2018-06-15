
class BaseUser():

    def __init__(self, bow):
        #if bow == 1, preceding, if 2 after
        self._bow = bow
        #num of stone
        self._nstone = 0
        #history
        self._input_history = []

    def set_nstone(self, nstone):
        """
        石の数をセット
        """
        self._nstone = nstone

    def append_history(self, coord):
        """
        ユーザが石を置いた座標の履歴
        """
        self._input_history.append(coord)

    def pop_history(self):
        """
        ユーザが石を置いた座標の履歴
        """
        self._input_history.pop()

    def display_bow(self):
        """
        ユーザが先攻か後攻か表示
        """
        if self._bow == 1:
            print("black: preceding attack")
        elif self._bow == 2:
            print("white: after attack")
        else:
            print("i don't know")

    def get_nstone(self):
        """
        ユーザのとった石の数を表示
        """
        return (self._nstone)

    def input_coord(self, **kwargs):
        """
        ユーザにインプットさせる．
        ここをオーバーライドしてください
        """
        pass

