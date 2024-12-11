# -*- coding: utf-8 -*-
"""SudokuSolvingOptimization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Tv3TKXJFxh4JtRjiM6fIcOuq7zT7MQiD

# **README**
we have 5 algorithms:
1. serial recursive backtracking algorithm
2. parallel recursive backtracking (cpu)
3. parallel recursive backtracking (gpu)
4. parallel constraint propogation and recursive backtracking method (cpu)
5. parallel constraint propogation and recursive backtracking method(gpu)

libraries used: numpy, ThreadPoolExecutor, cupy

---------------------------------------------------------------------------
# **How to run code?**

Make sure to run the board initialization code, this will ensure our solvers know what to solve

make sure you have installed
**pip install numpy**

for 3 and 5 (GPU Utilized algorithms):
**Runtime > Change runtime type > T4 GPU**

install cupy:
**!pip install cupy-cuda11x**

--------------------------------------------------------------------------
more info about board:

easy- easy to solve

medium - medium to solve

hard - hard to solve

evil- hardest to solve


-----------------------------------------------------------------------
More information about our project https://github.com/hibashaalan/sudoku

board difficulty based on https://www.websudoku.com/

serial algorithm based on https://github.com/nuhanishat/sudoku-stuff

# **Board Intialization Code**
"""

import numpy as np


board1_easy = [[8, 0, 0, 5, 1, 0, 0, 0, 2],
               [0, 0, 6, 9, 8, 0, 4, 5, 0],
               [0, 0, 0, 0, 0, 6, 0, 0, 0],
               [3, 5, 0, 7, 0, 0, 6, 1, 0],
               [0, 0, 9, 6, 2, 5, 7, 0, 0],
               [0, 7, 4, 0, 0, 3, 0, 8, 5],
               [0, 0, 0, 3, 0, 0, 0, 0, 0],
               [0, 2, 3, 0, 7, 9, 1, 0, 0],
               [7, 0, 0, 0, 5, 2, 0, 0, 3]]

np.save('1_Easy', np.array(board1_easy))
#print(np.array(board1_easy))


board2_medium = [[7, 2, 1, 0, 8, 0, 0, 6, 0],
		[0, 0, 0, 7, 0, 0, 8, 0, 0],
		[0, 0, 0, 1, 0, 0, 0, 9, 5],
		[0, 0, 8, 3, 0, 6, 0, 0, 9],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[9, 0, 0, 2, 0, 5, 1, 0, 0],
		[6, 9, 0, 0, 0, 1, 0, 0, 0],
		[0, 0, 5, 0, 0, 2, 0, 0, 0],
		[0, 1, 0, 0, 7, 0, 6, 5, 3]]

np.save('2_Medium', np.array(board2_medium))

board3_hard = [[0, 0, 0, 0, 1, 0, 0, 9, 0],
		[0, 0, 0, 0, 0, 2, 7, 0, 0],
		[6, 3, 1, 5, 0, 0, 4, 2, 0],
		[0, 0, 4, 0, 0, 0, 2, 0, 7],
		[0, 0, 0, 0, 4, 0, 0, 0, 0],
		[3, 0, 5, 0, 0, 0, 6, 0, 0],
		[0, 8, 7, 0, 0, 4, 9, 3, 1],
		[0, 0, 6, 9, 0, 0, 0, 0, 0],
		[0, 5, 0, 0, 7, 0, 0, 0, 0]]

np.save('3_Hard', np.array(board3_hard))

board4_evil = [[4, 0, 0, 0, 0, 3, 0, 6, 0],
		[0, 0, 0, 9, 2, 0, 0, 0, 0],
		[0, 5, 0, 0, 0, 6, 0, 9, 8],
		[7, 0, 0, 0, 0, 5, 0, 0, 0],
		[8, 0, 1, 0, 0, 0, 3, 0, 4],
		[0, 0, 0, 6, 0, 0, 0, 0, 7],
		[2, 4, 0, 3, 0, 0, 0, 1, 0],
		[0, 0, 0, 0, 1, 4, 0, 0, 0],
		[0, 3, 0, 7, 0, 0, 0, 0, 9]]

np.save('4_Evil', np.array(board4_evil))

"""# **Serial Recursive Backtracking**"""

import numpy as np


