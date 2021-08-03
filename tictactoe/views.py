from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import Game, GameMove
from .permissions import IsOwnerOrReadOnly


class GameCreateView(generics.CreateAPIView):
    serializer_class = GameCreateSerializer


class GameListView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameListSerializer
    permission_classes = (IsAuthenticated, )


class GameDetailView(generics.RetrieveAPIView):
    serializer_class = GameDetailSerializer
    queryset = Game.objects.all()
    permission_classes = (IsOwnerOrReadOnly, )


class GameMoveDetailView(generics.RetrieveAPIView):
    serializer_class = GameMoveDetailSerializer
    queryset = GameMove.objects.all()
    permission_classes = (IsOwnerOrReadOnly, )


class GameMoveListView(generics.ListAPIView):
    serializer_class = GameMoveListSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def get_queryset(self):
        game_id = self.kwargs['game_id']
        return GameMove.objects.filter(game=game_id)


class GameMoveCreateView(generics.CreateAPIView):
    serializer_class = GameMoveCreateSerializer




# Create your views here.
