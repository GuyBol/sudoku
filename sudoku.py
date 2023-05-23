#!/usr/bin/env python3

import random

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "(%d,%d)" % (self.x, self.y)

class Grid:
    def __init__(self):
        self.set_initial_grid()
        self.grid = [[self.initial_grid[x][y] for y in range(9)] for x in range(9)]
    
    def set_initial_grid(self):
        # Set randomly the first line of the grid
        # It will allow to generate 9! grids
        self.initial_grid = [[0 for y in range(9)] for x in range(9)]
        first_line = [x for x in range(1,10)]
        random.shuffle(first_line)
        for x in range(9):
            self.initial_grid[x][0] = first_line[x]
    
    def get(self, pos):
        return self.grid[pos.x][pos.y]

    def set(self, pos, value):
        self.grid[pos.x][pos.y] = value

    def next_pos(self, pos):
        new_pos = Position(0,0)
        if pos.x < 8:
            new_pos = Position(pos.x+1, pos.y)
        elif pos.y < 8:
            new_pos = Position(0, pos.y+1)
        else:
            # Indicate grid is done
            return Position(9, 8)
        while self.initial_grid[new_pos.x][new_pos.y] != 0:
            new_pos = self.next_pos(new_pos)
            if new_pos.x == -1 or new_pos.x == 9:
                return new_pos
        return new_pos

    def prev_pos(self, pos):
        new_pos = Position(0,0)
        if pos.x > 0:
            new_pos = Position(pos.x-1, pos.y)
        elif pos.y > 0:
            new_pos = Position(0, pos.y-1)
        else:
            # Indicate grid is unsolvable
            return Position(-1, 0)
        while self.initial_grid[new_pos.x][new_pos.y] != 0:
            new_pos = self.next_pos(new_pos)
            if new_pos.x == -1 or new_pos.x == 9:
                return new_pos
        return new_pos

    def valid(self, pos, value):
        """ Tells if setting this value at this position is allowed """
        # Line
        for x in range(9):
            if self.get(Position(x, pos.y)) == value:
                return False
        # Column
        for y in range(9):
            if self.get(Position(pos.x, y)) == value:
                return False
        # Sub-square
        for x in range(3):
            for y in range(3):
                if self.get(Position(3*(pos.x//3) + x, 3*(pos.y//3) + y)) == value:
                    return False
        # All good
        return True
    
    def solve(self):
        pos = self.next_pos(Position(-1,0))
        while True:
            # print(self)
            value = self.get(pos) + 1
            while value <= 9 and not self.valid(pos, value):
                value += 1
            if value <= 9:
                self.set(pos, value)
                pos = self.next_pos(pos)
                if pos.x == 9:
                    return True
            else:
                self.set(pos, 0)
                pos = self.prev_pos(pos)
                if pos.x == -1:
                    return False
    
    def __str__(self):
        footer = "+-----+-----+-----+\n"
        result = footer
        for y in range(9):
            result += "|"
            for x in range(9):
                result += str(self.grid[x][y])
                if x % 3 == 2:
                    result += "|"
                else:
                    result += " "
            result += "\n"
            if y % 3 == 2:
                result += footer
        return result


if __name__ == "__main__":
    grid = Grid()
    print(grid)