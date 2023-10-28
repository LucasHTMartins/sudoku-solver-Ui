# sudoku-solver
Sudoku Solver with UI, solo play, and saved boards (python and numpy)

This program is capable of solving any sudoku board, its primary function is to read user inputs within a 9x9 board and prints a completed board. The program and user interface are also capable of several secondary functions such as: storing a board state for solo play, checking current board state for completion, partial resetting to the saved board state, acessing easy, medium, and hard board from csv files, and displaying useful/interesting information to the user such as completion times.

# User Interface Summary

Board - Takes user input, displays solved boards, and allows for solo play

Main Buttons - Solves current board, completely resets the board accordingly

Solo Play - Saves current board for solo play, resets back to this current board state and checks for solo play completion

Saved Boards - Radio buttons cycle through the csv files and display the board to the user

Results - Display useful information such and time to solve, completion status, and reset messages.

# Code 

UIClass.py - Was primarily created by PyQt5's Designer and could easily be modified and rebuilt within similar parameters. Contains some feature documentation.

easy-boards.csv, medium-boards.csv, hard-boards.csv - Contain boards that were handpicked from various online repositories. Some of the hard boards were chosen for their human-logic difficulty (and are solved rather quickly by the algorythm) others were found to take considerably longer for a computer algorythm to solve. 

sudoku.py - Contains all the programming logic behind the button connections and functions. It has more substantial documentation for each of its working components 
