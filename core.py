class NotYourTurnError(RuntimeError):
    pass


class CellOccupiedError(RuntimeError):
    pass


class TheGame:
    def __init__(self, field_size, row_len):

        if field_size < 3:
            raise ValueError('Field size must be greater than 2')

        if row_len > field_size:
            raise ValueError('Row length cannot be greater than field size')

        if row_len < 3:
            raise ValueError('Row length cannot be less than 3')

        self.field_size = field_size
        self.row_len = row_len
        self.field = [[None] * field_size for i in range(field_size)]
        self.crosses_turn = True
        self.cells_left = self.field_size ** 2

    def make_a_move(self, crosses, x, y):
        if self.crosses_turn is None:
            raise RuntimeError('Game is over')

        if self.crosses_turn != crosses:
            raise NotYourTurnError('FUCK YOU')

        if not (1 <= x <= self.field_size) or not (1 <= y <= self.field_size):
            raise ValueError('Out of bounds')

        i = y - 1
        j = x - 1

        if self.field[i][j] is not None:
            raise CellOccupiedError('FUCK YOU ONE MORE TIME')

        self.field[i][j] = crosses
        self.cells_left -= 1
        self.crosses_turn = not self.crosses_turn

        directions = [
            ((0, -1), (0, 1)),
            ((-1, 0), (1, 0)),
            ((-1, -1), (1, 1)),
            ((-1, 1), (1, -1))
        ]

        won = False
        for d in directions:
            s = 1
            for di, dj in d:
                _i = i + di
                _j = j + dj
                while 0 <= _i < self.field_size and 0 <= _j < self.field_size:
                    if self.field[_i][_j] == crosses:
                        s += 1
                        if s >= self.row_len:
                            break
                    else:
                        break
                    _i += di
                    _j += dj
                if s >= self.row_len:
                    won = True
                    break
            else:
                continue
            break

        if won:
            self.crosses_turn = None
            return crosses

    def is_over(self):
        return self.crosses_turn is None or self.cells_left == 0

    def crosses_move(self, x, y):
        return self.make_a_move(True, x, y)

    def noughts_move(self, x, y):
        return self.make_a_move(False, x, y)

    def get_field(self):
        return self.field