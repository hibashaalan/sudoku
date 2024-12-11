# Accelerating Sudoku Solving Algorithms through Parallel Programming
**README**
we have 5 algorithms:
1. serial recursive backtracking algorithm
2. parallel recursive backtracking (cpu)
3. parallel recursive backtracking (gpu)
4. parallel constraint propogation and recursive backtracking method (cpu)
5. parallel constraint propogation and recursive backtracking method(gpu)

libraries used: numpy, ThreadPoolExecutor, cupy

---------------------------------------------------------------------------
# **How to run code?**
Recommended to use Google Colab

Make sure to run the board initialization code, this will ensure our solvers know what to solve

make sure you have installed 
**pip install numpy**

for 3 and 5 (GPU Utilized algorithms):
**Runtime > Change runtime type > T4 GPU**

install cupy: 
**!pip install cupy-cuda11x**

--------------------------------------------------------------------------
file info:

SudokuSolvingOptimization: Colab Notebook containing all algorithms 
Sudoku Matplots: Colab Containing all matplots used for algorithms and in paper 

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
