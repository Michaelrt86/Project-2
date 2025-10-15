import random
import copy

class Board: 
    def __init__(self, scoreGiven, boardGiven):
        self.currentScore = scoreGiven
        self.queenArray = boardGiven

def createBoard(n):
    newBoard = []
    for i in range(n):
        newBoard.append(random.randint(0,n-1))
    return newBoard

def checkScore(queenArray,n):
    hscore = 0
    counter = 0
    for col, row in enumerate(queenArray):
        upperDiagonal = row - col
        lowerDiagonal = row - (n - col)
        for newCol in range(col + 1, n):
            newUpperDiagonal = queenArray[newCol] - newCol
            newLowerDiagonal = queenArray[newCol] - (n - newCol)
            counter += 1
        
            if(row == queenArray[newCol] or upperDiagonal == newUpperDiagonal or lowerDiagonal == newLowerDiagonal):
                hscore += 1
    return hscore

def testScore(queenArray, n, currentScore):
    newScore = currentScore
    copy.deepcopy(queenArray)
    for col, row in enumerate(queenArray): #Row is where we are starting in the row
        newArray = copy.deepcopy(queenArray)
        for newRow in range(n):
            if(row != newRow): #Do not check the row that we are already in
                newArray[col] = newRow
                tempScore = checkScore(newArray, n)
                if(tempScore < newScore):
                    newScore = tempScore
                    tempArray = copy.deepcopy(newArray)

        # queenArray = copy.deepcopy(tempArray)
    newBoard = Board(newScore, copy.deepcopy(tempArray))
    print(tempArray)
    return newBoard
    
def Main():
    n = 4
    # mainBoard = createBoard(n)
    mainBoard = [2,1,2,1]
    currentScore = checkScore(mainBoard, n)
    if (currentScore == 0): #Checks if the board was perfect when generated (GOOD CODE)
        print("Board was perfect from the start!")
        return
    
    for i in range (1000): #The number of steps we will currently take in our hill climb before breaking
        result = testScore(mainBoard, n, currentScore)
        if(result.currentScore >= currentScore):
            print("No Solution Found (Hill Climb Stuck)")
            print(result.queenArray)
            print(result.currentScore)
            return
        if(result.currentScore == 0):
            print("Solution Found")
            print(result.queenArray)
            print(result.currentScore)
            return
        # else:
        #     print("ERROR")
        #     print(result.queenArray)
        #     print(result.currentScore)
        print(result.queenArray)
        mainBoard = copy.deepcopy(result.queenArray)
        currentScore = result.currentScore

Main()