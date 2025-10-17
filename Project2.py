import random
import copy

class Board: 
    def __init__(self, scoreGiven, boardGiven):
        self.currentScore = scoreGiven
        self.queenArray = boardGiven

def createBoard(n): #generate a random board of size nxn
    newBoard = []
    for i in range(n):
        newBoard.append(random.randint(0,n-1))
    return newBoard

def checkScore(queenArray,n): #calculate the heuritic score of a given board
    hscore = 0
    for col, row in enumerate(queenArray): #all values on a given diagonal calculate the same value with these formulas
        upperDiagonal = row - col 
        lowerDiagonal = row - (n - col)
        for newCol in range(col + 1, n):
            newUpperDiagonal = queenArray[newCol] - newCol
            newLowerDiagonal = queenArray[newCol] - (n - newCol)
            #check if the two queens are in conflict on the row or either diagonal 
            if(row == queenArray[newCol] or upperDiagonal == newUpperDiagonal or lowerDiagonal == newLowerDiagonal):
                hscore += 1
    return hscore

def checkScoreOptimal(queenArray, n, currentScore, oldRow, movedCol): #calculate the heuritic score of a given board
    for col, row in enumerate(queenArray): #all values on a given diagonal calculate the same value with these formulas
        if col != movedCol:
            #scoring col values
            upperDiagonal = row - col 
            lowerDiagonal = row - (n - col)
            #old values
            upperDiagonalOld = oldRow - movedCol 
            lowerDiagonalOld = oldRow - (n - movedCol)
            #new values
            upperDiagonalNew = queenArray[movedCol] - movedCol 
            lowerDiagonalNew = queenArray[movedCol] - (n - movedCol)

            oldConflict = row == oldRow or upperDiagonal == upperDiagonalOld or lowerDiagonal == lowerDiagonalOld
            newConflict = row == queenArray[movedCol] or upperDiagonal == upperDiagonalNew or lowerDiagonal == lowerDiagonalNew
            
            if oldConflict and not newConflict:
                currentScore -= 1
            elif newConflict and not oldConflict:
                currentScore += 1
        #for newCol in range(col + 1, n):
            #newUpperDiagonal = queenArray[newCol] - newCol
            #newLowerDiagonal = queenArray[newCol] - (n - newCol)
            #check if the two queens are in conflict on the row or either diagonal 
            #if(row == queenArray[newCol] or upperDiagonal == newUpperDiagonal or lowerDiagonal == newLowerDiagonal):
                #hscore += 1
    return currentScore

def testScoreBase(queenArray, n, currentScore):
    newScore = currentScore
    tempArray = copy.deepcopy(queenArray)
    for col, row in enumerate(queenArray): #Row is where we are starting in the row
        newArray = copy.deepcopy(queenArray)
        for newRow in range(n):
            if(row != newRow): #Do not check the row that we are already in
                newArray[col] = newRow
                tempScore = checkScoreOptimal(newArray, n, currentScore, row, col)
                #tempScore = checkScore(newArray, n)
                if(tempScore < newScore):
                    newScore = tempScore
                    tempArray = copy.deepcopy(newArray)
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
                tempScore = checkScoreOptimal(newArray, n, currentScore, row, col)
                if tempScore < newScore:
                    newScore = tempScore
                    tempArray = copy.deepcopy(newArray)
                elif tempScore == currentScore:
                    sidewaysMoves.append(newArray)
    newBoard = Board(newScore, copy.deepcopy(tempArray))
    return newBoard, sidewaysMoves

def baseHillClimb(n):
    mainBoard = createBoard(n)
    print(mainBoard)
    currentScore = checkScore(mainBoard, n)
    if (currentScore == 0): #Checks if the board was perfect when generated (GOOD CODE)
        print("Board was perfect from the start!")
        return 0, True
    
    for i in range (1000): #The number of steps we will currently take in our hill climb before breaking
        result = testScoreBase(mainBoard, n, currentScore)
        print(result.queenArray)
        if(result.currentScore >= currentScore):
            print("No Solution Found (Hill Climb Stuck)")
            print(result.queenArray)
            print(result.currentScore)
            return i + 1, False
        if(result.currentScore == 0):
            print("Solution Found")
            print(result.queenArray)
            print(result.currentScore)
            return i + 1, True
        mainBoard = copy.deepcopy(result.queenArray)
        currentScore = result.currentScore

def sidewaysHillClimb(n):
    sidewaysCount = 0
    mainBoard = createBoard(n)
    print(mainBoard)
    currentScore = checkScore(mainBoard, n)
    if (currentScore == 0): #Checks if the board was perfect when generated (GOOD CODE)
        print("Board was perfect from the start!")
        return 0, True
    
    for i in range (1000): #The number of steps we will currently take in our hill climb before breaking
        result, sidewaysArray = testScoreSideways(mainBoard, n, currentScore)
        print(result.queenArray)
        if result.currentScore > currentScore or sidewaysCount == 10:
            print("No Solution Found (Hill Climb Stuck)")
            print(result.queenArray)
            print(result.currentScore)
            return i + 1, True
        elif result.currentScore == 0:
            print("Solution Found")
            print(result.queenArray)
            print(result.currentScore)
            return i + 1, True
        elif result.currentScore == currentScore:
            print(f"{sidewaysArray} sideways array list")
            if len(sidewaysArray) == 1:
                mainBoard = copy.deepcopy(sidewaysArray[0])
            else:
                mainBoard = copy.deepcopy(sidewaysArray[random.randint(0, len(sidewaysArray) - 1)])
            sidewaysCount += 1
            continue
        mainBoard = copy.deepcopy(result.queenArray)
        currentScore = result.currentScore
        sidewaysCount = 0

