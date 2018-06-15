from user.base_user import BaseUser

class User(BaseUser):

    def input_coord(self, **kwargs):
        """
        ユーザにインプットさせる．
        """
        atk = kwargs['bow']
        game = kwargs['game']
        game.enable_gui_board(atk)

