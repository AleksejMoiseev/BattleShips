from rest_framework import serializers
from battle_of_ships.models import *


class GameDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'  # ввыводим все поля
        # exclude = ("date_start", )  # Выводим все кроме поля date_start


class UserListSerializers(serializers.ModelSerializer):
    # cat = serializers.SlugRelatedField(slug_field="name",read_only=True)  # Применяется для вывода связаного поля
    # Поле чтения-записи, представляющее цель отношения уникальным атрибутом slug
    class Meta:
        model = User
        fields = '__all__'


class CreateStartGame(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ("id",)


class UserShipStatusUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("ship", "status",)


class ListGame(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('game',)