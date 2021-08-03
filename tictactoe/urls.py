from django.urls import path, include

from .views import *

app_name = "tictactoe"

urlpatterns = [
    path("games/", GameListView.as_view()),
    path("game/create/", GameCreateView.as_view()),
    path('game/detail/<int:pk>/', GameDetailView.as_view()),
    path('game_move/create', GameMoveCreateView.as_view()),
    path('game_move/detail/<int:pk>/', GameMoveDetailView.as_view()),
    path('game_moves/<int:game_id>', GameMoveListView.as_view()),
]

