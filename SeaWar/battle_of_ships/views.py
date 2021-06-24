import logging

from django.db import transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from SeaWar.settings import MAXIMUM_ALLOWED_NUMBER_OF_PLAYERS
from battle_of_ships.serializers import *
from battle_of_ships.shortcart import (
    redis, next_move, choice_ready_user,
    get_enemy, DoesNotUser, get_enemy_ships, get_array_ships,
    check_hit, ships_to_json, save_enemy_ship,
    check_winner,
)

logger = logging.getLogger('custom')

logger.setLevel(level=logging.DEBUG)

log_handlers = {
    "file_debug": logging.FileHandler('/home/alex/Documents/Projects/battleShips/env2/debug.log', mode="w"),
    "file_info": logging.FileHandler('/home/alex/Documents/Projects/battleShips/env2/debug.log', mode="w"),
}
log_handlers["file_debug"].setLevel(logging.DEBUG)
log_handlers["file_info"].setLevel(logging.INFO)

log_formatters = {
    "file_debug": logging.Formatter("[%(levelname)s]@[%(asctime)s]: %(message)s"),
    "file_info": logging.Formatter("[%(levelname)s]@[%(asctime)s]: %(message)s"),
}

for k, v in log_formatters.items():
    print(k, v)
    log_handlers[k].setFormatter(v)

logger.addHandler(log_handlers['file_debug'])
logger.addHandler(log_handlers["file_info"])


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
        logger.info(msg="Начало функции создание игры второго игрока create")
        data_request = request.data
        game_id = data_request['game']
        logger.debug(msg=f"value game={game_id}")

        users = User.objects.select_for_update().filter(game_id=game_id)
        with transaction.atomic():
            if len(users) >= MAXIMUM_ALLOWED_NUMBER_OF_PLAYERS:
                data_responce = JSONRenderer().render(data={"errors": "Потомушта нельзя больше двух игроковб вообщето"})
                return Response(status=status.HTTP_403_FORBIDDEN, data=data_responce)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        id_user = serializer.data['id']
        logger.debug(msg=f"value id_user = {id_user}")
        headers['id'] = id_user
        response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        response.set_cookie(key='id', value=id_user)
        logger.info(msg="cookies set")
        logger.info(msg=f"Окончание создания второго игрока")
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
    queryset = User.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class CreateUserAndGame(generics.CreateAPIView):
    serializer_class = CreateStartGame
    queryset = Game.objects.all()

    def create(self, request, *args, **kwargs):
        logger.info(msg=f"Создание первого игрока")
        name = request.data['name']
        logger.debug(msg=f'value name user = {name}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        id_game = serializer.data['id']
        logger.debug(msg=f'value id_game = {id_game}')
        game = Game.objects.get(id=id_game)
        logger.debug(msg=f'value game = {game}')
        created_user = User.objects.create(name=name, game=game)
        logger.debug(msg=f'value created_user = {name}')
        headers = self.get_success_headers(serializer.data)
        logger.debug(msg=f'value name user = {name}')
        headers['id'] = created_user.pk
        logger.debug(msg=f'value name user = {name}')
        response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        response.set_cookie(key='id', value=created_user.pk)
        logger.info(f'Конец создания первого игрока')
        return response


@method_decorator(csrf_exempt, name='dispatch')
class UpdateShip(generics.RetrieveUpdateAPIView):
    serializer_class = UserShipStatusUpdate
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        logger.info('Пытаемся изменить корабли')
        user_id = request.COOKIES.get('id')
        logger.debug(msg=f'value user_id = {user_id}')
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        is_ready = choice_ready_user(user_id=user_id)
        logger.debug(msg=f'состояние готовности {is_ready}')
        if not is_ready:
            logger.info('Один из игроков не готов, возвращаем st=204')
            return Response(status=204)
        logger.info('Все готовы, возвращаем st=200')
        return Response(serializer.data, status=200)


@csrf_exempt
def faire(request):
    user_id = request.COOKIES.get('id')
    coordinate = request.POST['coordinate']
    response = HttpResponse()

    game, list_of_ships_enemy = get_enemy_ships(user_id=user_id)
    harbor_arr_ships_enemy = get_array_ships(list_json_objects=list_of_ships_enemy)
    hit_result = check_hit(harbor=harbor_arr_ships_enemy, coordinate=coordinate)
    harbor_arr_ready_save_to_database = ships_to_json(arrships_objects=harbor_arr_ships_enemy)
    save_enemy_ship(ships_json=harbor_arr_ready_save_to_database, user_id=user_id)
    if check_winner(arr_ships=harbor_arr_ships_enemy):
        user = User.objects.get(pk=user_id)
        user_name = user.name
        user.game.status = Game.Status.FINISHED
        user.game.winner = user_name
        user.game.save()
        data = {"coordinate": coordinate, "hit_result": "win", "winner": user_name}
        content = JSONRenderer().render(data=data)
        response.content = content
        return response
    if hit_result == 'mimo':
        next_move_user, game = next_move(user_id=user_id)
        redis_key = 'current_' + str(game.id)

    redis_key_set_shots = SET_CONTAINS_SHOTS_USER_KEY_PREFIX + str(game.id) + str(user_id)

    redis.sadd(redis_key_set_shots, coordinate)
    data = {"coordinate": coordinate, "hit_result": hit_result}
    logger.debug(msg=f"Результат выстрела : {data}")
    content = JSONRenderer().render(data=data)

    response.content = content
    return response


@csrf_exempt
@api_view(['GET'])
def get_current_move(request):
    user_id = request.COOKIES.get('id')
    user = User.objects.get(pk=user_id)
    game = user.game
    status = game.status
    winner = user.game.winner
    response = HttpResponse()
    if status == 0:
        data = {"current_move": "null", "status": status, "winner": winner}
        content = JSONRenderer().render(data=data)
        response.content = content
        return response

    redis_key = 'current_' + str(game.id)
    current_move = redis.get(name=redis_key)

    data = {"current_move": current_move, "status": status, "winner": winner}
    logger.debug(msg=f'следующий игрок : {data}')
    content = JSONRenderer().render(data=data)
    response.content = content

    return response

@csrf_exempt
@api_view(['GET'])
def get_shots_enemy(request):
    try:
        user_id = request.COOKIES.get('id')
        if user_id == None:
            raise DoesNotUser
    except DoesNotUser:
        return HttpResponse("<h1>Нет USERA</h1>")

    game, user_enemy = get_enemy(user_id=user_id)
    if not user_enemy:
        logger.debug(msg=f"user_enemy - {user_enemy}")
        return HttpResponse(status=204)
    redis_key_get_shots = SET_CONTAINS_SHOTS_USER_KEY_PREFIX + str(game.id) + str(user_enemy.id)
    set_shots_enemy = redis.smembers(redis_key_get_shots)
    set_shots_enemy_in_json = JSONRenderer().render(data=set_shots_enemy)
    return HttpResponse(content=set_shots_enemy_in_json)













