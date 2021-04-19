from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import ListView
from rest_framework.decorators import api_view


from battle_of_ships.forms import CreateUserForm
from battle_of_ships.serializers import *
from battle_of_ships.models import User
from battle_of_ships.models import Game
from rest_framework.permissions import AllowAny
from django.views.generic import CreateView
from rest_framework.authtoken.models import Token


from rest_framework import authentication
from rest_framework import exceptions

from django.conf import settings

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.renderers import JSONRenderer

from battle_of_ships.shortcart import (
    redis, get_users, next_move, choice_ready_user,
    get_enemy, DoesNotUser, get_enemy_ships, get_array_ships,
    check_hit, ships_to_json, save_enemy_ship,
    check_winner,
)

CURRENT_USER_KEY_PREFIX = 'current:{}'
SET_CONTAINS_SHOTS_USER_KEY_PREFIX = 'set'


class GameView(generics.RetrieveAPIView):
    serializer_class = ListGame
    queryset = User.objects.all()


class GameCreateView(generics.ListCreateAPIView):
    serializer_class = GameDetailSerializers
    queryset = Game.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(generics.ListCreateAPIView):
    serializer_class = UserListSerializers
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        # self.authenticate(request)
        print(request.user)
        print(request.session)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        id_user = serializer.data['id']
        headers['id'] = id_user
        response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        response.set_cookie(key='id', value=id_user)
        return response


class GameRetriveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GameDetailSerializers
    queryset = Game.objects.all()
    lookup_field = 'id'
    permission_classes = (AllowAny, )

"""
Еще одна реализация через написания логики в самом классе через наследования базового класса APIView,  и 
самостоятельному определению метода get
"""


class GameDetailView(APIView):

    def get(self, request, id):
        game = Game.objects.get(id=id)  # выбираем из базы данных   query данные с id=id
        serializer = GameDetailSerializers(game)  # устанавливаем сериализатор
        return Response(serializer.data)  # Возвращаем Responce c данными


class UserDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = UserListSerializers
    queryset = u.objects.all()




# class CreateUserAndGame(CreateView):
#     form_class = CreateUserForm
#     template_name = "my_server/fronted/auth.html"
#     context_object_name = 'name_user'
#
#


@method_decorator(csrf_exempt, name='dispatch')
class CreateUserAndGame(generics.CreateAPIView):
    serializer_class = CreateStartGame
    queryset = Game.objects.all()

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        id_game = serializer.data['id']
        game = Game.objects.get(id=id_game)
        created_user = User.objects.create(name=name, game=game)
        headers = self.get_success_headers(serializer.data)
        headers['id'] = created_user.pk
        response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        response.set_cookie(key='id', value=created_user.pk)
        return response


class UpdateShip(generics.RetrieveUpdateAPIView):
    serializer_class = UserShipStatusUpdate
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        print('request', request.COOKIES)
        print("request cookies", request.COOKIES.get('id'))
        user_id = request.COOKIES.get('id')
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        print(choice_ready_user(user_id=user_id))
        return Response(serializer.data)


@csrf_exempt
def faire(request):
    user_id = request.COOKIES.get('id')
    coordinate = request.POST['coordinate']
    response = HttpResponse()

    game, list_of_ships_enemy = get_enemy_ships(user_id=user_id)
    harbor_arr_ships_enemy = get_array_ships(list_json_objects=list_of_ships_enemy)
    print(harbor_arr_ships_enemy)
    hit_result = check_hit(harbor=harbor_arr_ships_enemy, coordinate=coordinate)
    print('hit_result', hit_result)
    harbor_arr_ready_save_to_database = ships_to_json(arrships_objects=harbor_arr_ships_enemy)
    save_enemy_ship(ships_json=harbor_arr_ready_save_to_database, user_id=user_id)
    print("check_winner(arr_ships=harbor_arr_ships_enemy)", check_winner(arr_ships=harbor_arr_ships_enemy))
    if check_winner(arr_ships=harbor_arr_ships_enemy):
        user = User.objects.get(pk=user_id)
        user_name = user.name
        user.game.status = Game.Status.FINISHED
        user.game.winner = user_name
        user.game.save()
        print("СТАТУС ИГРЫ - Зашли в победу", game.status)
        data = {"coordinate": coordinate, "hit_result": "win", "winner": user_name}
        content = JSONRenderer().render(data=data)
        print("content", content)
        response.content = content
        return response
    if hit_result == 'mimo':
        next_move_user, game = next_move(user_id=user_id)
        print('следующий ход делает user:', next_move_user)
        redis_key = 'current_' + str(game.id)
        print('value redis', redis.get(name=redis_key))

    redis_key_set_shots = SET_CONTAINS_SHOTS_USER_KEY_PREFIX + str(game.id) + str(user_id)
    # print("redis_key_set_shots", redis_key_set_shots)

    redis.sadd(redis_key_set_shots, coordinate)
    data = {"coordinate": coordinate, "hit_result": hit_result}
    content = JSONRenderer().render(data=data)

    print(content)
    response.content = content
    return response


@api_view(['GET'])
def get_current_move(request):
    user_id = request.COOKIES.get('id')
    user = User.objects.get(pk=user_id)
    game = user.game
    status = game.status
    winner = user.game.winner
    response = HttpResponse()
    if status == 0:
        print('Мы здесь')
        data = {"current_move": "null", "status": status, "winner": winner}
        content = JSONRenderer().render(data=data)
        response.content = content
        return response

    redis_key = 'current_' + str(game.id)
    print(redis_key)
    current_move = redis.get(name=redis_key)

    data = {"current_move": current_move, "status": status, "winner": winner}
    content = JSONRenderer().render(data=data)
    response.content = content

    # response.content = current_move
    print("current_move", current_move)
    return response


@api_view(['GET'])
def get_shots_enemy(request):
    try:
        user_id = request.COOKIES.get('id')
        print('user_id request', user_id)
        if user_id == None:
            raise DoesNotUser
    except DoesNotUser:
        print(" i here")
        return HttpResponse("<h1>Нет USERA</h1>")
    game, user_enemy = get_enemy(user_id=user_id)
    redis_key_get_shots = SET_CONTAINS_SHOTS_USER_KEY_PREFIX + str(game.id) + str(user_enemy.id)
    print(" redis_key_get_shots", redis_key_get_shots)
    set_shots_enemy = redis.smembers(redis_key_get_shots)
    # set_shots_enemy = redis.smembers(name='myset2')
    set_shots_enemy_in_json = JSONRenderer().render(data=set_shots_enemy)
    print("set_shots_enemy_in_json", set_shots_enemy_in_json)
    print("set_shots_enemy", set_shots_enemy)
    return HttpResponse(content=set_shots_enemy_in_json)