class Sudoku():
    def __init__(self, board):
        self.board = board
        self.rows = range(9)
        self.columns = range(9)
        self.boxes = range(9)
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.backtracked = 0


    # Find unassigned blanks
    def find_blanks(self, count): # count keeps track of the current cell location
        for i in self.rows:
            for j in self.columns:
                if self.board[i][j] == 0:
                    count[0] = i
                    count[1] = j
                    return True
        return False

    # Returns domain after checking row constraints
    def check_rows_dom(self, row):
        values = self.values.copy()
        for i in self.columns:
            if self.board[row][i] in values:
                values.remove(self.board[row,i])
        return values

    # Returns domain after checking column constraints
    def check_columns_dom(self, column):
        values = self.values.copy()
        for i in self.rows:
            if self.board[i][column] in values:
                values.remove(self.board[i][column])
        return values

    # Returns domain after checking box constraints
    def check_boxes_dom(self, row, column):
        values = self.values.copy()
        for i in range(3):
            for j in range(3):
                if self.board[row+i][column+j] in values:
                    values.remove(self.board[row+i][column+j])
        return values


    # Find all the unassigned variables that meet the meets the constraints
    def find_constrained_dom(self, row, column):
        row_dom = self.check_rows_dom(row)
        col_dom = self.check_columns_dom(column)
        box_dom = self.check_boxes_dom(row-row%3, column-column%3)


        ordered_dom = set(row_dom).intersection(set(col_dom), set(box_dom))
        return list(ordered_dom)


    # What is backtracking doing?

        # It checks if a cell is blank, keeps the previous structure. Count is the starting cell
        # If blank:
            # Find possible values that could go in the cell (domain)
            # Update list of unassigned variables with the domain found (The idea is to reduce the search space)
            # For each value in domain, start searching.....
                # Do your usual backtracking stuff


    def backtracking(self, count):
        if not self.find_blanks(count):
            return True

        row = count[0]
        column = count[1]

        cell_dom = self.find_constrained_dom(row, column)

        for j in range(len(cell_dom)):
            self.board[row][column] = cell_dom[j]

            if self.backtracking(count):
                return True

            self.board[row][column] = 0

            if self.board[row][column] == 0:
                self.backtracked += 1

        return False




if __name__ == '__main__':


    board1 = np.load('1_Easy.npy')
    board2 = np.load('2_Medium.npy')
    board3 = np.load('3_Hard.npy')
    board4 = np.load('4_Evil.npy')

    board_name = {'Easy':board1, 'Medium':board2, 'Hard':board3, 'Evil':board4}
    board = ['Easy', 'Medium', 'Hard', 'Evil']


    for item in board:
        sudoku = Sudoku(board_name[item])

        # sudoku.update_unassigned()
        result = sudoku.backtracking([0, 0])


        if result == True:
            print(f"Solved {item} Sudoku Board:")
            print(np.matrix(sudoku.board))
            print('Number of times backtracked: ', sudoku.backtracked)
        else:
            print('No solution')

"""# **Parallel Recursive Backtracking**

***CPU Utilized Algorithm***
"""

import numpy as np
from concurrent.futures import ThreadPoolExecutor

class Sudoku():
    def __init__(self, board):
        self.board = board
        self.rows = range(9)
        self.columns = range(9)
        self.boxes = range(9)
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.backtracked = 0

    def find_blanks(self, count):
        for i in self.rows:
            for j in self.columns:
                if self.board[i][j] == 0:
                    count[0] = i
                    count[1] = j
                    return True
        return False

    def check_rows_dom(self, row):
        values = self.values.copy()
        for i in self.columns:
            if self.board[row][i] in values:
                values.remove(self.board[row, i])
        return values

    def check_columns_dom(self, column):
        values = self.values.copy()
        for i in self.rows:
            if self.board[i][column] in values:
                values.remove(self.board[i][column])
        return values

    def check_boxes_dom(self, row, column):
        values = self.values.copy()
        for i in range(3):
            for j in range(3):
                if self.board[row + i][column + j] in values:
                    values.remove(self.board[row + i][column + j])
        return values

    def find_constrained_dom(self, row, column):
        row_dom = self.check_rows_dom(row)
        col_dom = self.check_columns_dom(column)
        box_dom = self.check_boxes_dom(row - row % 3, column - column % 3)

        ordered_dom = set(row_dom).intersection(set(col_dom), set(box_dom))
        return list(ordered_dom)

    def backtracking(self, count):
        if not self.find_blanks(count):
            return True

        row = count[0]
        column = count[1]

        cell_dom = self.find_constrained_dom(row, column)

        for j in range(len(cell_dom)):
            self.board[row][column] = cell_dom[j]

            if self.backtracking(count):  # Recursive backtracking
                return True

            self.board[row][column] = 0

            if self.board[row][column] == 0:
                self.backtracked += 1

        return False

    def parallel_backtracking(self, initial_choices):
        """Solve the Sudoku puzzle by exploring different starting points in parallel."""
        solutions = []

        def solve_partial_board(start_value):
            temp_board = self.board.copy()
            temp_board[0][0] = start_value  # Assume first blank cell for parallelization
            temp_sudoku = Sudoku(temp_board)
            if temp_sudoku.backtracking([0, 0]):
                return temp_sudoku.board, temp_sudoku.backtracked
            return None

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(solve_partial_board, value) for value in initial_choices]

            for future in futures:
                result = future.result()
                if result:
                    solutions.append(result)
                    break  # Stop other threads when a solution is found

        return solutions[0] if solutions else None


