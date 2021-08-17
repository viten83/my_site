from .models import Game, GameMove
from random import randint


class Cell:
    def __init__(self, row, column, value=0):
        self.row = row
        self.column = column
        self.value = value


class GameField:

    def __init__(self, game):
        self.field_size = game.field_size
        # number of symbols to win
        self.win_count = 3
        self.game_id = game.pk
        self.winner = None
        self.symbol_computer = game.symbol_computer
        self.symbol_player = game.symbol_player
        self.cells = []

        self.__create_field()

    def __create_field(self):
        for row in range(0, self.field_size):
            self.cells.append([])
            for column in range(0, self.field_size):
                self.cells[row].append(0)

        game_moves = GameMove.objects.filter(game=self.game_id)
        for game_move in game_moves:
            self.cells[game_move.row][game_move.column] = game_move.value

    def check_tie(self):
        for row in range(0, self.field_size):
            for column in range(0, self.field_size):
                if self.cells[row][column] == 0:
                    return False
        return True

    def check_win(self):
        if self.__check_win_columns():
            return True
        elif self.__check_win_rows():
            return True
        return False

    def __check_win_rows(self):
        for row in range(0, self.field_size):
            if self.__check_win_row(row=row):
                return True
            elif self.__check_diagonal(row=row):
                return True
        return False

    def __check_win_row(self, row):
        for column in range(0, self.field_size-self.win_count+1):
            if self.cells[row][column] != 0:
                value = self.cells[row][column]
                l_sum = value
                for index in range(column+1, column+self.win_count):
                    if value == self.cells[row][index]:
                        l_sum += value
                    else:
                        break
                if l_sum == self.symbol_player*self.win_count:
                    self.winner = Game.Winners.PLAYER
                    return True
                elif l_sum == self.symbol_computer*self.win_count:
                    self.winner = Game.Winners.COMPUTER
                    return True
        return False

    def __check_win_columns(self):
        for column in range(0, self.field_size):
            if self.__check_win_column(column):
                return True
        return False

    def __check_win_column(self, column):
        for row in range(0, self.field_size-self.win_count+1):
            if self.cells[row][column] != 0:
                value = self.cells[row][column]
                l_sum = value
                for index in range(row+1, row+self.win_count):
                    if value == self.cells[index][column]:
                        l_sum += value
                    else:
                        break
                    if l_sum == self.symbol_player * self.win_count:
                        self.winner = Game.Winners.PLAYER
                        return True
                    elif l_sum == self.symbol_computer * self.win_count:
                        self.winner = Game.Winners.COMPUTER
                        return True
        return False

    def __check_diagonal_down(self, row):

        """
        [
            [0,0,0,0]
            [1,0,0,0]
            [0,1,0,0]
            [0,0,1,0]
        ]
        if win_count == 3:
            winner_moves = [ {"row": 1, "column": 0}, {"row": 2, "column": 1,}, {"row": 3, "column": 2}]
        """
        l_row = row
        l_column_left = 0
        l_column_right = self.field_size - 1

        while l_row <= self.field_size-self.win_count:
            if self.cells[l_row][l_column_left] != 0:
                l_sum = self.cells[l_row][l_column_left]
                for index in range(1, self.win_count):
                    if self.cells[l_row + index][l_column_left + index] == self.cells[l_row][l_column_left]:
                        l_sum += self.cells[l_row][l_column_left]
                    else:
                        break
                if l_sum == self.symbol_player * self.win_count:
                    self.winner = Game.Winners.PLAYER
                    return True
                elif l_sum == self.symbol_computer * self.win_count:
                    self.winner = Game.Winners.COMPUTER
                    return True

            if self.cells[l_row][l_column_right] != 0:
                l_sum = self.cells[l_row][l_column_right]
                for index in range(1, self.win_count):
                    if self.cells[l_row + index][l_column_right - index] == self.cells[l_row][l_column_right]:
                        l_sum += self.cells[l_row][l_column_right]
                    else:
                        break
                if l_sum == self.symbol_player * self.win_count:
                    self.winner = Game.Winners.PLAYER
                    return True
                elif l_sum == self.symbol_computer * self.win_count:
                    self.winner = Game.Winners.COMPUTER
                    return True

            l_row += 1
            l_column_left += 1
            l_column_right -= 1

        return False

    def __check_diagonal_up(self, row):
        """
               [
                   [0,1,0,1]
                   [0,0,1,0]
                   [0,0,0,1]
                   [,0,1,0]
               ]
            if win_count == 3:
            winner_moves = [ {"row": 0, "column": 1}, {"row": 1, "column": 2,}, {"row": 2, "column": 3}]
        """
        l_row = row
        l_column_left = 0
        l_column_right = self.field_size - 1

        while l_row >= self.win_count-1:
            if self.cells[l_row][l_column_left] != 0:
                l_sum = self.cells[l_row][l_column_left]
                for index in range(1, self.win_count):
                    if self.cells[l_row - index][l_column_left + index] == self.cells[l_row][l_column_left]:
                        l_sum += self.cells[l_row][l_column_left]
                    else:
                        break
                if l_sum == self.symbol_player * self.win_count:
                    self.winner = Game.Winners.PLAYER
                    return True
                elif l_sum == self.symbol_computer * self.win_count:
                    self.winner = Game.Winners.COMPUTER
                    return True

            if self.cells[l_row][l_column_right] != 0:
                l_sum = self.cells[l_row][l_column_right]
                for index in range(1, self.win_count):
                    if self.cells[l_row - index][l_column_right - index] == self.cells[l_row][l_column_right]:
                        l_sum += self.cells[l_row][l_column_right]
                    else:
                        break
                if l_sum == self.symbol_player * self.win_count:
                    self.winner = Game.Winners.PLAYER
                    return True
                elif l_sum == self.symbol_computer * self.win_count:
                    self.winner = Game.Winners.COMPUTER
                    return True

            l_row -= 1
            l_column_left += 1
            l_column_right -= 1


    def __check_diagonal(self, row):
        if row <= self.field_size - self.win_count:
            return self.__check_diagonal_down(row)
        elif row >= self.win_count - 1:
            return self.__check_diagonal_up(row)
        return False

    def generate_first_move(self):
        list_moves = [
            Cell(row=0, column=0),
            Cell(row=0, column=self.field_size-1),
            Cell(row=self.field_size-1, column=0),
            Cell(row=self.field_size-1, column=self.field_size-1)
        ]

        return list_moves[randint(0, len(list_moves)-1)]

    def generate_move(self):
        return self.__generate_move_simple()

    def __generate_move_simple(self):
        empty_cells = self.__get_empty_cells()
        return empty_cells[randint(0, len(empty_cells)-1)]

    def __get_empty_cells(self):
        empty_cells = []
        for row in range(0, self.field_size):
            for column in range(0, self.field_size):
                if self.cells[row][column] == 0:
                    empty_cells.append(Cell(row=row, column=column))

        return empty_cells

    def __generate_move_hard(self):
        """
        I'll finish the method in the evening
        """
        return self.__generate_move_simple()
