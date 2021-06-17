"""
helper
"""
from random import choice

import redis as redis_client

from battle_of_ships.models import User

redis = redis_client.Redis(host='localhost', port=6379, db=0)


class Ship:
    def __init__(self, coordinates, hit_coordinates):
        self.coordinates = coordinates
        self.hit_coordinates = hit_coordinates

    def to_json(self):
        return {'coordinates': self.coordinates, 'hit_coordinates': self.hit_coordinates}

    def __str__(self):
        return f"'coordinates': {self.coordinates}, 'hit_coordinates': {self.hit_coordinates}"

    def check_hit(self, coordinate):
        if not (coordinate in self.coordinates):
            return 'mimo'
        if not (coordinate in self.hit_coordinates):
            self.hit_coordinates.append(coordinate)
        if len(self.coordinates) == len(self.hit_coordinates):
            return 'killed'
        return 'ranen'

    def killed(self):
        if len(self.coordinates) == len(self.hit_coordinates):
            return True
        return False


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
        if player.status != 1:
            return False
        list_ready.append(player.id)
    id_who_move = choice(list_ready)
    redis_key = 'current_' + str(game.id)
    redis.set(redis_key, id_who_move)
    return True


def get_enemy(user_id):
    game, all_user_in_game = get_users(user_id=user_id)
    for enemy in all_user_in_game:
        if int(enemy.id) != int(user_id):
            return game, enemy


def get_enemy_ships(user_id):
    game, enemy = get_enemy(user_id=user_id)
    ships_json = enemy.ship
    return game, ships_json


def save_enemy_ship(ships_json, user_id):
    game, enemy_user_id = get_enemy(user_id=user_id)
    enemy_user_id.ship = ships_json
    enemy_user_id.save()

1
def get_array_ships(list_json_objects):
    harborArr = []
    for json_object in list_json_objects:
        ship = Ship(coordinates=json_object['coordinates'], hit_coordinates=json_object['hit_coordinates'])
        harborArr.append(ship)
    return harborArr


def ships_to_json(arrships_objects):
    arr_to_json = []
    for ship in arrships_objects:
        arr_to_json.append(ship.to_json())
    return arr_to_json


def check_hit(harbor, coordinate):
    for ship in harbor:
        hit_result = ship.check_hit(coordinate=coordinate)
        if hit_result == "ranen":
            return "ranen"
        if hit_result == "killed":
            return "killed"
    return "mimo"


def check_winner(arr_ships):
    for ship in arr_ships:
        if not ship.killed():
            return False
    return True





