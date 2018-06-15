import copy
import random

from user.base_user import BaseUser
from ai.search_better import Search


class AiUser(BaseUser):

    def input_coord(self, **kwargs):
        """
        ユーザにインプットさせる．
        """
        board = kwargs['board']
        atk = kwargs['bow']
        opp = board.get_opponent(atk)
        game = kwargs['game']
        tmp_board = copy.deepcopy(board)
        search = Search(board, atk, opp, game.get_turn())
        evaluation, x, y = search.search()
        game.game_process(None, int(x), int(y), atk)

class RandomUser(BaseUser):
    def input_coord(self, **kwargs):
        """
        ユーザにインプットさせる．
        """
        board = kwargs['board']
        atk = kwargs['bow']
        opp = board.get_opponent(atk)
        game = kwargs['game']
        tmp_board = copy.deepcopy(board)
        board.listing_puttable(atk)
        legales = board.get_puttable_list()
        random_coord_index = random.randint(0, len(legales)-1)
        random_coord = legales[random_coord_index]
        game.game_process(None, int(random_coord[0]), int(random_coord[1]), atk)
