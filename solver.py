from collections import defaultdict

class Cell(object):
    remaining_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    final_value = None

    def __init__(self, row, column, board, initial_value=0):
        self.row = row
        self.column = column
        self.board = board

        if initial_value:
            self.final_value = initial_value
            self.remaining_values = set()

    def __repr__(self):
        if self.final_value:
            return str(self.final_value)
        else:
            return str(sorted(list(self.remaining_values)))

    def _cells_in_row(self):
        for cell in self.board[self.row]:
            yield cell

    def _cells_in_column(self):
        for row in self.board:
            yield row[self.column]

    def _cells_in_square(self):
        indices = ((0, 1, 2), (3, 4, 5), (6, 7, 8))
        row_indices = indices[self.row / 3]
        column_indices = indices[self.column / 3]

        for r in row_indices:
            for c in column_indices:
                yield self.board[r][c]

    def process(self):
        self._update_possibilities()
        self._check_loneliness()

    def _update_possibilities(self):
        if self.final_value:
            return

        external_final_values = set(
            [] # just for formatting, lol
        ).union(
            set([x.final_value for x in self._cells_in_row() if x.final_value])
        ).union(
            set([x.final_value for x in self._cells_in_column() if x.final_value])
        ).union(
            set([x.final_value for x in self._cells_in_square() if x.final_value])
        )

        self.remaining_values = self.remaining_values - external_final_values

        if len(self.remaining_values) == 1:
            self.final_value = self.remaining_values.pop()

    def _get_possibility_counts(self, cells):
        counter = defaultdict(int)
        for cell in cells:
            for value in cell.remaining_values:
                counter[value] += 1
        return counter

    def _check_loneliness(self):
        row_counts = self._get_possibility_counts(self._cells_in_row())
        column_counts = self._get_possibility_counts(self._cells_in_column())
        square_counts = self._get_possibility_counts(self._cells_in_square())

        for remaining_value in self.remaining_values:
            if (
                    (row_counts[remaining_value] == 1) or
                    (column_counts[remaining_value] == 1) or
                    (square_counts[remaining_value] == 1)
            ):
                self.final_value = remaining_value
                self.remaining_values = set()
                return

class Board(object):


    def __init__(self, board):
        self.basic_board = board
        # should probably do a proper init, innit?

        self.cell_board = []
        for row in xrange(9):
            self.cell_board.append([])
            for column in xrange(9):
                value = self.basic_board[row][column]
                cell = Cell(row, column, self.cell_board, value)
                self.cell_board[row].append(cell)

    def __repr__(self):
        line_format   = "{} {} {} | {} {} {} | {} {} {}"
        row_separator = "------+-------+------"
        number_display = lambda x: x.final_value if x.final_value else ' '
        lines = []

        lines.append(line_format.format(*map(number_display, self.cell_board[0][0]._cells_in_row())))
        lines.append(line_format.format(*map(number_display, self.cell_board[1][0]._cells_in_row())))
        lines.append(line_format.format(*map(number_display, self.cell_board[2][0]._cells_in_row())))
        lines.append(row_separator)
        lines.append(line_format.format(*map(number_display, self.cell_board[3][0]._cells_in_row())))
        lines.append(line_format.format(*map(number_display, self.cell_board[4][0]._cells_in_row())))
        lines.append(line_format.format(*map(number_display, self.cell_board[5][0]._cells_in_row())))
        lines.append(row_separator)
        lines.append(line_format.format(*map(number_display, self.cell_board[6][0]._cells_in_row())))
        lines.append(line_format.format(*map(number_display, self.cell_board[7][0]._cells_in_row())))
        lines.append(line_format.format(*map(number_display, self.cell_board[8][0]._cells_in_row())))
        return '\n'.join(lines)

    def cycle(self):
        for row in xrange(9):
            for column in xrange(9):
                cell = self.cell_board[row][column]
                cell.process()
        print self


test_board_1 = [
    [7, 5, 0, 0, 3, 8, 0, 0, 0],
    [0, 0, 0, 5, 0, 0, 9, 0, 0],
    [0, 9, 0, 0, 7, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 2, 1],
    [1, 3, 4, 0, 0, 0, 7, 5, 6],
    [2, 8, 7, 0, 0, 0, 0, 0, 0],
    [0, 0, 6, 0, 2, 0, 0, 3, 0],
    [0, 0, 5, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 4, 1, 0, 0, 9, 2],
]

test_board_2 = [
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 8, 0, 6, 0, 0, 0, 0],
    [7, 0, 5, 4, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 5, 0],
    [5, 8, 7, 0, 0, 0, 2, 0, 0],
    [4, 0, 0, 7, 0, 0, 9, 6, 0],
    [9, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 2, 6, 5, 0, 0, 4, 0, 0],
]

board = Board(test_board_2)
import ipdb; ipdb.set_trace()
print board
