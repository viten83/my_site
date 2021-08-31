from rest_framework import serializers
from .models import Game, GameMove


class GameMoveListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMove
        fields = '__all__'
        read_only_fields = ['id', 'value']

    def create(self, validated_data):
        game_move = GameMove(**validated_data)
        game_move.value = game_move.game.symbol_player
        return game_move

    def validate(self, attrs):
        game = attrs['game']
        column = attrs['column']
        if column < 0 or column >= game.board_size:
            raise serializers.ValidationError("Column out of range.")
        row = attrs['row']
        if row < 0 or row >= game.board_size:
            raise serializers.ValidationError("Row out of range.")
        return attrs


class GameListModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    start_date_time = serializers.DateTimeField(read_only=True)
    end_date_time = serializers.DateTimeField(read_only=True)
    winner = serializers.IntegerField(read_only=True)
    state = serializers.IntegerField(read_only=True)
    board_size = serializers.IntegerField()
    symbol_player = serializers.CharField(max_length=1)
    symbol_computer = serializers.CharField(read_only=True, max_length=1)
    level = serializers.IntegerField()

    def create(self, validated_data):
        game = Game(**validated_data)
        game.update_symbol_computer()
        return game

    def validate(self, attrs):
        board_size = attrs['board_size']
        if board_size < 3:
            raise serializers.ValidationError("Field size out of range.")
        level = attrs['level']
        if level not in Game.Levels.to_dict().values():
            raise serializers.ValidationError("Level out of range.")
        symbol_player = attrs['symbol_player']
        if symbol_player not in Game.Symbols.to_list():
            raise serializers.ValidationError("Symbol player out of range.")
        return attrs

    class Meta:
        model = Game
        fields = [
            'id',
            'start_date_time',
            'end_date_time',
            'winner',
            'state',
            'board_size',
            'symbol_player',
            'symbol_computer',
            'level'
        ]


class GameMoveDetailModelSerializer(serializers.ModelSerializer):
    game = GameListModelSerializer()

    class Meta:
        model = GameMove
        fields = [
            'id',
            'row',
            'column',
            'value',
            'date_time',
            'game'
        ]


class GameDetailModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    start_date_time = serializers.DateTimeField(read_only=True)
    end_date_time = serializers.DateTimeField(read_only=True)
    winner = serializers.IntegerField(read_only=True)
    state = serializers.IntegerField(read_only=True)
    board_size = serializers.IntegerField()
    symbol_player = serializers.CharField(max_length=1)
    symbol_computer = serializers.CharField(read_only=True, max_length=1)
    level = serializers.IntegerField()

    game_moves = GameMoveListModelSerializer(many=True)

    class Meta:
        model = Game
        fields = [
            'id',
            'start_date_time',
            'end_date_time',
            'winner',
            'state',
            'board_size',
            'symbol_player',
            'symbol_computer',
            'level',
            "game_moves"
        ]


