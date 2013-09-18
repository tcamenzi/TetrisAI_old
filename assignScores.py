##Changes to original:
#squaring the surface tension now

BURIED_PENALTY = 0
SURFACE_PENALTY = 0
HEIGHT_PENALTY = 0
NUMABOVE_HIGHESTBURIED_PENALTY = 0
TRENCH_PENALTY = 0

import time

def constantInit( bp, sp, hp, nahbp, tp):
    global BURIED_PENALTY
    global SURFACE_PENALTY
    global HEIGHT_PENALTY
    global NUMABOVE_HIGHESTBURIED_PENALTY
    global TRENCH_PENALTY
    BURIED_PENALTY = bp
    SURFACE_PENALTY = sp
    HEIGHT_PENALTY = hp
    NUMABOVE_HIGHESTBURIED_PENALTY = nahbp
    TRENCH_PENALTY = tp
    
def getSurfaceTension( grid, highestBuriedIndex ):

    #####Get the height of the columns
    heights = [0]*len(grid[0]) #store the height of each column, ie index of 1st 1
    for colindex in range(len(grid[0])): #for each column:
        for rowindex in range(len(grid)): #walk down that column until a 1 is reached
            if grid[rowindex][colindex] == 1: 
                heights[colindex] = len(grid) - rowindex #the height of the column
                break

    ##Get the number above the highest buried
    numAboveHighestBuried = 0
    if highestBuriedIndex < len(grid): #otherwise there are none buried, return the default ie 0
        for col in range(len(grid[0])): #find highest for each column
            if grid[highestBuriedIndex][col]==0: #potentially a buried square
                difference = heights[col] - (len(grid)-highestBuriedIndex) #negative if unburied, positive if buried
                if difference>numAboveHighestBuried: #store the max
                    numAboveHighestBuried = difference

    ###Get the trenches
    numTrenches = 0 ##not actually the #, but actually the depth of each squared
    for index in range(1, len(heights)-1): ##do all the middle ones first
        left = heights[index-1] - heights[index]
        right = heights[index+1] - heights[index]
        if left > 0 and right > 0: ##left & right sides are taller so it's truly a trench
            numTrenches += min(left, right)**2 ##the lower boundary determines trench depth. We take the depth & square it & add
    ##Take care of the leftmost side
    sideTrench = heights[1] - heights[0]
    if sideTrench > 0:
        numTrenches += sideTrench **2
    sideTrench = heights[-2] - heights[-1] ##the 2nd to right minus rightmost
    if sideTrench > 0:
        numTrenches += sideTrench**2

    ##Get the 'surface tension' or the height differences between columns                
    total = 0
    for index in range(len(heights) - 1):
        total+= (abs( heights[index] - heights[index+1] ))**2
    return total, numAboveHighestBuried, numTrenches

def getBuried( grid ):
    highestBuriedIndex = len(grid) ##1st buried is past end of grid, ie none buried
    numBuried = 0
    for colindex in range(len(grid[0])): #for each column:
        isCovered = False #still above the start 
        for rowindex in range(len(grid)): ##walk down each column until a 1 is reached
            if grid[rowindex][colindex]==1:
                isCovered = True ##you're now in an overhang
            if isCovered and grid[rowindex][colindex]==0: #buried one
                numBuried +=1
                if rowindex < highestBuriedIndex: ##lowest index = highest buried; starts at 0
                    highestBuriedIndex = rowindex
    return numBuried, highestBuriedIndex

def checkFill(grid): ##filter out all rows that are filled
    numRows = len(grid)
    numCols = len(grid[0])
    grid = [row for row in grid if len(row)!=sum(row)] #filter out all rows
    removed = numRows - len(grid)
    grid = [[0]*numCols for x in xrange(removed) ] + grid #add needed empty rows to the top of the grid
    return grid

def getHeight(grid):
    total = 0
    currHeight = len(grid)
    for row in grid:
        total+=sum(row)*currHeight
        currHeight-=1
    return total

def getScore( grid ):

    Height = getHeight(grid) #Higher blocks = more penalty.
    ##Be sure to get the height *before* deleting all the rows / checkfill
    grid = checkFill(grid)
    global BURIED_PENALTY
    global SURFACE_PENALTY
    global HEIGHT_PENALTY
    global NUMABOVE_HIGHESTBURIED_PENALTY
    global TRENCH_PENALTY
##    BURIED_PENALTY = 21
##    SURFACE_PENALTY = 1
##    HEIGHT_PENALTY = 0
    
    
    NumBuried, highestBuriedIndex = getBuried(grid)
    SurfaceTension, numAboveHighestBuried, numTrenches = getSurfaceTension(grid, highestBuriedIndex) ##must come below getBuried
##    print "The number of trenches is: ", numTrenches
    #print "numAboveHighestBuried is: ", numAboveHighestBuried
    #print Height*HEIGHT_PENALTY
    return BURIED_PENALTY*NumBuried + SURFACE_PENALTY*SurfaceTension +Height*HEIGHT_PENALTY + numAboveHighestBuried * NUMABOVE_HIGHESTBURIED_PENALTY+ numTrenches * TRENCH_PENALTY

def getBest( allBoards ):
##    print "start getBest"
    if len(allBoards) == 0:
        print "THERE ARE NO BOARDS HERE IN ASSIGNSCORES.PY, THIS IS BAD"
        return 0
    bestScore = getScore( allBoards[0].board )
    bestBoard = allBoards[0]
    
    for board in allBoards:
##        board.board = checkFill( board.board )
        score = getScore( board.board)
        if score < bestScore:
            bestScore = score
            bestBoard = board
            
##    print "the best board is: "
##    for row in bestBoard.board:
##        print row
##    print "end getBest"
    return bestBoard
