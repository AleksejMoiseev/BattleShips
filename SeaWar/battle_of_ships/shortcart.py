"""
helper
"""
from random import choice
import redis as redis_client
from battle_of_ships.models import User
from rest_framework import exceptions

redis = redis_client.Redis(host='localhost', port=6379, db=0)


class Ship:
    def __init__(self, coordinates, hit_coordinates):
        self.coordinates = coordinates
        self.hit_coordinates = hit_coordinates


class DoesNotUser(Exception):
    pass


def get_users(user_id):
    user = User.objects.get(pk=user_id)
    game = user.game
    all_user_in_game = User.objects.filter(game=game)
    return game, all_user_in_game


def next_move(user_id):
    game, list_users = get_users(user_id=user_id)
    redis_key = 'current_' + str(game.id)
    id_last_move = redis.get(name=redis_key)
    for player in list_users:
        if player.id != int(id_last_move):
            redis.set(name=redis_key, value=player.id)
            return player.id, game


def choice_ready_user(user_id):
    list_ready = []
    # user = u.objects.get(pk=user_id)
    # game = user.game
    # all_user_in_game = u.objects.filter(game=user.game)
    game, all_user_in_game = get_users(user_id=user_id)
    for player in all_user_in_game:
        print("player.status", player.status)
        if player.status != 1:
            return False
        list_ready.append(player.id)
    id_who_move = choice(list_ready)
    redis_key = 'current_' + str(game.id)
    print(redis_key)
    redis.set(redis_key, id_who_move)
    print(redis.get(name=redis_key))
    return True


def get_enemy(user_id):
    print("get_enemy", user_id)
    game, all_user_in_game = get_users(user_id=user_id)
    for enemy in all_user_in_game:
        print("сравнение enemy.id, user_id", int(enemy.id), int(user_id))
        if int(enemy.id) != int(user_id):
            print(enemy.id != user_id)
            print('game, enemy', game, enemy )
            return game, enemy


def get_enemy_ships(user_id):
    game, enemy = get_enemy(user_id=user_id)
    ships_json = enemy.ship
    return game, ships_json


def save_enemy_ship(ships_json, user_id):
    game, enemy = get_enemy(user_id=user_id)
    enemy.ship = ships_json


def _check_hit(ship, coordinate):
    if not (coordinate in ship.coordinates):
        return 'mimo'
    if not (coordinate in ship.hit_coordinates):
        ship.hit_coordinates.append(coordinate)
    if len(ship.coordinates) == len(ship.hit_coordinates):
        return "killed"
    return "ranen"

"""
Не дописана
"""
def check_hit(list_json_objects):
    harborArr = []
    for json_object in list_json_objects:
        ship = Ship(coordinates=json_object['coordinates'], hit_coordinates=json_object['hit_coordinates'])
        harborArr.append(ship)




