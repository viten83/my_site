from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import Game, GameMove
from .game_field import GameField
from datetime import datetime
from django.db import models


class GameWinnerListView(APIView):

    """get list winners game"""

    def get(self, request, forman=None):
        return Response(Game.Winners.to_dict())


class GameStateListView(APIView):
    """ get list stats game"""

    def get(self, request, format=None):
        return Response(Game.States.to_dict())


class GameSymbolListView(APIView):
    """ get list symbols game"""

    def get(self, request, format=None):
        return Response(Game.Symbols.to_dict())


class GameLevelListView(APIView):
    """ get list levels game"""

    def get(self, request, format=None):
        return Response(Game.Levels.to_dict())


class GameListView(APIView):
    """
        get method - return all games
        post method - create new game
        create Game:
        {
            "field_size": int_value>=3,
            "symbol_player": Game.Symbols.value,
            "level": Game.Levels.value
        }

    """

    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        return Response(GameListModelSerializer(Game.objects.all(), many=True).data)

    def post(self, request, format=None):

        serializer = GameListModelSerializer(data=request.data)

        if serializer.is_valid():
            game = serializer.save()
            game.user = request.user
            game.save()
            return Response(GameListModelSerializer(game).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameDetailView(APIView):

    """
        get method - return game detail
        path method - game over, player lost
        delete method - delete game
    """

    permission_classes = (IsAuthenticated, )

    def get(self, request, pk, format=None):

        try:
            game = Game.objects.get(pk=pk)
        except models.ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(GameDetailModelSerializer(game).data)

    def patch(self, request, pk, format=None):

        try:
            game = Game.objects.get(pk=pk)
        except models.ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if game.state == Game.States.GAME_OVER:
            return Response({"Error:": "The game is over."}, status=status.HTTP_400_BAD_REQUEST)

        game.state = Game.States.GAME_OVER
        game.winner = Game.Winners.COMPUTER
        game.end_date_time = datetime.now()
        game.save()

        return Response(GameListModelSerializer(game).data)

    def delete(self, request, pk, format=None):
        try:
            game = Game.objects.get(pk=pk)
        except models.ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GameMoveListView(APIView):
    """
        post - create game move
        {
            "game": Game.pk,
            "row": 0>=row<Game.field_size,
            "column": 0>=column<Game.field_size
        }
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        serializer = GameMoveListModelSerializer(data=request.data)

        if serializer.is_valid():
            game_move = serializer.save()
            if GameMove.objects.filter(game=game_move.game, column=game_move.column, row=game_move.row).exists():
                return Response({"Error:": "This cell is already taken."}, status.HTTP_400_BAD_REQUEST)
            if game_move.game.state == Game.States.GAME_OVER:
                return Response({"Error:": "The game is over."}, status=status.HTTP_400_BAD_REQUEST)
            game_move.value = game_move.game.symbol_player
            game_move.save()

            game_field = GameField(game=game_move.game)
            if game_field.check_win():
                game_move.game.winner = game_field.winner
                game_move.game.end_date_time = datetime.now()
                game_move.game.state = Game.States.GAME_OVER
                game_move.game.save()
            if game_field.check_tie():
                game_move.game.winner = Game.Winners.TIE
                game_move.game.end_date_time = datetime.now()
                game_move.game.state = Game.States.GAME_OVER
                game_move.game.save()

            return Response(GameMoveDetailModelSerializer(game_move).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameNextMoveView(APIView):
    """
        get - get computer game move
    """

    def get(self, request, pk, format=None):

        try:
            game = Game.objects.get(pk=pk)
            if game.state == Game.States.GAME_OVER:
                return Response({"Error": "The game is over."}, status=status.HTTP_400_BAD_REQUEST)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        game_move = GameMove()
        game_move.value = game.symbol_computer
        game_move.game = game

        game_field = GameField(game=game)
        cell = game_field.generate_move()

        game_move.column = cell.column
        game_move.row = cell.row
        game_move.save()

        if game_field.check_win():
            game.winner = game_field.winner
            game.end_date_time = datetime.now()
            game.state_game = Game.States.GAME_OVER
            game.save()
        elif game_field.check_tie():
            game.winner = Game.Winners.TIE
            game.end_date_time = datetime.now()
            game.state = Game.States.GAME_OVER
            game.save()

        return Response(GameMoveDetailModelSerializer(game_move).data)


class GameCheckWin(APIView):

    def get(self, request, pk, format=None):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if game.state == Game.States.GAME_OVER:
            return Response(GameListModelSerializer(game).data)

        game_field = GameField(game=game)

        if game_field.check_win():
            game.winner = game_field.winner
            game.end_date_time = datetime.now()
            game.state = Game.States.GAME_OVER
            game.save()
        if game_field.check_tie():
            game.winner = Game.Winners.TIE
            game.end_date_time = datetime.now()
            game.state = Game.States.GAME_OVER
            game.save()

        return Response(GameDetailModelSerializer(game).data)