if __name__ == '__main__':
    board1 = np.load('1_Easy.npy')
    board2 = np.load('2_Medium.npy')
    board3 = np.load('3_Hard.npy')
    board4 = np.load('4_Evil.npy')

    board_name = {'Easy': board1, 'Medium': board2, 'Hard': board3, 'Evil': board4}
    board_difficulty = ['Easy', 'Medium', 'Hard', 'Evil']

    for item in board_difficulty:
        sudoku = Sudoku(board_name[item])

        # Generate initial choices for the first empty cell
        initial_choices = sudoku.find_constrained_dom(0, 0)
        if not initial_choices:
            print(f"No valid starting values for {item} puzzle.")
            continue

        # Solve the puzzle using parallel backtracking
        solution = sudoku.parallel_backtracking(initial_choices)

        if solution:
            solved_board, backtracked_count = solution
            print(f"Solved {item} Sudoku Board:")
            print(np.matrix(solved_board))
            print('Number of times backtracked:', backtracked_count)
        else:
            print(f"No solution found for {item} puzzle.")

"""***GPU Utilized Algorithm***"""

import cupy as cp
from concurrent.futures import ThreadPoolExecutor
import time

class Sudoku():
    def __init__(self, board):
        self.board = cp.array(board)
        self.rows = range(9)
        self.columns = range(9)
        self.boxes = range(9)
        self.values = cp.arange(1, 10)
        self.backtracked = 0

    def find_blanks(self, count):
        for i in self.rows:
            for j in self.columns:
                if self.board[i, j] == 0:
                    count[0] = i
                    count[1] = j
                    return True
        return False

    def check_rows_dom(self, row):
        values = cp.copy(self.values)
        for i in self.columns:
            if self.board[row, i] in values:
                values = values[values != self.board[row, i]]
        return values

    def check_columns_dom(self, column):
        values = cp.copy(self.values)
        for i in self.rows:
            if self.board[i, column] in values:
                values = values[values != self.board[i, column]]
        return values

    def check_boxes_dom(self, row, column):
        values = cp.copy(self.values)
        start_row, start_col = row - row % 3, column - column % 3
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i, start_col + j] in values:
                    values = values[values != self.board[start_row + i, start_col + j]]
        return values

    def find_constrained_dom(self, row, column):
        row_dom = self.check_rows_dom(row)
        col_dom = self.check_columns_dom(column)
        box_dom = self.check_boxes_dom(row, column)

        ordered_dom = cp.intersect1d(cp.intersect1d(row_dom, col_dom), box_dom)
        return ordered_dom

    def backtracking(self, count):
        if not self.find_blanks(count):
            return True

        row = count[0]
        column = count[1]

        cell_dom = self.find_constrained_dom(row, column)

        for value in cell_dom:
            self.board[row, column] = value

            if self.backtracking(count):  # Recursive backtracking
                return True

            self.board[row, column] = 0
            self.backtracked += 1

        return False

    def parallel_backtracking(self, initial_choices):
        """Solve the Sudoku puzzle by exploring different starting points in parallel."""
        solutions = []

        def solve_partial_board(start_value):
            temp_board = cp.copy(self.board)
            temp_board[0, 0] = start_value  # Assume first blank cell for parallelization
            temp_sudoku = Sudoku(temp_board)
            if temp_sudoku.backtracking([0, 0]):
                return cp.asnumpy(temp_sudoku.board), temp_sudoku.backtracked
            return None

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(solve_partial_board, value) for value in initial_choices]

            for future in futures:
                result = future.result()
                if result:
                    solutions.append(result)
                    break  # Stop other threads when a solution is found

        return solutions[0] if solutions else None

