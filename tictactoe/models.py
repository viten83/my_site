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
        PLAYER = 1, 'Player'
        COMPUTER = 2, 'Computer'
        TIE = 3, 'Tie'

        @staticmethod
        def to_dict():
            return {"PLAYER": 1, "COMPUTER": 2, "TIE": 3}

    class Symbols(models.IntegerChoices):
        VALUE_X = 1, 'X'
        VALUE_O = -1, 'O'

        @staticmethod
        def to_dict():
            return {"X": 1, "O": -1}

    class Levels(models.IntegerChoices):
        EASY = 1, 'Easy'
        HARD = 2, 'Hard'

        @staticmethod
        def to_dict():
            return {"EASY": 1, "HARD": 2}

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Player")
    start_date_time = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date of start game")
    end_date_time = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, verbose_name="Date of end game")
    field_size = models.IntegerField(default=3, verbose_name="Playing field size")
    state = models.IntegerField(choices=States.choices, default=1, verbose_name="Game stats")
    winner = models.IntegerField(choices=Winners.choices, null=True, verbose_name="Winner game")
    symbol_player = models.IntegerField(choices=Symbols.choices, verbose_name="Player symbol")
    symbol_computer = models.IntegerField(choices=Symbols.choices, verbose_name="Computer symbol")
    level = models.IntegerField(choices=Levels.choices, verbose_name="Game level")

    def __str__(self):
        return " -- field size:" + str(self.field_size) + " -- start date:" + str(self.start_date_time)

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
