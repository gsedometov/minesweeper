import io
import random
from itertools import chain, product


class Board:
    def __init__(self, rows, columns, mines):
        self.total_mines = mines
        self.revealed_count = 0
        self.free_cells_count = rows*columns - mines
        self.rows = rows
        self.columns = columns
        self.cells = [[0 for _ in range(columns)] for _ in range(rows)]
        self.revealed = [[False for _ in range(columns)] for _ in range(rows)]
        all_coords = list(product(range(rows), range(columns)))
        mines_coords = random.sample(list(all_coords), mines)
        for x, y in mines_coords:
            self[x, y] = -1

        for x, y in all_coords:
            if (x, y) not in mines_coords:
                self[x, y] = self.mines_around(x, y)

    def __getitem__(self, item):
        x, y = item
        return self.cells[y][x]

    def __setitem__(self, key, value):
        x, y = key
        self.cells[y][x] = value

    def get_neib(self, x, y):
        return [row[max(x-1, 0):x+2] for row in self.cells[max(y-1, 0):y+2]]

    def mines_around(self, x, y):
        neighborhood = self.get_neib(x, y)
        return len([c for c in chain(*neighborhood) if c == -1])

    def get_neib_coords(self, x, y):
        return [(xn, yn) for xn, yn in product((x-1, x, x+1), (y-1, y, y+1)) if
                not (xn == x and yn == y)
                and xn in range(self.columns)
                and yn in range(self.rows)]

    def reveal(self, x, y):
        if self[x, y] == -1:
            return 'Game over'
        queue = [(x, y)]
        while queue:
            cell_x, cell_y = queue.pop()
            if self.revealed[cell_y][cell_x]:
                continue
            self.revealed[cell_y][cell_x] = True
            self.revealed_count += 1
            if self[cell_x, cell_y] == 0:
                neib_coords = self.get_neib_coords(cell_x, cell_y)
                queue.extend(neib_coords)

        if self.free_cells_count == self.revealed_count:
            return 'You win'
        return 'Success'

    def render(self):
        result = io.StringIO()
        for (cells_row, reveal_row) in zip(self.cells, self.revealed):
            result.write(' '.join([str(c) if r else 'X' for (c, r) in zip(cells_row, reveal_row)]))
            result.write('\n')
        print(result.getvalue())