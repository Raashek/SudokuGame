###########
# modules #
###########

import random



#####################
#  Generate Sudoku  #
#####################

numbers = [1,2,3,4,5,6,7,8,9]

#I: None
#O: None or a list
def genBoard():

    # Create a matrix 9x9 with mpty variables. 
    # matrix empty shell
    board = [[None for _ in range(9)] for _ in range(9)]

    # Rows
    for i in range(9):
        #Columns
        for j in range(9):
            #reorder the order of the numbers list
            values = numbers
            random.shuffle(values)

            counter = -1

            # moves around the board, place by place 
            while board[i][j] is None:
                counter += 1
                
                if counter == 9:
                    return None
                
                # Gets a number from the 0 to 9
                # [values[counter], True]
                generateNumber = values[counter]

                # Checks if the values is in the board rows. If it is, continues to the next one.
                if generateNumber in board[i]:
                    continue
                
                # Checks if the value of a position is  in the columns.
                inCloumn = False
                for elem in board:
                    if elem[j] == generateNumber:

                        inCloumn = True

                if inCloumn: 
                    continue
                
                # Checks next values if they are the same
                # cases: 1, 4, 7
                if i % 3 == 1:
                    # cases: 3, 6, 9
                    if   j % 3 == 0 and generateNumber in (board[i-1][j+1],board[i-1][j+2]): 
                        continue
                    # cases: 1, 4, 7
                    elif j % 3 == 1 and generateNumber in (board[i-1][j-1],board[i-1][j+1]): 
                        continue
                    # cases: 2, 8, 5
                    elif j % 3 == 2 and generateNumber in (board[i-1][j-1],board[i-1][j-2]): 
                        continue
                
                # cases: 2, 8, 5
                elif i % 3 == 2:
                    # cases: 3, 6, 9
                    if   j % 3 == 0 and generateNumber in (board[i-1][j+1],board[i-1][j+2],board[i-2][j+1],board[i-2][j+2]): 
                        continue
                    # cases: 1, 4, 7
                    elif j % 3 == 1 and generateNumber in (board[i-1][j-1],board[i-1][j+1],board[i-2][j-1],board[i-2][j+1]): 
                        continue
                    # cases: 1, 4, 7
                    elif j % 3 == 2 and generateNumber in (board[i-1][j-1],board[i-1][j-2],board[i-2][j-1],board[i-2][j-2]): 
                        continue

                # If everything's good, then asign number
                board[i][j] = generateNumber
    
    return board

#I: None
#O: List
# Generates a board
def stablishBoard():

    board = None
    while board is None:
        board = genBoard()
    return board



#I: list, number
#O: None or a list
# Given a percentage, replaces numbers of a sudoku list with 0
def replaceWithCero(matrix, percent):
    total_elements = len(matrix) * len(matrix[0])
    numToReplace = int(total_elements * (percent / 100))
    
    index = [(i, j) for i in range(len(matrix)) for j in range(len(matrix[0]))]
    random.shuffle(index)
    
    for i, j in index[:numToReplace]:
        matrix[i][j] = 0
    
    return matrix



####################
#  Solve a Sudoku  #
####################

# I: A list containing the sudoku
# O: Boolean
def itsSolved(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False
    return True

# I: A list containing the sudoku
# O: number
# Function finds the next empty cell to be filled
def nextEmpty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return -1, -1

# I: A list, 3 numbers 
# O: Boolean
# Checks if a number can be placed in a given cell based on Sudoku rules.
def checkNum(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True



####################
#  Main Functions  #
####################

# Creates sudokus with levels of difficulty
# I: None
# O: list
def getSudokuEasy():
    board = stablishBoard()
    return replaceWithCero(board, 25)
def getSudokuMedium():
    board = stablishBoard()
    return replaceWithCero(board, 50)
def getSudokuHard():
    board = stablishBoard()
    return replaceWithCero(board, 60)

# I: A list containing the sudoku
# O: Boolean
# If it has a sol then returns True if not returns False
def solveSudoku(board):

    if itsSolved(board):
        return True

    row, col = nextEmpty(board)
    for num in range(1, 10):
        if checkNum(board, row, col, num):
            board[row][col] = num

            if solveSudoku(board):
                return True

            board[row][col] = 0

    return False

# I: A list containing the sudoku
# O: Boolean or a list
# Returns a solution for a given sudoku
def solution(board):
    if solveSudoku(board):
        return board
    else:
        return False


def checkMatrix(matrix):
    # Check if the matrix has 9 rows
    if len(matrix) != 9:
        return False

    # Check if each row has 9 columns
    for row in matrix:
        if len(row) != 9:
            return False

    # Check if each element is a number between 0 and 9 (inclusive)
    for row in matrix:
        for element in row:
            if not isinstance(element, int) or element < 0 or element > 9:
                return False

    # If all conditions are satisfied, return True
    return True