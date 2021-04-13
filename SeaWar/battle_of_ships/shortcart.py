"""
helper
"""
from models import User
from random import choice


def choice_ready_user(user_id):

    user = User.objects.get(pk=user_id)
    list_ready = []
    all_user_in_game = User.objects.filter(game=user.game)
    for player in all_user_in_game:
        if player.status != 1:
            return False
        list_ready.append(player.id)
    user_first_move_id = choice(list_ready)
    """
    Получили id игрока который ходит первым, удаляем его из листа и записываем в редис  
    через POP со статусом 1, другого игрока со статусом 0
    """
    return True