if __name__ == '__main__':
    board1 = cp.load('1_Easy.npy')
    board2 = cp.load('2_Medium.npy')
    board3 = cp.load('3_Hard.npy')
    board4 = cp.load('4_Evil.npy')

    board_name = { 'Easy': board1, 'Medium': board2, 'Hard': board3, 'Evil': board4}
    board_difficulty = ['Easy', 'Medium', 'Hard', 'Evil']

    for item in board_difficulty:
        sudoku = Sudoku(board_name[item])

        # Generate initial choices for the first empty cell
        initial_choices = sudoku.find_constrained_dom(0, 0)
        if not initial_choices.size:
            print(f"No valid starting values for {item} puzzle.")
            continue

        # Solve the puzzle using parallel backtracking
        solution = sudoku.parallel_backtracking(initial_choices)

        if solution:
            solved_board, backtracked_count = solution
            print(f"Solved {item} Sudoku Board:")
            print(cp.array(solved_board))
            print('Number of times backtracked:', backtracked_count)

"""# **Parallel Constraint Propagation and Recursive Backtracking**

***CPU Utilized Algorithm***
"""

from concurrent.futures import ThreadPoolExecutor
import numpy as np
import copy

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.backtracked = 0  # Counter for backtracks

    def is_valid(self, row, col, num):
        """Check if placing num at board[row][col] is valid."""
        # Check row and column
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def find_candidates(self):
        """Generate candidates for each empty cell."""
        candidates = {}
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    candidates[(row, col)] = {num for num in range(1, 10) if self.is_valid(row, col, num)}
        return candidates

    def propagate_constraints(self, candidates):
        """Propagate constraints to reduce candidates."""
        changed = True
        while changed:
            changed = False
            for (row, col), possible_nums in list(candidates.items()):
                if len(possible_nums) == 1:
                    # Only one candidate; place it on the board
                    num = possible_nums.pop()
                    self.board[row][col] = num
                    del candidates[(row, col)]
                    changed = True

                    # Update constraints
                    for i in range(9):
                        candidates.get((row, i), set()).discard(num)  # Row
                        candidates.get((i, col), set()).discard(num)  # Column
                    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                    for i in range(start_row, start_row + 3):
                        for j in range(start_col, start_col + 3):
                            candidates.get((i, j), set()).discard(num)
        return candidates

    def solve_with_constraints(self):
        """Solve the Sudoku using constraint propagation and backtracking."""
        candidates = self.find_candidates()
        candidates = self.propagate_constraints(candidates)

        # If no candidates left, return solved board or continue backtracking
        if not candidates:
            return True  # Solved

        # Pick the cell with the fewest candidates
        (row, col), possible_nums = min(candidates.items(), key=lambda x: len(x[1]))

        for num in possible_nums:
            # Create a copy of the board and candidates for recursive solving
            new_board = copy.deepcopy(self.board)
            new_candidates = copy.deepcopy(candidates)
            new_board[row][col] = num
            new_solver = SudokuSolver(new_board)
            new_solver.backtracked = self.backtracked  # Carry over backtrack count

            # Update candidates and propagate constraints
            new_candidates = new_solver.propagate_constraints(new_candidates)
            if new_solver.solve_with_constraints():
                # Update current board and backtrack count from successful branch
                self.board = new_solver.board
                self.backtracked = new_solver.backtracked
                return True

            # Increment backtrack counter if solution failed
            self.backtracked += 1

        return False

if __name__ == "__main__":
    # Load Sudoku boards
    board1 = np.load('1_Easy.npy')
    board2 = np.load('2_Medium.npy')
    board3 = np.load('3_Hard.npy')
    board4 = np.load('4_Evil.npy')

    # Choose a board to solve
    board_name = {'Easy': board1, 'Medium': board2, 'Hard': board3, 'Evil': board4}
    board_difficulty = ['Easy', 'Medium', 'Hard', 'Evil']

    for item in board_difficulty:
        sudoku = Sudoku(board_name[item])
        solver = SudokuSolver(sudoku.board)
        if solver.solve_with_constraints():
            print("Solved Sudoku:")
            for row in solver.board:
                print(row)
            print(f"Backtracks: {solver.backtracked}")
        else:
            print("No solution found.")

