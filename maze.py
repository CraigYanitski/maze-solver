import random
import statistics as stat
import time

from graphics import Point, Line


class Cell:
    def __init__(self, window=None):
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.win = window
        self.visited = False

    def draw(self, x1, y1, x2, y2, color="black", offcolor="#d9d9d9", width=2):
        if self.win is None:
            return
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)

        # Bottom Wall
        if self.has_bottom_wall:
            line: Line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
            self.win.draw_line(line, color=color, width=width)
        else:
            line: Line = Line(Point(self.x1+width/2, self.y2), Point(self.x2-width/2, self.y2))
            self.win.draw_line(line, color=offcolor, width=width)
        
        # Top Wall
        if self.has_top_wall:
            line: Line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
            self.win.draw_line(line, color=color, width=width)
        else:
            line: Line = Line(Point(self.x1+width/2, self.y1), Point(self.x2-width/2, self.y1))
            self.win.draw_line(line, color=offcolor, width=width)
        
        # Left Wall
        if self.has_left_wall:
            line: Line = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
            self.win.draw_line(line, color=color, width=width)
        else:
            line: Line = Line(Point(self.x1, self.y1+width/2), Point(self.x1, self.y2-width/2))
            self.win.draw_line(line, color=offcolor, width=width)
        
        # Right Wall
        if self.has_right_wall:
            line: Line = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
            self.win.draw_line(line, color=color, width=width)
        else:
            line: Line = Line(Point(self.x2, self.y1+width/2), Point(self.x2, self.y2-width/2))
            self.win.draw_line(line, color=offcolor, width=width)

    def to_cell(self, cell, undo=False, width=2):
        if self.win is None:
            return
        x1, y1 = stat.mean((self.x1, self.x2)), stat.mean((self.y1, self.y2))
        x2, y2 = stat.mean((cell.x1, cell.x2)), stat.mean((cell.y1, cell.y2))
        line: Line = Line(Point(x1, y1), Point(x2, y2))
        if undo:
            color = "gray"
        else:
            color = "red"
        self.win.draw_line(line, color=color, width=width)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, width=2, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._cells = []
        self._win = win
        self.width = 8#width
        self.seed = seed
        if not seed is None:
            random.seed(seed)
        self._create_cells()

    def _create_cells(self):
        for i in range(self._num_cols):
            col = []
            for j in range(self._num_rows):
                cell = Cell(self._win)
                col.append(cell)
            self._cells.append(col)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1, y1 = self._x1 + i * self._cell_size_x, self._y1 + j * self._cell_size_y
        x2, y2 = x1 + self._cell_size_x, y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2, width=self.width)
        self._animate(0.0001)

    def _animate(self, dt=0.01):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(dt)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        i = len(self._cells) - 1
        j = len(self._cells[0]) - 1
        self._cells[i][j].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(i, j)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            possible = []
            for nx, ny in neighbours:
                if 0 <= i+nx < self._num_cols and 0 <= j+ny < self._num_rows:
                    if self._cells[i+nx][j+ny].visited:
                        continue
                    else:
                        possible.append((nx, ny))
            if len(possible):
                d = random.choice(possible)
            else:
                self._draw_cell(i, j)
                return
            if d == (-1, 0):
                self._cells[i][j].has_left_wall = False
            elif d == (1, 0):
                self._cells[i][j].has_right_wall = False
            elif d == (0, -1):
                self._cells[i][j].has_top_wall = False
            elif d == (0, 1):
                self._cells[i][j].has_bottom_wall = False
            else:
                raise Exception("Index Error: invalid direction...")
            self._break_walls_r(i + d[0], j + d[1])
        self._reset_cells_visited()

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, x, y, path_width=4):
        self._animate(0.001)
        cell = self._cells[x][y]
        cell.visited = True
        if (x, y) == (self._num_cols-1, self._num_rows-1):
            return True
        for nx, ny in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            if 0 <= x+nx < self._num_cols and 0 <= y+ny < self._num_rows:
                next_cell = self._cells[x+nx][y+ny]
                move = False
                if self._cells[x+nx][y+ny].visited:
                    continue
                elif (not cell.has_top_wall) and (ny < 0) and (y > 0):
                    move = True
                elif (not cell.has_bottom_wall) and (ny > 0) and (y < (self._num_rows-1)):
                    move = True
                elif (not cell.has_left_wall) and (nx < 0) and (x > 0):
                    move = True
                elif (not cell.has_right_wall) and (nx > 0) and (x < (self._num_cols-1)):
                    move = True
                if move:
                    cell.to_cell(next_cell, undo=False, width=path_width)
                    if self._solve_r(x+nx, y+ny):
                        return True
                    else:
                        cell.to_cell(next_cell, undo=True, width=path_width)
                        self._animate(0.01)
        return False

