from django.db import models
from accounts.models import User


class Game(models.Model):

    class States(models.IntegerChoices):
        PROGRESS = 1, 'Progress game'
        GAME_OVER = 2, 'Game over'

        @staticmethod
        def to_dict():
            return {"PROGRESS": 1, "GAME_OVER": 2}

    class Winners(models.IntegerChoices):
        PLAYER = -1, 'Player'
        COMPUTER = 1, 'Computer'
        TIE = 0, 'Tie'

        @staticmethod
        def to_dict():
            return {"PLAYER": -1, "COMPUTER": 1, "TIE": 0}

    class Symbols(models.TextChoices):
        VALUE_X = 'X'
        VALUE_O = 'O'

        @staticmethod
        def to_list():
            return ['X', 'O']

    class Levels(models.IntegerChoices):
        EASY = 1, 'Easy'
        MEDIUM = 2, 'Medium'
        HARD = 3, 'Hard'

        @staticmethod
        def to_dict():
            return {"EASY": 1, "MEDIUM": 2, "HARD": 3}

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Player")
    start_date_time = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date of start game")
    end_date_time = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, verbose_name="Date of end game")
    board_size = models.IntegerField(default=3, verbose_name="Playing field size")
    state = models.IntegerField(choices=States.choices, default=1, verbose_name="Game stats")
    winner = models.IntegerField(choices=Winners.choices, null=True, verbose_name="Winner game")
    symbol_player = models.CharField(choices=Symbols.choices, max_length=1, verbose_name="Player symbol")
    symbol_computer = models.CharField(choices=Symbols.choices, max_length=1, verbose_name="Computer symbol")
    level = models.IntegerField(choices=Levels.choices, verbose_name="Game level")

    def __str__(self):
        return " -- field size:" + str(self.board_size) + " -- start date:" + str(self.start_date_time)

    def update_symbol_computer(self):
        if self.symbol_player == Game.Symbols.VALUE_O:
            self.symbol_computer = Game.Symbols.VALUE_X
        else:
            self.symbol_computer = Game.Symbols.VALUE_O

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"
        ordering = ('start_date_time', )


class GameMove(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="When the move is made")
    column = models.IntegerField(verbose_name="Number column")
    row = models.IntegerField(verbose_name="Number row")
    value = models.IntegerField(choices=Game.Symbols.choices, verbose_name="Cell value")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Game", related_name="game_moves")

    def __str__(self):
        return str(self.date_time)+"("+str(self.number_column)+"X"+str(self.number_row)+")"

    class Meta:
        verbose_name = "Game move"
        verbose_name_plural = "Game moves"
        ordering = ('date_time', )




# Create your models here.