"""***GPU Utilized Algorithm***"""

import cupy as cp
import numpy as np
import copy
import time

class SudokuSolverGPU:
    def __init__(self, board):
        self.board = cp.array(board)  # Store the board as a CuPy array
        self.backtracked = 0  # Counter for backtracks

    def is_valid(self, row, col, num):
        """Check if placing num at board[row][col] is valid."""
        # Check row and column
        if cp.any(self.board[row, :] == num) or cp.any(self.board[:, col] == num):
            return False

        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        if cp.any(self.board[start_row:start_row + 3, start_col:start_col + 3] == num):
            return False

        return True

    def is_completed(self):
        """Check if the board is already completed."""
        return cp.all(self.board != 0)

    def find_candidates(self):
        """Generate candidates for each empty cell using GPU acceleration."""
        candidates = {}
        empty_cells = cp.argwhere(self.board == 0)

        for row, col in empty_cells:
            possible_nums = {
                num for num in range(1, 10) if self.is_valid(row.item(), col.item(), num)
            }
            candidates[(row.item(), col.item())] = possible_nums
        return candidates

    def propagate_constraints(self, candidates):
        """Propagate constraints using GPU acceleration."""
        changed = True
        while changed:
            changed = False
            for (row, col), possible_nums in list(candidates.items()):
                if len(possible_nums) == 1:
                    # Only one candidate; place it on the board
                    num = possible_nums.pop()
                    self.board[row, col] = num
                    del candidates[(row, col)]
                    changed = True

                    # Update constraints
                    for i in range(9):
                        candidates.get((row, i), set()).discard(num)  # Row
                        candidates.get((i, col), set()).discard(num)  # Column
                    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                    for i in range(start_row, start_row + 3):
                        for j in range(start_col, start_col + 3):
                            candidates.get((i, j), set()).discard(num)
        return candidates

    def solve_with_constraints(self):
        """Solve the Sudoku using constraint propagation and backtracking."""
        candidates = self.find_candidates()
        candidates = self.propagate_constraints(candidates)

        # If no candidates left, return solved board or continue backtracking
        if not candidates:
            return True  # Solved

        # Pick the cell with the fewest candidates
        (row, col), possible_nums = min(candidates.items(), key=lambda x: len(x[1]))

        # Guessing using Recursive Backtracking
        for num in possible_nums:
            # Create a copy of the board and candidates for recursive solving
            new_board = copy.deepcopy(self.board)
            new_candidates = copy.deepcopy(candidates)
            new_board[row, col] = num
            new_solver = SudokuSolverGPU(new_board)
            new_solver.backtracked = self.backtracked  # Carry over backtrack count

            # Update candidates and propagate constraints
            new_candidates = new_solver.propagate_constraints(new_candidates)
            if new_solver.solve_with_constraints():
                # Update current board and backtrack count from successful branch
                self.board = new_solver.board
                self.backtracked = new_solver.backtracked
                return True

            # Increment backtrack counter if solution failed
            self.backtracked += 1

        return False


if __name__ == "__main__":
    # Load boards
    board1 = np.load('1_Easy.npy')
    board2 = np.load('2_Medium.npy')
    board3 = np.load('3_Hard.npy')
    board4 = np.load('4_Evil.npy')

    # Map boards
    board_name = {'Easy': board1, 'Medium': board2,
        'Hard': board3, 'Evil': board4
    }
    board_difficulty = ['Easy', 'Medium', 'Hard', 'Evil']

    for item in board_difficulty:
        sudoku = SudokuSolverGPU(board_name[item])

        # Check if the puzzle is already completed/invalid
        if sudoku.is_completed():
            print(f"No valid starting values for {item} puzzle.")
            continue

        # Solve the puzzle if it's valid and not completed
        if sudoku.solve_with_constraints():
            print(f"Solved {item} Sudoku Board:")
            for row in cp.asnumpy(sudoku.board):  # Convert CuPy array back to NumPy for printing
                print(row)
            print(f"Backtracks: {sudoku.backtracked}")
        else:
            print(f"No solution found for {item} Sudoku Board.")