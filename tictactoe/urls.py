from django.urls import path, include
from .views import *

app_name = "tictactoe"

urlpatterns = [
    path('games/', GameListView.as_view()),
    path('games/<int:pk>/', GameDetailView.as_view()),
    path('games_next_move/<int:pk>/', GameNextMoveView.as_view()),
    path('games_check_win/<int:pk>/', GameCheckWin.as_view()),
    path('game_moves/', GameMoveListView.as_view()),
    path('game_winners/', GameWinnerListView.as_view()),
    path('game_states/', GameStateListView.as_view()),
    path('game_symbols/', GameSymbolListView.as_view()),
    path('game_levels/', GameLevelListView.as_view()),
]

