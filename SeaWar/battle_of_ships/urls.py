from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.urls import path
from battle_of_ships.views import *

urlpatterns = [
    path('', myfunc, name='myfunc'),
    path('game/', GameCreateView.as_view()),
    path('user/', UserCreateView.as_view()),
    path('getfunc/<uuid:id>/', GameDetailView.as_view()),
    path('retrive/<uuid:id>/', GameRetriveView.as_view()),
    path('destroy/<int:pk>/', UserDestroy.as_view()),
    path('createuser/', CreateUserAndGame.as_view()),
    path('update_user/<int:pk>/', UpdateShip.as_view()),
    path('faire/', faire, name="faire"),
    path('get_current_move/', get_current_move, name="get_current_move"),
]
