from tkinter import *
from gameLogic import *
from jsonFunctions import *
import copy


matrixPrime = [[0] * 9 for _ in range(9)]
undoList = []
redoList = []
selectedNum = 0



####################
#  Aux Functions   #
####################

# Function for buttons with no use
# I: None
# O: None
def nothin():
    lblResult.set('')
    lblGood.set('')
    return 

# I: None
# O: None
def updateGUI():

    # Clear the existing values in the GUI grid
    # and update it with the new values from the sudoku_matrix

    for i in range(9):
        for j in range(9):
            # Assuming you have a Label widget representing each cell of the Sudoku grid
            # Update the text of each Label widget with the corresponding value from the matrix
            if matrixPrime[i][j] == 0:
                sudokuButtons[i][j].config(text = str(''), bd= 1 ,width= 5, height =2, fg="black", command = lambda row= i, col= j: assignNum(row,col)) 
            else:
                sudokuButtons[i][j].config(text= str(matrixPrime[i][j]), bd= 1, width= 5, height =2,  fg="black", command = nothin)

# I: None
# O: None
def checkWin():

    for row in range(len(matrixPrime)):
        for col in range(len(matrixPrime[0])):
            if matrixPrime[row][col] == 0:
                return
            
    lblGood.set('Congrats you won!!! :)')
    disableSudoku()
    disableUtilities()



# Group of functions that disables buttons.

# I: Lista and string
# O: None
def toggleBtnState(buttons, state):
    for button in buttons:
        button["state"] = state
# I: None
# O: None
def disableSudoku():
    toggleBtnState(allButtons, "disabled")
# I: None
# O: None
def disableLevels():
    toggleBtnState(levelBtns, "disabled")
# I: None
# O: None
def disableUtilities():
    toggleBtnState(utilityBtns, "disabled")


# I: None
# O: None
def saveSudoku():
    writeFile(matrixPrime)
# I: None
# O: None
def loadSudoku():
    global matrixPrime
    lblResult.set('')
    lblGood.set('')
    
    newMatrix = loadFile()
    if newMatrix == []:
        return
    elif checkMatrix(newMatrix):
        matrixPrime = newMatrix
        toggleBtnState(allButtons, "normal")
        toggleBtnState(utilityBtns, "normal")
        updateGUI()
    else:
        lblResult.set('Select a valid file')
        return 
# I: None
# O: None
def newGame():
    global matrixPrime, undoList, redoList
    lblResult.set('')
    lblGood.set('')

    disableSudoku()
    disableUtilities()
    toggleBtnState(levelBtns, "normal")

    # Set all values in the matrix to 0 or empty
    undoList = []
    redoList = []
    matrixPrime = [[0] * 9 for _ in range(9)]

    lblGood.set('Select a difficulty')
    updateGUI()
    return


# I: None
# O: None
def easyMode():
    global matrixPrime
    lblResult.set('')
    lblGood.set('')
    
    toggleBtnState(allButtons, "normal")
    toggleBtnState(utilityBtns, "normal")
    disableLevels()
    matrixPrime = getSudokuEasy()
    updateGUI()
    return
# I: None
# O: None
def mediumMode():
    global matrixPrime
    lblResult.set('')
    lblGood.set('')
    
    toggleBtnState(allButtons, "normal")
    toggleBtnState(utilityBtns, "normal")
    disableLevels()
    matrixPrime = getSudokuMedium()
    updateGUI()
    return 
# I: None
# O: None
def hardMode():
    global matrixPrime
    lblResult.set('')
    lblGood.set('')
    
    toggleBtnState(allButtons, "normal")
    toggleBtnState(utilityBtns, "normal")
    disableLevels()
    matrixPrime = getSudokuHard()
    updateGUI()
    return


# I: None
# O: None
def verify():

    global matrixPrime
    lblResult.set('')
    lblGood.set('')

    board = copy.deepcopy(matrixPrime)

    if solveSudoku(board):
        lblGood.set('This sudoku has solution')
    else:
        lblResult.set('This sudoku has no solution')

    return
# I: None
# O: None
def solve():
    global matrixPrime
    lblResult.set('')
    lblGood.set('')

    board = copy.deepcopy(matrixPrime)

    if solveSudoku(board):
        matrixPrime = solution(matrixPrime)
        disableSudoku()
        disableUtilities()
        updateGUI()
    else:
        lblResult.set('This sudoku has no solution')

    return


# I: None
# O: None
def undo():
    global matrixPrime, undoList, redoList
    lblResult.set('')
    lblGood.set('')
    
    if undoList == []:
        lblResult.set('There\'s nothing to undo')
    else:
        # undoAct = [action, row, col]
        undoAct = undoList.pop()
        row = undoAct[1]
        col = undoAct[2]
        matrixPrime[row][col] = 0

        # Stores the undoned action in the redo list. 
        # So after the undo act is done, then the user can redo again.
        redoList.append(undoAct)

        updateGUI()
    return 
# I: None
# O: None
def redo():
    global matrixPrime, undoList, redoList
    lblResult.set('')
    lblGood.set('')
    
    if redoList == []:
        lblResult.set('There\'s nothing to redo')
    else:
        # redoAct = [action, row, col]
        redoAct = redoList.pop()
        row = redoAct[1]
        col = redoAct[2]
        matrixPrime[row][col] = redoAct[0]

        # Stores the redoned action in the undo list.
        # So after the redo act is done, then the user can undo again. 
        undoList.append(redoAct)

        updateGUI()
    return