def baseHillClimbRestart(n, numOfRestarts, numOfSteps):
    numOfRestarts += 1
    mainBoard = createBoard(n)
    print(mainBoard)
    currentScore = checkScore(mainBoard, n)
    if (currentScore == 0): #Checks if the board was perfect when generated (GOOD CODE)
        print("Board was perfect from the start!")
        return numOfRestarts, numOfSteps
    
    for i in range (1000): #The number of steps we will currently take in our hill climb before breaking
        result = testScoreBase(mainBoard, n, currentScore)
        print(result.queenArray)
        print(f"{result.currentScore} h-score")
        print(f"{numOfRestarts} number of restarts")
        if(result.currentScore >= currentScore):
            return baseHillClimbRestart(n, numOfRestarts, numOfSteps + i + 1)
        if(result.currentScore == 0):
            print("Solution Found")
            return numOfRestarts, numOfSteps + i + 1
        print(result.queenArray)
        mainBoard = copy.deepcopy(result.queenArray)
        currentScore = result.currentScore

def sidewaysHillClimbRestart(n, numOfRestarts, numOfSteps):
    numOfRestarts += 1
    sidewaysCount = 0
    mainBoard = createBoard(n)
    print(mainBoard)
    currentScore = checkScore(mainBoard, n)
    if (currentScore == 0): #Checks if the board was perfect when generated (GOOD CODE)
        print("Board was perfect from the start!")
        return numOfRestarts, numOfSteps
    for i in range (1000): #The number of steps we will currently take in our hill climb before breaking
        result, sidewaysArray = testScoreSideways(mainBoard, n, currentScore)
        print(result.queenArray)
        print(f"{result.currentScore} h-score")
        print(f"{numOfRestarts} number of restarts")
        if result.currentScore > currentScore or sidewaysCount == 100:
            return sidewaysHillClimbRestart(n, numOfRestarts, numOfSteps + i + 1)
        elif result.currentScore == 0:
            print("Solution Found")
            return numOfRestarts, numOfSteps + i + 1
        elif result.currentScore == currentScore:
            mainBoard = copy.deepcopy(sidewaysArray[random.randint(0, len(sidewaysArray) - 1)])
            sidewaysCount += 1
            continue
        mainBoard = copy.deepcopy(result.queenArray)
        currentScore = result.currentScore
        sidewaysCount = 0


nSize = input("What size of N would you like? ")
solveMethod = input("What solution methodolgy would you like to use?\n" \
"                    1) Basic Hill Climb\n"
"                    2) Hill Climb with Sideways Moves\n" \
"                    3) Basic Hill Climb with Restart\n" \
"                    4) Hill Climb with Sideway Moves and restarts\n")
numOfLoops = input("how many times do you want to run this? ")

passes = []
fails = []
restarts = []
if solveMethod == "1":
    for i in range(int(numOfLoops)):
        numSteps, ifSucceeded = baseHillClimb(int(nSize))
        print(ifSucceeded)
        if ifSucceeded == True:
            passes.append(numSteps)
        else:
            fails.append(numSteps)
    if len(passes) != 0:
        print(f"{sum(passes)/len(passes)} average steps for success")
    if len(fails) != 0:
        print(f"{sum(fails)/len(fails)} average steps for fails")
elif solveMethod == "2":
    for i in range(int(numOfLoops)):
        numSteps, ifSucceeded = sidewaysHillClimb(int(nSize))
        print(ifSucceeded)
        if ifSucceeded == True:
            passes.append(numSteps)
        else:
            fails.append(numSteps)
    if len(passes) != 0:
        print(f"{sum(passes)/len(passes)} average steps for success")
    if len(fails) != 0:
        print(f"{sum(fails)/len(fails)} average steps for fails")
elif solveMethod == "3":
    for i in range(int(numOfLoops)):
        numRestarts, numSteps = baseHillClimbRestart(int(nSize), -1, 0)
        passes.append(numSteps)
        restarts.append(numRestarts)
    print(f"{sum(passes)/len(passes)} average steps for success")
    print(f"{sum(restarts)/len(restarts)} average restarts")
elif solveMethod == "4":
    for i in range(int(numOfLoops)):
        numRestarts, numSteps = sidewaysHillClimbRestart(int(nSize), -1, 0)
        passes.append(numSteps)
        restarts.append(numRestarts)
    print(f"{sum(passes)/len(passes)} average steps for success")
    print(f"{sum(restarts)/len(restarts)} average restarts")
else:
    print("you did not provide a proper argument of 1-4 run the program again")
