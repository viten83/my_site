from django.urls import path
from .views import *

app_name = "tictactoe"

urlpatterns = [
    path('games/', GameListView.as_view()),
    path('games/<int:pk>/', GameDetailView.as_view()),
    path('game_make_move/<int:pk>/', GameMakeMoveView.as_view()),
    path('game_moves/', GameMoveListView.as_view()),
    path('game_winners/', GameWinnerListView.as_view()),
    path('game_states/', GameStateListView.as_view()),
    path('game_levels/', GameLevelListView.as_view()),
]

