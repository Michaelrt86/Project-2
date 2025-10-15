import random

def createBoard(n):
    newBoard = []
    for i in range(n):
        newBoard[i] = random.randint(0,n-1)
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
    print(counter)
    return hscore

def testScore(queenArray, n, currentScore):
    newScore = currentScore
    for col, row in enumerate(queenArray): #Row is where we are starting in the row
        newArray = queenArray
        for newRow in range(n):
            if(row != newRow): #Do not check the row that we are already in
                newArray[col] = newRow
                tempScore = checkScore(newArray, n)
                if(tempScore < currentScore):
                    newScore = tempScore
print(checkScore([0,0,3,3], 4))