# I: A number (Integer)
# O: None
def selectNum(num):
    global selectedNum
    lblResult.set('')
    lblGood.set('')
    selectedNum = num
    return
# I: 2 numbers (Integers from 1 to 9)
# O: None
def assignNum(row, col):
    global selectedNum, matrixPrime, undoList
    lblResult.set('')
    lblGood.set('')

    if selectedNum == 0:
        lblResult.set('Select a number')
        return
    elif checkNum(matrixPrime, row, col, selectedNum):
        undoList.append([selectedNum, row, col])
        matrixPrime[row][col] = selectedNum
        selectedNum = 0
    else:
       lblResult.set('Can\'t place this number')
       selectedNum = 0 

    updateGUI()
    checkWin()
    return
    


################
#  Sudoku GUI  #
################

# Create a window 
root = Tk()
root.title("Sudoku")
root.geometry("900x410")


# Create frames for each group of buttons

mainFrame = Frame(root, highlightbackground= 'black', highlightthickness= 2, background='black')
mainFrame.place(x = 20, y = 25)

numPadFrame = Frame(root, width= 800, height= 800, highlightthickness= 2)
numPadFrame.place(x = 550, y = 110)

levelFrame = Frame(root)
levelFrame.place(x = 550, y= 60)

optionsFrame = Frame(root)
optionsFrame.place(x= 550, y = 20)

redoUndoFrame = Frame(root)
redoUndoFrame.place(x = 550, y = 300)

finishersFrame = Frame(root)
finishersFrame.place(x= 550, y = 350)



# Buttons: New game, load game, save.

newGame= Button(optionsFrame,text='New Game',width=10, command = newGame)
newGame.grid(row=0, column=0)

loadGame= Button(optionsFrame,text='Load Game',width=10,command= loadSudoku)
loadGame.grid(row=0, column=1)

saveGame= Button(optionsFrame,text='Save',width=10,command= saveSudoku)
saveGame.grid(row=0, column=2) 



# Buttons for difficulty levels: Easy, medium and hard.

easy = Button(levelFrame,text='Easy',width=6, command = easyMode)
easy.grid(row=0, column=0)

medium = Button(levelFrame,text='Medium',width=6,command= mediumMode)
medium.grid(row=0, column=1)

hard = Button(levelFrame,text='Hard',width=6,command= hardMode)
hard.grid(row=0, column=2)



# Buttons: Undo and redo

undo= Button(redoUndoFrame,text='Undo',width=6, command = undo)
undo.grid(row= 0, column= 0)

redo= Button(redoUndoFrame,text='Redo',width=6, command= redo)
redo.grid(row= 0, column= 1)



# Buttons: Verify if sudoku has a solution
verify = Button(finishersFrame, text='Verify',width=6, command= verify)
verify.grid(row= 0, column= 0)



# Buttons: Give up. Shows the solution of the current sudoku.

giveUp = Button(finishersFrame, text='Give Up',width=6, command= solve)
giveUp.grid(row= 0, column= 1)



#############################################################
# Store all difficyulty buttons in a list                   #
levelBtns = [easy, medium, hard]                            #
# Store all utility buttons in a list                       #
utilityBtns = [undo, redo, verify, giveUp, saveGame]        #
#############################################################



# Buttons: Close the window

close = Button(finishersFrame, text="Close",width=6, command= root.destroy)
close.grid(row= 0, column= 2)



# Buttons: Numpad for inputs

for i in range(1, 10):

    button = Button(numPadFrame, text=str(i), width= 5, height = 2, command= lambda i=i: selectNum(i))
    button.grid(row= (i-1)//3 + 100, column= (i-1)%3 + 7)



# Creates the whole matrix with the values of a solved sudoku.
sudokuButtons = []
# Store all buttons in a list
allButtons = []

for i in range(9):
    rowButtons = []

    for j in range(9):
        row = i
        col = j

        # Creates thick lines between rows and columns every 3 cells.
        rowPadding=(0,0)
        colPadding=(0,0)
        if (i == 3 or i == 6):
            rowPadding = (1,0)
        else:
            rowPadding = (0,0)
        if (j == 2 or  j == 5):
            colPadding = (0,1)
        else:
            colPadding = (0,0)

        # attributes of the sudoku buttons. If the position is 0 then the button must have the functionality to assign a number to it
        if matrixPrime[i][j] == 0:
            btn = Button(mainFrame, text = str(''), state="disabled", bd= 1 ,width= 5, height =2, fg="black", command = lambda row=row, col=col: assignNum(row,col))
        else:
            btn = Button(mainFrame, text = str(matrixPrime[i][j]), state="disabled", bd= 1, width= 5, height =2,  fg="black")

        # Store all buttons in a list
        allButtons.append(btn)

        subrow, subcol = divmod(j, 3)
        # The button is placed in the matrix, in position i,j
        btn.grid(row= i, column=j,padx= colPadding, pady= rowPadding)                                                                    
        matrixPrime[i][j] = btn
        rowButtons.append(btn)
    sudokuButtons.append(rowButtons)



#Lable for bad news messages
lblResult = StringVar()
Label(root, text="", textvariable= lblResult, fg = "#f00aba").place(x=554, y= 257)

#Lable for good news messages
lblGood = StringVar()
Label(root, text="", textvariable= lblGood, fg = "green").place(x=550, y= 257)

# Disable buttons at the start of the game until user clicks 'new game'
disableSudoku()
disableUtilities()
disableLevels()





# Start the window
root.mainloop()