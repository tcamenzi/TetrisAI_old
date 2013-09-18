from assignScores import constantInit
import win32api, win32con, ImageGrab
from boardClass import board
from draw import drawBoard
from getRandomPiece import writeToFile
from getPrintScreen import ExtractScreenData
from activePiece import coord
from activePiece import ActivePiece
from getBestBoardFast import getBestMovesFast
import time
import pdb
import os

def setType( name ): #we only care if it's a square or not
    if name=="SQUARE":
        return 0
    if name == "BackL":
        return 4
    if name=="FrontL":
        return 3
    if name=="BackZ":
        return 6
    if name=="FrontZ":
        return 5
    if name=="T":
        return 2
    if name=="LINE":
        return 1
    print 'error in settype'

def setRelativePoints( points ):
    coords = []
    for point in points:
        coords.append( coord(point[1], point[0]) )
    return coords

def pushButtons( bestBoard ):
    if bestBoard == 0: ##near top / collision
        return
##    print 'sleep 1 s'
##    time.sleep(2)
    SLEEP = .05
    nummoves = bestBoard.numRotate + bestBoard.numLeft + bestBoard.numRight
    for a in range( bestBoard.numRotate):
        print 'rotate'
        ##rotate
        win32api.keybd_event( 0x26, 0 ) #up
        time.sleep(SLEEP)
    for a in range( bestBoard.numLeft):
        print 'left'
        ##left
        win32api.keybd_event( 0x25, 0 ) #left
        time.sleep(SLEEP)
    for a in range( bestBoard.numRight):
        print 'right'
        ##right
        win32api.keybd_event( 0x27, 0 ) #right
        time.sleep(SLEEP)

    if nummoves > 0:
        for a in range(3): #push it down
            print 'down'
            win32api.keybd_event(0x28, 0,0,0)
            time.sleep(SLEEP)
            win32api.keybd_event(0x28,0,2,0)
            time.sleep(SLEEP)
        
NUMROWS = 18
NUMCOLS = 10
size = [1,1] #doesn't matter for this
board = board( NUMROWS, NUMCOLS, size)
bp = 20
sp = 1
hp = 0
nahbp = 1
tp = 1
constantInit(bp, sp, hp,nahbp,tp)
raw_input("hit enter before a 5 second grace period")
time.sleep(5)

def printLastImageNumber():
    count = 1
    while(os.path.isfile("printscreens/"+str(count)+".jpg")):
        count+=1
    print "The last file number is ", count-1, "\n"
    
while True:
    print 'start extract'
    data = ExtractScreenData()
    print 'end extract'
    if data[2] !=0: #there's an active piece in the top
        print "time to navigate"
        board.board = data[1]
        active = ActivePiece(0,0)
        active.type = setType( data[2] )
        active.centery = data[3][0][0]
        active.centerx = data[3][0][1]
        #print "center x and y", active.centerx, active.centery
        active.relativePoints = setRelativePoints( data[3][1] )#coord class
        board.piece = active
        bestBoard = getBestMovesFast( board )
        #pdb.set_trace()
        
        #######print all data
        print "\nboard"
        for row in board.board:
            print row
        print "\nactive piece"
        print "type", board.piece.type
        print "center x y ", board.piece.centerx, board.piece.centery
        print "relative points: "
        for coordi in board.piece.relativePoints:
            print coordi.x, coordi.y
        print "\nbest moves"
        if bestBoard!=0:
            print "best board rotate left rigth", bestBoard.numRotate, bestBoard.numLeft, bestBoard.numRight
        else:
            print "bestboard is 0"
        print "data with active piece", data[0]
        printLastImageNumber()
##        pdb.set_trace()
##        raw_input("press enter to continue after a 2 second pause")
##        time.sleep(2)
##        
        ####done printing data
        
        pushButtons( bestBoard )
        
