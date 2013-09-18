from assignScores import getScore

def getRotationsNeeded(boardClass):
    temp = boardClass.piece.type
    if temp == 0: #square
        return 1 #1 rotation is enough, ie 1 run of for loop
    
    if temp==1: #straight
        return 2
    
    if temp == 2: #T
        return 4 #all 4 rotations are unique
    
    if temp==3: #L
        return 4 #all 4 rotations unique

    if temp==4: #L backwards
        return 4

    if temp==5: #S
        return 2 #symmetric 180

    if temp==6: #S backwards
        return 2 ##symmetric 180

    
def addToBoard( boardClass):
    for coord in boardClass.piece.relativePoints: ##add each square to the board
        x = boardClass.piece.centerx + coord.x
        y = boardClass.piece.centery + coord.y
        boardClass.board[y][x] = 1
        
def removeFromBoard( boardClass):
    for coord in boardClass.piece.relativePoints: ##add each square to the board
        x = boardClass.piece.centerx + coord.x
        y = boardClass.piece.centery + coord.y
        if boardClass.board[y][x]==0:
            print "uh oh it's not working in getBestBoardFast.py..."
        boardClass.board[y][x] = 0

class MoveData:
    numRotate = 0
    numLeft = 0
    numRight = 0
    def __init__(self, rotate, left, right):
        self.numRotate = rotate
        self.numLeft = left
        self.numRight = right


def getBestMovesFast( boardClass ):
    #print"\n\n\n New board examining"
    boardClass.piece.moveDown()
    boardClass.piece.moveDown()
    if( boardClass.isConflict()):
        boardClass.piece.moveUp()
        boardClass.piece.moveUp()
        return 0 ##hit conflict early, you've lost
    addToBoard( boardClass) ##Add the active piece to the board
    bestScore = getScore( boardClass.board )
    bestMoves = MoveData(0,0,0) #0 rotations, 0 left, 0 right
    removeFromBoard( boardClass ) #remove the active piece from the board

    rotationsNeeded = getRotationsNeeded(boardClass)

    for rotation in range(rotationsNeeded):
        if not boardClass.isConflict():
            movesLeft = 0
            while( not boardClass.isConflict() ): ##do each shift left

                ######Code for a single down/score/back up
                movesDown = 0
                while( not boardClass.isConflict() ): ##push down until collision
                    boardClass.piece.moveDown()
                    movesDown+=1
                ##now a collision; reverse by 1
                boardClass.piece.moveUp()
                movesDown-=1
                ##now in place at the bottom
                addToBoard( boardClass )
                temp = getScore(boardClass.board)
                removeFromBoard( boardClass)
                if temp < bestScore:
                    #print "THE ABOVE BOARD WAS THE BEST"
                    bestScore = temp
                    bestMoves = MoveData(rotation, movesLeft, 0) #no moves right
                ##move back up to where you were before
                for up in range(movesDown):
                    boardClass.piece.moveUp()
                ################Now back at the top where it started. Continue leftshifts
                boardClass.piece.moveLeft()
                movesLeft+=1

                
            ###########Tried moving left, now there is conflict! Can't go further left, move to center
            for left in range(movesLeft):
                boardClass.piece.moveRight()


            ######################Now repeat the above for rightshifts
            movesRight = 0
            while( not boardClass.isConflict() ): ##do each shift right
                
                ###code for a single down/score/back up
                movesDown = 0
                while(not boardClass.isConflict()):
                    boardClass.piece.moveDown()
                    movesDown+=1
                ##now a collision, reverse by 1
                boardClass.piece.moveUp()
                movesDown-=1
                ##now in place at the bottom
                addToBoard( boardClass)
                temp = getScore( boardClass.board)
                ##debugging only
                removeFromBoard( boardClass)
                if temp < bestScore:
                    #print "THE ABOVE BOARD WAS THE BEST"
                    bestScore = temp
                    bestMoves = MoveData( rotation, 0, movesRight)
                ##move back up to where yo were before
                for up in range(movesDown):
                    boardClass.piece.moveUp()
                ###############now at top where started. convinue right shifts
                boardClass.piece.moveRight()
                movesRight+=1
                
            ######MOved all the way right. can't go further, back to center
            for right in range(movesRight):
                boardClass.piece.moveLeft()

        ############Ok. moved left/right/back to center. time for the next rotation...
        boardClass.piece.rotate()
        
    
    ###############done with all rotations!!            

    for rotation in range( 4 - rotationsNeeded):
        boardClass.piece.rotate() ##total of 4 rotations

    ##had moved down two earlier; now move two up so it's in the same spot.
    boardClass.piece.moveUp()
    boardClass.piece.moveUp()
    return bestMoves
