from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import ListView
from rest_framework.decorators import api_view


from battle_of_ships.forms import CreateUserForm
from battle_of_ships.serializers import *
from battle_of_ships.models import User as u
from battle_of_ships.models import Game
from rest_framework.permissions import AllowAny
from django.views.generic import CreateView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User as auth


from rest_framework import authentication
from rest_framework import exceptions

from django.conf import settings

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator



class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None

        try:
            user = auth.objects.get(username=username)
            print(user)
        except auth.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)

# Create your views here.


def myfunc(request):
    return HttpResponse("<h1>Privet</h1>")


class GameCreateView(generics.ListCreateAPIView):
    serializer_class = GameDetailSerializers
    queryset = Game.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(generics.ListCreateAPIView):
    serializer_class = UserListSerializers
    queryset = u.objects.all()

    def create(self, request, *args, **kwargs):
        self.authenticate(request)
        print(request.user)
        print(request.session)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        id_user = serializer.data['id']
        # request.session['id'] = id_user
        # print(request.session)
        # print(request.session['id'])
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
        created_user = u.objects.create(name=name, game=game)
        headers = self.get_success_headers(serializer.data)
        headers['id'] = created_user.pk
        response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        response.set_cookie(key='id', value=created_user.pk)
        return response


class UpdateShip(generics.RetrieveUpdateAPIView):
    serializer_class = UserShipStatusUpdate
    queryset = u.objects.all()

    def put(self, request, *args, **kwargs):
        print('request', request.cookies)
        print("request cookies", request.cookies.get('id'))
        return self.partial_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # print('request', request.COOKIES)
        # print("request cookies", request.COOKIES.get('id'))
        # user_id = request.COOKIES.get('id')
        # print(choice_ready_user(user_id=user_id))
        return self.partial_update(request, *args, **kwargs)

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
    print(user_id)
    print(request.COOKIES)
    coordinate = request.POST['coordinate']
    print(coordinate)
    print(coordinate.encode())
    print(type(coordinate))
    response = HttpResponse()
    print("proba")
    response.content = coordinate.encode()
    next_move_user, game = next_move(user_id=user_id)
    print('следующий ход делает user:', next_move_user)
    redis_key = 'current_' + str(game.id)
    print('value redis', redis.get(name=redis_key))
    return response


@api_view(['GET'])
def get_current_move(request):
    user_id = request.COOKIES.get('id')
    game = u.objects.get(pk=user_id).game
    print(user_id)
    print(request.GET)
    response = HttpResponse()
    redis_key = 'current_' + str(game.id)
    current_move = redis.get(name=redis_key)
    response.content = current_move.encode()
    return response












