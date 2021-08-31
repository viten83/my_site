from .models import Game, GameMove
from random import randint
from copy import deepcopy
import sys


class Cell:
    def __init__(self, row=-1, column=-1, value=0):
        self.row = row
        self.column = column
        self.value = value

    def __str__(self):
        return "<Cell row:"+str(self.row)+" column:"+str(self.column)+" value:"+str(self.value)+">"


class Move:
    def __init__(self, cell=Cell(), score=0):
        self.cell = cell
        self.score = score

    def __str__(self):
        return "<Move score:"+self.score+" "+str(self.cell)


class GameBoard:

    def __init__(self, game):
        self.board_size = game.board_size
        # number of symbols to win
        self.win_count = 3
        self.game_id = game.pk
        self.winner = None
        self.depth = game.level*2
        self.board = []

        self.__create_field()

    def __create_field(self):
        self.board.clear()
        for row in range(0, self.board_size):
            self.board.append([])
            for column in range(0, self.board_size):
                self.board[row].append(0)

        game_moves = GameMove.objects.filter(game=self.game_id)
        for game_move in game_moves:
            self.board[game_move.row][game_move.column] = game_move.value

    def check_tie(self):
        if len(self.__get_available_cells()) == 0:
            return True
        return False

    def check_win(self):
        return self.__check_win_board(self.board, self.win_count)

    def make_move(self, player=Game.Winners.COMPUTER):
        best_moves = []

        board = deepcopy(self.board)

        if player == Game.Winners.COMPUTER:
            best_score = -sys.maxsize
            for row in range(0, len(board)):
                for column in range(0, len(board)):
                    if board[row][column] == 0:
                        alpha = -sys.maxsize
                        beta = sys.maxsize

                        board[row][column] = Game.Winners.COMPUTER
                        score = self.__minimax(board=board,
                                               depth=self.depth,
                                               is_max=False,
                                               alpha=alpha,
                                               beta=beta)
                        if score > best_score:
                            best_score = score
                            best_moves.clear()
                            best_moves.append(Move(Cell(row=row, column=column), score=score))
                        elif score == best_score:
                            best_moves.append(Move(Cell(row=row, column=column), score=score))

                        board[row][column] = 0
            best_move = best_moves[randint(0, len(best_moves) - 1)]

        else:
            best_score = sys.maxsize
            for row in range(0, len(board)):
                for column in range(0, len(board)):
                    if board[row][column] == 0:
                        alpha = -sys.maxsize
                        beta = sys.maxsize

                        board[row][column] = Game.Winners.PLAYER
                        score = self.__minimax(board=board,
                                               depth=self.depth,
                                               is_max=True,
                                               alpha=alpha,
                                               beta=beta)

                        if score < best_score:
                            best_score = score
                            best_moves.clear()
                            best_moves.append(Move(Cell(row=row, column=column), score=score))
                        elif score == best_score:
                            best_moves.appen(Move(Cell(row=row, column=column), score=score))

                        board[row][column] = 0
            best_move = best_moves[randint(0, len(best_moves) - 1)]
        self.board[best_move.cell.row][best_move.cell.column] = player
        return best_move

    def __minimax(self, board, depth, alpha, beta, is_max):
        win = GameBoard.__check_win_board(board, self.win_count)
        if win or depth == 0:
            return depth * win
        available_moves = GameBoard.__get_available_cells_from_board(board)
        if len(available_moves) == 0:
            return 0

        new_board = deepcopy(board)

        if not is_max:
            best_score = sys.maxsize
            for row in range(0, len(new_board)):
                for column in range(0, len(new_board)):
                    if new_board[row][column] == 0:
                        new_board[row][column] = -1
                        score = self.__minimax(new_board,  depth - 1, alpha, beta, not is_max)
                        if score < best_score:
                            best_score = score
                        new_board[row][column] = 0
                        beta = min(beta, score)
                        if beta < alpha:
                            break
                if beta < alpha:
                    break

        else:
            best_score = -sys.maxsize
            for row in range(0, len(new_board)):
                for column in range(0, len(new_board)):
                    if new_board[row][column] == 0:
                        new_board[row][column] = 1
                        score = self.__minimax(new_board,  depth - 1, alpha, beta, not is_max)
                        if score > best_score:
                            best_score = score
                        new_board[row][column] = 0
                        alpha = max(alpha, score)
                        if beta < alpha:
                            break
                if beta < alpha:
                    break
        return best_score

    def __get_available_cells(self):
        available_cells = []
        for row in range(0, self.board_size):
            for column in range(0, self.board_size):
                if self.board[row][column] == 0:
                    available_cells.append(Cell(row=row, column=column))

        return available_cells

    @staticmethod
    def __get_available_cells_from_board(board):
        available_cells = []
        for row in range(0, len(board)):
            for column in range(0, len(board)):
                if board[row][column] == 0:
                    available_cells.append(Cell(row=row, column=column))
        return available_cells

    @staticmethod
    def __check_win_board(board, win_count):
        for row in range(0, len(board)):
            for column in range(0, len(board)):
                if board[row][column] != 0:
                    if row <= len(board) - win_count:
                        sum_row = 0
                        sum_diagonal_to_right = 0
                        sum_diagonal_to_left = 0

                        sum_column = GameBoard.__calculate_column_down(board=board,
                                                                       win_count=win_count,
                                                                       row=row,
                                                                       column=column)
                        if column <= len(board) - win_count:
                            sum_row = GameBoard.__calculate_row_right(board=board,
                                                                      win_count=win_count,
                                                                      row=row,
                                                                      column=column)
                            sum_diagonal_to_right = GameBoard.__calculate_diagonal_to_right_down(board=board,
                                                                                             win_count=win_count,
                                                                                             row=row,
                                                                                             column=column)
                        if column >= win_count - 1:
                            sum_diagonal_to_left = GameBoard.__calculate_diagonal_to_left_down(board=board,
                                                                                           win_count=win_count,
                                                                                           row=row,
                                                                                           column=column)

                        max_value = GameBoard.__get_max(sum_row,
                                                        sum_diagonal_to_left,
                                                        sum_diagonal_to_right,
                                                        sum_column)

                        if max_value == -win_count:
                            return -1
                        elif max_value == win_count:
                            return 1

                    if row > len(board) - win_count:
                        if column <= len(board) - win_count:
                            sum_row = GameBoard.__calculate_row_right(board=board,
                                                                      win_count=win_count,
                                                                      row=row,
                                                                      column=column)
                            if sum_row == -win_count:
                                return -1
                            elif sum_row == win_count:
                                return 1
        return 0

    @staticmethod
    def __get_max(*args):
        max_move = args[0]
        for index in range(1, len(args)):
            if abs(max_move) < abs(args[index]):
                max_move = args[index]

        return max_move

    @staticmethod
    def __calculate_column_down(board, win_count, row, column):
        s_move = board[row][column]
        for index in range(1, win_count):
            s_move += board[row + index][column]
        return s_move

    @staticmethod
    def __calculate_column_up(board, win_count, row, column):
        s_move = board[row][column]
        for index in range(1, win_count):
            s_move += board[row - index][column]
        return s_move

    @staticmethod
    def __calculate_row_right(board, win_count, row, column):
        s_move = board[row][column]
        for index in range(1, win_count):
            s_move += board[row][column + index]
        return s_move

    @staticmethod
    def __calculate_row_left(board, win_count, row, column):
        s_move = board[row][column]
        for index in range(1, win_count):
            s_move += board[row][column - index]
        return s_move

    @staticmethod
    def __calculate_diagonal_to_right_down(board, win_count, row, column):
        s_move = board[row][column]
        for index in range(1, win_count):
            s_move += board[row + index][column + index]
        return s_move

    @staticmethod
    def __calculate_diagonal_to_right_up(board, win_count, row, column):
        s_move = board[row][column]
        for index in range(1, win_count):
            s_move += board[row - index][column + index]
        return s_move

    @staticmethod
    def __calculate_diagonal_to_left_down(board, win_count, row, column):
        s_move = board[row][column]
        for index in range(1, win_count):
            s_move += board[row + index][column - index]
        return s_move

    @staticmethod
    def __calculate_diagonal_to_left_up(board, win_count, row, column):
        s_move = board[row][column]
        for index in range(1, win_count):
            s_move += board[row - index][column - index]
        return s_move

