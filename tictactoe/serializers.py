from rest_framework import serializers
from .models import Game, GameMove
import random


class GameListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Game
        fields = '__all__'


class GameMoveCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    game_move_owner = serializers.HiddenField(default=1)

    class Meta:
        model = GameMove
        fields = '__all__'


class GameMoveDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GameMove
        fields = '__all__'


class GameMoveListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)

    class Meta:
        model = GameMove
        fields = '__all__'


class GameCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    result_game = serializers.HiddenField(default=4)
    end_date_time = serializers.HiddenField(default=None)

    class Meta:
        model = Game
        fields = '__all__'


class GameDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Game
        fields = '__all__'






