from boardState import BoardState
import copy

def getAllDown(boardClass, worklist, rotation, movesLeft, movesRight):
##    print "getting all down. Rotation movesleft movesright is: ", rotation, movesLeft, movesRight
    workingBoard = copy.deepcopy(boardClass)
    movesDown = 0
    while(not workingBoard.isConflict()):
        workingBoard.piece.moveDown()
        movesDown+=1
    ##movesDown now has the number of moves needed to reach a conflict.
    ##we want to move the piece until just *before* there is a conflict and add it
    ##So... probably move up by one and then add it. This will never go too high because
    ## you always start in a non-conflict zone [otherwise this fxn would not get called]
    workingBoard.piece.moveUp()
    movesDown-=1

    ##Add each part of the activePiece to the board
    for coord in workingBoard.piece.relativePoints:
        x = coord.x + workingBoard.piece.centerx
        y = coord.y + workingBoard.piece.centery
        workingBoard.board[y][x] = 1
    ##Add an independent copy to the worklist
    worklist.append( BoardState( copy.deepcopy( workingBoard.board), movesLeft, movesRight, movesDown, rotation) )
    
def getAllWithinRotation( boardClass, worklist, rotation):
##    print "getting all within the rotation " , rotation
##    print "piece is ", boardClass.piece.relativePoints
    workingBoard = copy.deepcopy(boardClass)
    movesLeft = 0
    movesRight = 0
    while(not workingBoard.isConflict() ): ##scoot left as far as possible
        getAllDown(workingBoard, worklist, rotation, movesLeft, movesRight)
        workingBoard.piece.moveLeft()
        movesLeft +=1
    ##reset to one right of center
    workingBoard = copy.deepcopy(boardClass)
    workingBoard.piece.moveRight()
    movesLeft = 0
    movesRight = 1
    while( not workingBoard.isConflict()): ##scoot right as far as possible
        getAllDown(workingBoard, worklist, rotation, movesLeft, movesRight)
        workingBoard.piece.moveRight()
        movesRight +=1
        
##Input: a board class, ie a board and state. This original is read-only.
##Output: all possible boards & sequences of moves to get there

def getAllConfigurations( boardClass ):
    #print "getting all configurations for the board"
##    boardClass.printBoard()
    worklist = []
    if boardClass.isConflict():
        return worklist
    workingBoard = copy.deepcopy(boardClass)
    workingBoard.piece.moveDown() ##for now a hack to make sure it's not 
    workingBoard.piece.moveDown() ##cut off past the top of the screen.
    for rotation in range(4):
        if not workingBoard.isConflict():
            getAllWithinRotation( workingBoard, worklist, rotation)
        workingBoard.piece.rotate()
    #print "done getting configurations"
    return worklist

    
