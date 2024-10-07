from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QButtonGroup
from timeit import default_timer as timer
from UiClass import Ui_MainWindow
import numpy as np
import csv
import ast


class Code_for_ui(QtWidgets.QMainWindow):
    '''
    Class inherits the ui from the module Ui_MainWindow
    Logic and code are specified here while ui elements should be within the other document
    '''

    def __init__(self):
        '''
        Establishes the connections between buttons and functions as well as class instance variables
        '''
        super(Code_for_ui, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # list of all input areas in order for easy manipulation
        self.board_all = [
            self.ui.pos0, self.ui.pos1, self.ui.pos2, self.ui.pos3, self.ui.pos4, self.ui.pos5, self.ui.pos6, self.ui.pos7, self.ui.pos8,
            self.ui.pos10, self.ui.pos11, self.ui.pos12, self.ui.pos13, self.ui.pos14, self.ui.pos15,self.ui.pos16, self.ui.pos17, self.ui.pos18,
            self.ui.pos20, self.ui.pos21, self.ui.pos22, self.ui.pos23, self.ui.pos24, self.ui.pos25, self.ui.pos26, self.ui.pos27, self.ui.pos28,
            self.ui.pos30, self.ui.pos31, self.ui.pos32, self.ui.pos33, self.ui.pos34, self.ui.pos35, self.ui.pos36, self.ui.pos37, self.ui.pos38,
            self.ui.pos40, self.ui.pos41, self.ui.pos42, self.ui.pos43, self.ui.pos44, self.ui.pos45, self.ui.pos46, self.ui.pos47, self.ui.pos48,
            self.ui.pos50, self.ui.pos51, self.ui.pos52, self.ui.pos53, self.ui.pos54, self.ui.pos55, self.ui.pos56, self.ui.pos57, self.ui.pos58,
            self.ui.pos60, self.ui.pos61, self.ui.pos62, self.ui.pos63, self.ui.pos64, self.ui.pos65, self.ui.pos66, self.ui.pos67, self.ui.pos68,
            self.ui.pos70, self.ui.pos71, self.ui.pos72, self.ui.pos73, self.ui.pos74, self.ui.pos75, self.ui.pos76, self.ui.pos77, self.ui.pos78,
            self.ui.pos80, self.ui.pos81, self.ui.pos82, self.ui.pos83, self.ui.pos84, self.ui.pos85, self.ui.pos86, self.ui.pos87, self.ui.pos88
            ]

        # where solo boards are saved and rewritten as necessary
        self.board = []
        # indexing for boards from csv files
        self.index = 0

        # button connections for functions
        self.ui.reset_button.clicked.connect(self.clearboard)
        self.ui.solve_button.clicked.connect(self.check_board)
        self.ui.solo_start.clicked.connect(self.solo_start_func)
        self.ui.solo_check_solution.clicked.connect(self.check_solo)
        self.ui.solo_reset_button.clicked.connect(self.solo_reset)
        self.ui.hard_radio.clicked.connect(self.set_difficulty_hard)
        self.ui.medium_radio.clicked.connect(self.set_difficulty_medium)
        self.ui.easy_radio.clicked.connect(self.set_difficulty_easy)

        # tool tips for users
        self.ui.solve_button.setToolTip("Click here to solve the board.")
        self.ui.reset_button.setToolTip("Click here to completely reset the board.")
        self.ui.solo_start.setToolTip("Click here to save the current board while you play by yourself.")
        self.ui.solo_check_solution.setToolTip("Ready to check if you have solved the puzzle?.")
        self.ui.solo_reset_button.setToolTip("Click here to reset board to the same position from when you clicked \"Start Playing\".")
        self.ui.new_board_button.setToolTip("Cycle through a selection of saved boards .")

        # radio group set up
        self.ui.button_group = QButtonGroup(self)
        self.ui.button_group.addButton(self.ui.easy_radio)
        self.ui.button_group.addButton(self.ui.medium_radio)
        self.ui.button_group.addButton(self.ui.hard_radio)

    def set_difficulty_easy(self):
        '''
        Further sets up the radio functionality,
        resets index,
        and indicates the file where the Sudoku boards are located at to following functions
        '''
        self.ui.new_board_button.disconnect()
        self.index = 0
        self.ui.new_board_button.clicked.connect(lambda:self.new_board('easy-boards.csv'))

    def set_difficulty_medium(self):
        self.ui.new_board_button.disconnect()
        self.index = 0
        self.ui.new_board_button.clicked.connect(lambda:self.new_board('medium-boards.csv'))

    def set_difficulty_hard(self):
        self.ui.new_board_button.disconnect()
        self.index = 0
        self.ui.new_board_button.clicked.connect(lambda:self.new_board('hard-boards.csv'))

    def new_board(self, file_name):
        '''
        Opens the file corresponding to the selected difficulty
        creates a list of all boards
        displays one board at a time
        also print which board number they have currently selected
        In case opening files each time becomes an issue, could be reworked into two functions although then click behaviour has to be changed
        '''
        with open(file_name, 'r') as handle:
            values = ['board_num', 'list']
            reader = csv.DictReader(handle, fieldnames=values)
            next(reader)
            boards = []

            for row in reader:
                board = row['list']
                boards.append(board)

        s_board = boards[self.index % len(boards)]
        board = ast.literal_eval(s_board)

        for val, pos in zip(board, self.board_all):
            if int(val) == 0:
                pos.setPlainText('')
            else:
                pos.setPlainText(str(val))

        self.ui.sudoku_number.setText(f'Sudoku no. {(self.index % len(boards)) + 1 }')
        self.index += 1

    def global_check_user_input(self, board):
        '''
        Checks for validity of inputs
        Returns True if there are no issues
        Normalizes blank spaces to 0s
        '''
        for input_val in board:
            if input_val == '':
                input_val = 0

            try:
                input_val = int(input_val)
            except:
                # self.clearboard()
                self.ui.results_tag.setText('Please only input numbers')
                return

            if input_val not in range(0, 10):
                # self.clearboard()
                self.ui.results_tag.setText('Please only input numbers from 1-9')
                return
        return True

    def solo_start_func(self):
        '''
        Checks user input board and saves the board to the class instance variable
        '''
        board = []
        for pos in self.board_all:
            input_val = pos.toPlainText()
            board.append(input_val)

        if self.global_check_user_input(board):
            self.board = board

    def solo_reset(self):
        '''
        Provides a clean reset of the the board except it re=establishes the saved board state
        also updates the results tag
        '''
        for val, pos in zip(self.board, self.board_all):
            if val == 0:
                pos.setPlainText('')
            else:
                pos.setPlainText(str(val))
        self.ui.results_tag.setText('Board has been reset to start of puzzle')

    def check_solo(self):
        '''
        Checks if board is complete and correct
        updates results tags accordingly
        '''
        board = []
        final_board = []
        for pos in self.board_all:
            if pos == '' or 0:
                self.ui.results_tag.setText('Sorry... Solution is not the right answer')
                return
            input_val = pos.toPlainText().strip()
            board.append(input_val)

        if not self.global_check_user_input(board):
            return

        for val in board:
            try:
                input_val = int(val)
            except:
                self.ui.results_tag.setText('Please only input numbers')
                return
            final_board.append(input_val)

        arr = np.array(board, dtype=np.int64).reshape((9, 9))
        all_uniques = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

        for row in range(9):
            for column in range(9):
                row_vals = np.unique(arr[row])
                col_vals = np.unique(arr[:, column].flatten())
                r_start = (row//3)*3
                c_start = (column//3)*3
                grid_vals = np.unique(arr[r_start:r_start+3, c_start:c_start+3].flatten())

                if not np.array_equal(row_vals, all_uniques) or not np.array_equal(col_vals, all_uniques) or not np.array_equal(grid_vals, all_uniques):
                    self.ui.results_tag.setText('Sorry... Solution is not the right answer')
                    return
        else:
            self.ui.results_tag.setText('Congratulations! The solution is correct')

    def clearboard(self):
        '''
        Completely clears the board by replacing all input values with ''
        also updates the results tag
        '''
        for pos in self.board_all:
            pos.setPlainText('')
        self.ui.results_tag.setText(f'It took Python and Numpy: X seconds to solve this Sudoku Board!')


    def check_board(self):
        '''
        Checks the user input, converts into an np.array,
        sends array to solve_board()
        '''
        board = []

        for pos in self.board_all:
            input_val = pos.toPlainText()
            if input_val == '':
                input_val = 0
            try:
                input_val = int(input_val)
            except:
                self.ui.results_tag.setText('Please only input numbers')
                return
            if input_val not in range(0, 10):
                self.ui.results_tag.setText('Please only input numbers from 1-9')
                return
            board.append(input_val)

        arr_long = np.array(board)
        arr = arr_long.reshape(9, 9)
        self.solve_board(arr)

    def solve_board(self, arr):
        '''
        Solves the Sudoku Board
        uses a recursive function solve() to look for possible solutions
        check() is used to determine if solution is valid
        also prints the time it took to solve the puzzle
        '''

        def check(arr, row, column, choice):
            row_vals = np.unique(arr[row])
            if choice in row_vals:
                return False

            col_vals = np.unique(arr[:, column].flatten())
            if choice in col_vals:
                return False

            r_start = (row//3)*3
            c_start = (column//3)*3
            grid_vals = np.unique(arr[r_start:r_start+3, c_start:c_start+3].flatten())
            if choice in grid_vals:
                return False

            return True

        def solve(arr):
            for num in range(81):
                row, column = divmod(num, 9)
                if arr[row, column] == 0:
                    for choice in range(1, 10):
                        if check(arr, row, column, choice):
                            arr[row, column] = choice
                            if solve(arr):
                                return True
                            arr[row, column] = 0
                    return False
            return True

        start = timer()
        solve(arr)
        end = timer()

        time = end - start
        self.ui.results_tag.setText(f'It took Python and Numpy: {time:.3f} seconds to solve this Sudoku Board!')
        self.display_nums(arr)

    def display_nums(self, arr):
        '''
        Displays the solved board
        takes a numpy array, zips values that correspond to the input areas,
        and sets the text accordingly
        '''
        arr_list = arr.flatten().tolist()
        for val, pos in zip(arr_list, self.board_all):
            pos.setPlainText(str(val))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Code_for_ui()
    MainWindow.show()
    sys.exit(app.exec_())
