from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    STATS_GAME = (
        (1, "Окончена, игрок выиграл"),
        (2, "Окончена, игрок проиграл"),
        (3, "Окончена, ничья"),
        (4, "Идет игра")
    )

    GAME_SYMBOLS = (
        (1, "O"),
        (2, "X")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Игрок")
    start_date_time = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Время начала игры")
    end_date_time = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Время завершения игры")
    field_size = models.IntegerField(default=3, verbose_name="Размер игрового поля")
    result_game = models.IntegerField(default=4, choices=STATS_GAME, verbose_name="Статус игры")
    symbol_gamer = models.IntegerField(choices=GAME_SYMBOLS, verbose_name="Символ, которым играет игрок")

    def __str__(self):
        return str(self.field_size)

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"


class GameMove(models.Model):
    GAME_MOVE_OWNERS = (
        (1, "Игрок"),
        (2, "Компьютер")
    )

    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Игра")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Игрок")
    game_move_owner = models.IntegerField(choices=GAME_MOVE_OWNERS, verbose_name="Кто сделал ход")
    date_time = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Когда сделан ход")
    number_column = models.IntegerField(verbose_name="Номер столбца")
    number_row = models.IntegerField(verbose_name="Номер строки")

    def __str__(self):
        return str(self.date_time)+"("+str(self.number_column)+"X"+str(self.number_row)+")"

    class Meta:
        verbose_name = "Ход"
        verbose_name_plural = "Ходы"




# Create your models here.
