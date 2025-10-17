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

def testScoreBase(queenArray, n, currentScore):
    newScore = currentScore
    tempArray = copy.deepcopy(queenArray)
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
    return newBoard

def testScoreSideways(queenArray, n, currentScore):
    newScore = currentScore
    sidewaysMoves = []
    tempArray = copy.deepcopy(queenArray)
    for col, row in enumerate(queenArray): #Row is where we are starting in the row
        newArray = copy.deepcopy(queenArray)
        for newRow in range(n):
            if(row != newRow): #Do not check the row that we are already in
                newArray[col] = newRow
                tempScore = checkScore(newArray, n)
                if tempScore < newScore:
                    newScore = tempScore
                    tempArray = copy.deepcopy(newArray)
                elif tempScore == currentScore:
                    sidewaysMoves.append(newArray)

        # queenArray = copy.deepcopy(tempArray)
    newBoard = Board(newScore, copy.deepcopy(tempArray))
    return newBoard, sidewaysMoves

def baseHillClimb(n):
    # mainBoard = createBoard(n)
    mainBoard = createBoard(n)
    print(mainBoard)
    currentScore = checkScore(mainBoard, n)
    if (currentScore == 0): #Checks if the board was perfect when generated (GOOD CODE)
        print("Board was perfect from the start!")
        return
    
    for i in range (1000): #The number of steps we will currently take in our hill climb before breaking
        result = testScoreBase(mainBoard, n, currentScore)
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

def sidewaysHillClimb(n):
    sidewaysCount = 0
    # mainBoard = createBoard(n)
    mainBoard = createBoard(n)
    print(mainBoard)
    currentScore = checkScore(mainBoard, n)
    if (currentScore == 0): #Checks if the board was perfect when generated (GOOD CODE)
        print("Board was perfect from the start!")
        return
    
    for i in range (1000): #The number of steps we will currently take in our hill climb before breaking
        result, sidewaysArray = testScoreSideways(mainBoard, n, currentScore)
        if result.currentScore > currentScore or sidewaysCount == 100:
            print("No Solution Found (Hill Climb Stuck)")
            print(result.queenArray)
            print(result.currentScore)
            return
        elif result.currentScore == 0:
            print("Solution Found")
            print(result.queenArray)
            print(result.currentScore)
            return
        elif result.currentScore == currentScore:
            mainBoard = copy.deepcopy(sidewaysArray[random.randint(0, len(sidewaysArray) - 1)])
            sidewaysCount += 1
            continue
        # else:
        #     print("ERROR")
        #     print(result.queenArray)
        #     print(result.currentScore)
        print(result.queenArray)
        mainBoard = copy.deepcopy(result.queenArray)
        currentScore = result.currentScore
        sidewaysCount = 0

def baseHillClimbRestart(n, numOfRestarts):
    numOfRestarts += 1
    # mainBoard = createBoard(n)
    mainBoard = createBoard(n)
    print(mainBoard)
    currentScore = checkScore(mainBoard, n)
    if (currentScore == 0): #Checks if the board was perfect when generated (GOOD CODE)
        print("Board was perfect from the start!")
        return
    
    for i in range (1000): #The number of steps we will currently take in our hill climb before breaking
        result = testScoreBase(mainBoard, n, currentScore)
        if(result.currentScore >= currentScore):
            print("No Solution Found (Hill Climb Stuck)")
            print(result.queenArray)
            print(result.currentScore)
            return baseHillClimbRestart(numOfRestarts)
        if(result.currentScore == 0):
            print("Solution Found")
            print(result.queenArray)
            print(result.currentScore)
            print(numOfRestarts)
            return
        # else:
        #     print("ERROR")
        #     print(result.queenArray)
        #     print(result.currentScore)
        print(result.queenArray)
        mainBoard = copy.deepcopy(result.queenArray)
        currentScore = result.currentScore

def sidewaysHillClimbRestart(n, numOfRestarts):
    numOfRestarts += 1
    sidewaysCount = 0
    # mainBoard = createBoard(n)
    mainBoard = createBoard(n)
    print(mainBoard)
    currentScore = checkScore(mainBoard, n)
    if (currentScore == 0): #Checks if the board was perfect when generated (GOOD CODE)
        print("Board was perfect from the start!")
        return
    
    for i in range (1000): #The number of steps we will currently take in our hill climb before breaking
        result, sidewaysArray = testScoreSideways(mainBoard, n, currentScore)
        if result.currentScore > currentScore or sidewaysCount == 100:
            print("No Solution Found (Hill Climb Stuck)")
            print(result.queenArray)
            print(result.currentScore)
            return sidewaysHillClimbRestart(numOfRestarts)
        elif result.currentScore == 0:
            print("Solution Found")
            print(result.queenArray)
            print(result.currentScore)
            print(numOfRestarts)
            return
        elif result.currentScore == currentScore:
            mainBoard = copy.deepcopy(sidewaysArray[random.randint(0, len(sidewaysArray) - 1)])
            sidewaysCount += 1
            continue
        # else:
        #     print("ERROR")
        #     print(result.queenArray)
        #     print(result.currentScore)
        print(result.queenArray)
        mainBoard = copy.deepcopy(result.queenArray)
        currentScore = result.currentScore
        sidewaysCount = 0


nSize = input("What size of N would you like? ")
solveMethod = input("What solution methodolgy would you like to use?\n" \
"                    1) Basic Hill Climb\n"
"                    2) Hill Climb with Sideways Moves\n" \
"                    3) Basic Hill Climb with Restart\n" \
"                    4) Hill Climb with Sideway Moves and restarts\n")

if solveMethod == "1":
    baseHillClimb(int(nSize))
elif solveMethod == "2":
    sidewaysHillClimb(int(nSize))
elif solveMethod == "3":
    baseHillClimbRestart(int(nSize), -1)
elif solveMethod == "4":
    sidewaysHillClimbRestart(int(nSize), -1)
else:
    print("you did not provide a proper argument of 1-4 run the program again")
#sidewaysHillClimb()