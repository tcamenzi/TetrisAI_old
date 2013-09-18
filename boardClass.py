from activePiece import ActivePiece
from getAllConfigurations import getAllConfigurations
from assignScores import getBest, getScore
from getBestBoardFast import getBestMovesFast
import pdb
import time
import sys
##0,0 is the top left of the board

##This class keeps track of the board state.
##It supplies the client functions to move/rotate a piece,
##and also keeps track of score, whether/not you've lost, and
##creates new active pieces as needed
class  board(object):
    numCols = 0 #number of rows and columns in the grid
    numRows = 0
    rowpixWidth = 0 #in pixels; store this for the draw function
    colpixWidth = 0
    board = 0 ##will be a 2d array of on/off filled/not [static squares only]
    hasLost = False #set to true when you lose
    piece = 0 #will hold a class for the currently active piece
    numRowsCleared = 0 #Increment upon clearing a row
    numRotations = 0
    numLeft = 0
    numRight = 0

    def __init__(self, rows, cols, size):
        print "initializing", rows, cols, size
        self.numCols = cols
        self.numRows = rows
        self.rowpixWidth = size[1] / rows
        self.colpixWidth = size[0] / cols
        self.board = [[0]*cols for x in xrange(rows) ] #2d grid board[row][col]
        self.piece = ActivePiece( cols / 2, 0 ) ##create the class to start in the middle/top of the board
        

    def movePieceLeft(self): ##Move the piece left if available. Else, don't move the piece.
        #print "moving the piece left"
        self.piece.moveLeft()
        if self.isConflict(): ##undo, can't move there
            self.piece.moveRight()

    def movePieceRight(self): ##move the active piece right if space is available. 
        #print "moving the piece right"
        self.piece.moveRight()
        if self.isConflict(): ##undo, can't move there
            self.piece.moveLeft()

    def movePieceDown(self): ##Move down if space is available. If no space, then add this piece to the static grid & get a new active piece
        #print "moving the piece down"
        self.piece.moveDown()
        if self.isConflict(): ##undo, can't move there
            self.piece.moveUp()
            start = time.clock()
            self.hitBottom()
            #print "end hit bottom", time.clock()-start

    def rotatePiece(self): ##rotate the current piece if space
        #print "rotating"
        self.piece.rotate()
        if self.isConflict(): ##undo, can't rotate
            self.piece.rotate() ##3 rights make a left
            self.piece.rotate()
            self.piece.rotate()

    def hitBottom(self): ##called once the current piece must be added to the static board.
##        raw_input()
        for coord in self.piece.relativePoints: ##add each square to the board
            x = self.piece.centerx + coord.x
            y = self.piece.centery + coord.y
            if y<0: ##you're past the top of the board when you hit the bottom; you've filled up the board and lose.
                self.hasLost = True
            self.board[y][x] = 1
        self.checkFill() #clear out any filled rows
##        print "\n\n\n============Below is the output for the current board==="
##        getScore(self.board)
        self.piece = ActivePiece( self.numCols / 2, 0 ) #new piece starts top & center
        #start = time.clock()
##        allBoards = getAllConfigurations( self )
##        print "end get all configs", time.clock()-start
##        start = time.clock()
##        bestBoard = getBest(allBoards)
        bestBoard = getBestMovesFast( self )
        #print "end getbest", time.clock()-start
        if bestBoard==0:
            print "Game Over. NumCleared: ", self.numRowsCleared
            self.hasLost = True
            return
            #sys.exit()
        self.numRotations = bestBoard.numRotate 
        self.numLeft = bestBoard.numLeft
        self.numRight = bestBoard.numRight
        #print "rotate by ", self.numRotations, "shift left by ", self.numLeft, "shift right by ", self.numRight
        ##pdb.set_trace()

    def checkFill(self): ##filter out all rows that are filled
        self.board = [row for row in self.board if len(row)!=sum(row)] #filter out all rows
        removed = self.numRows - len(self.board)
        self.numRowsCleared += removed #keep track of score
        #print "Number of rows cleared: ", self.numRowsCleared
        self.board = [[0]*self.numCols for x in xrange(removed) ] + self.board #add needed empty rows to the top of the grid

    def isConflict(self):
        ##returns true if there is a conflict, ie either the piece is out of
        ##bounds or the piece overlaps with existing squares
        for coord in self.piece.relativePoints: #check each square for conlicts
            x = self.piece.centerx + coord.x
            y = self.piece.centery + coord.y
            if (not self.inBounds( x, y )) or (y>=0 and self.board[y][x] ==1):
                return True #either of bounds, or hit an overlapping square
        return False #each square cleared, so the fxn clears

    def inBounds(self, x, y): #true if in bounds. No restriction for being off the top of the grid, because pieces start partially past the top.
        return (x>=0) and (x < len(self.board[0])) and (y < len(self.board)) 

    def printBoard(self):
        for row in self.board:
            print row
