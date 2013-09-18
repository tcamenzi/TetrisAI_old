import win32api, win32con, ImageGrab
from scipy.ndimage import filters
from PIL import Image
from pylab import *
from numpy import *
import pdb
import random
import os.path

def get4Adjacent( point, pointSet):
    r = point[0]
    c = point[1]
    total = 0
    total+= (r+1,c) in pointSet
    total+= (r-1,c) in pointSet
    total+= (r, c-1) in pointSet
    total+= (r, c+1) in pointSet
    return total

def get8Adjacent(point, pointSet):
    total = get4Adjacent(point, pointSet)
    r = point[0]
    c = point[1]
    total+=(r+1, c+1) in pointSet
    total+=(r+1, c-1) in pointSet
    total+=(r-1, c+1) in pointSet
    total+=(r-1, c-1) in pointSet
    return total

def getL( pointSet ):
    one = 0
    end = 0
    for point in pointSet: #find the one point
        if get8Adjacent(point, pointSet)==1:
            one = point
            break
    for point in pointSet: #find the poitn oppostive from 1, ie diff x,y coords
        if point[0]!=one[0] and point[1]!=one[1]:
            end = point
            break
        
    r = end[0] - one[0] #difference in row; normalize to 0,0
    c = end[1] - one[1] #difference in col
    count = 0
    count+= (r>0) #1st num positive
    count+= (c>0) #2nd num positive
    count+= (abs(r)==1)#1st num a one
    if count%2 == 1: #left L will have an odd number true
        return "BackL"
    else:
        return "FrontL"

def getZ( pointSet ):
    end = 0
    start = 0
    for point in pointSet:
        if get8Adjacent(point, pointSet):
            if start==0:
                start = point
            else:
                end = point
    r = end[0] - start[0]
    c = end[1] - start[1]
    count = 0
    count+= (r > 0)
    count+=(c>0)
    count+= ( abs(r)==1)
    if count%2 == 1:
        return "BackZ"
    else:
        return "FrontZ"
    
def getActivePieceType( points ):
    if points==0:
        return 0
    pointSet = set([])
    for item in points:
        pointSet.add(tuple(item))
        
    total = 0
    for point in points:
        temp = get4Adjacent( point, pointSet ) #returns no. of squares adj to point in points
        if temp==3:
            return 'T'
        total+=temp
    if total==8: #2 adj each totals 8, square
        return 'SQUARE'

    total = 0
    for point in points:
        temp = get8Adjacent(point, pointSet) #returns no of 8 adj
        total+=temp
    if total==6:
        return "LINE"
    if total==8: #must be an L
        return getL( pointSet )
    if total==10: #must be an S
        return getZ( pointSet )
    print "error in getactivepiecetype"

def ActivePieceRelative( points, ptype ):
    if points==0:
        return 0
    pointSet = set([])
    for item in points:
        pointSet.add(tuple(item))

    ###################Set the center point
    center = 0
    #ones with special cases: line, Ls. these are 'flexible' rotators    
    if ptype == "SQUARE" or ptype == "T" or ptype == "FrontZ" or ptype == "BackZ": 
        for point in points:
            if get4Adjacent(point, pointSet) >= 2:
                center = point
                break
            
    if ptype=="LINE":
        first = 0
        second = 0
        for point in points:
            if get4Adjacent(point, pointSet) >=2:
                if first==0:
                    first = point
                else:
                    second = point
        center = 0
        if sum(first) < sum(second):
            center = first
        else:
            center = second

    if ptype=="FrontL" or ptype == "BackL":
        first = 0
        second = 0
        for point in points:
            if get4Adjacent(point, pointSet) >=2:
                if first==0:
                    first = point
                else:
                    second = point
        dx = first[0] - second[0]
        dy = first[1] - second[1]
        firstabove = (  first[0] + dx, first[1] + dy)
        firstbelow = (  first[1] - dx, first[1] - dy)
        if firstabove in pointSet and firstbelow in pointSet:
            center = first
        else:
            center = second

    #########################Center point chosen, now relativePoints
    relativePoints = []
    for point in points:
        r = point[0] - center[0]
        c = point[1] - center[1]
        relativePoints.append([r,c])
    return [center, relativePoints]

def writeToFile(im):
    count = 1
    while(os.path.isfile("printscreens/"+str(count)+".jpg")):
        count+=1
    im.save("printscreens/"+str(count)+".jpg")
    
def getImageArray():
    im = None
    while im == None:
        #for a in range(10): ##see if this fixes an earlier bug of not getting most current printscreen
         #   win32api.keybd_event(win32con.VK_SNAPSHOT, 0) #set to 1 to capture only python shell screen;
        #0 is whole printscreen like normal
        im = ImageGrab.grab()
    writeToFile(im)
    return array(im)
    #return array( Image.open('printscreens/22.jpg'))

def isClose( pixel):
    RED_BORDER_TARGET = 105
    GREEN_BORDER_TARGET = 120
    BLUE_BORDER_TARGET = 150
    CUTOFF = 90 #change back to 45
    rdif = abs(pixel[0] - RED_BORDER_TARGET)
    gdif = abs(pixel[1] - GREEN_BORDER_TARGET)
    bdif = abs(pixel[2] - BLUE_BORDER_TARGET)
    if (rdif+gdif+bdif) < CUTOFF:
        return True
    else:
        return False
    
def getVerticalBars(imarray):
    BOX_HEIGHT = 550 ##it's more like 610 but close enough
    allBars = []
    height = len(imarray)
    rowIndex = height / 2 ##for now just do for one row
    for colIndex in range(len(imarray[0])): ##each column
        if isClose( imarray[rowIndex][colIndex]):
            topIndex = rowIndex
            while isClose( imarray[topIndex-10][colIndex]):
                topIndex-=10
            bottomIndex = rowIndex
            while isClose( imarray[bottomIndex+10][colIndex]):
                bottomIndex+=10
            if (bottomIndex - topIndex) > BOX_HEIGHT:
                allBars.append([topIndex, bottomIndex, colIndex])
    return allBars

def plotVerticalBars( vertical, imarray):
    imshow(imarray, interpolation = "nearest")
    x = []
    y = []
    for sequence in vertical:
        x.append(sequence[2]) #x coord of top point
        y.append( sequence[0]) #y coord of top point
        x.append(sequence[2]) #x coord of bottom point
        y.append(sequence[1]) #y coord of bottom point
    plot(x, y, 'r*')
    show()

##def getColumns(vertical):
##    columns = []
##    index = 0
##    while index < len(vertical): ##for each elem in vertical
##        curr = vertical[index] ##see how many columns are adjacent to the curr column
##        numAdjacent = 0
##        ##see how many blocks are within 5 columns of the current one
##        while (index < len(vertical)) and (abs( vertical[index][2] - curr[2]) < 5):
##            index+=1
##            numAdjacent+=1
##        ##numadj = 1 means lonely. need at least 2 more.
##        if numAdjacent >= 3:
##            columns.append(curr[2]) #valid grouping of 3
##    return columns

##Input: a list of vertical bars with info.
##Output; array of [topleftx, toplefty, width, height] with info about the square
def getSquarePosition(vertical):    
    if len(vertical) < 4:
        print "error in get square postion"
    topleftx = vertical[1][2] ##assume the 2nd one is a good read of the left side
    toplefty = vertical[1][0]
    height = vertical[1][1]-vertical[1][0]
    ###Go through until you find a hit on the right side
    righty = 0
    nextValue = False
    for item in vertical:
        if nextValue:
            righty=item[2]
            break
        if item[2] > (topleftx + 100): ##youre on the right side
            nextValue = True
    width = righty-topleftx
    return [topleftx, toplefty, width, height]

###Take a pixel, say whether/not it's the same color as the background    
def isBackground(pixel):
    r = pixel[0]
    if r<175 or r>205:
        return False
    g = pixel[1]
    if g<195 or g>225:
        return False
    b = pixel[2]
    if b<220 or b>250:
        return False
    return True

def isFilled(imarray, x, y, width, height):
    numBackground = 0
    for a in range(10): ##sample 10 points
        randx = random.randint( x+15, x+width-10) ##don't get border 5 pix wide
        randy = random.randint( y+10, y+height-10)
        if isBackground(imarray[randy][randx]):
            numBackground+=1
        else:
            plot(randx,randy, 'r*')
    #print numBackground
    if numBackground > 5:
        return 0
    else:
        return 1

def getFour( grid, rowindex, colindex):
    if grid[rowindex][colindex] == 0:
        return 0
    #pdb.set_trace()
    ##it's a 1, do a recursive thing
    numBlocks = 0
    curr = [rowindex, colindex]
    queue = [curr]
    visitedpoints = set([])
    while len(queue)!=0:
        curr = queue.pop()
        r = curr[0]
        c = curr[1]
        grid[r][c]=0
        visitedpoints.add(tuple(curr))
        numBlocks +=1
        if numBlocks >= 5:
            break
        ##Get four adjacent squares; note that there's always a buffer on left/right/bottom, but maybe not top
        
        if grid[r+1][c]==1 and (r+1,c) not in visitedpoints:
            queue.append([r+1,c])
        if r>0: #don't go neg index
            if grid[r-1][c]==1 and (r-1,c) not in visitedpoints:
                queue.append([r-1,c])
        if c<( len(grid[0])-1 ):
            if grid[r][c+1]==1 and (r,c+1) not in visitedpoints:
                queue.append([r,c+1])
        if c>0:
            if grid[r][c-1]==1 and (r,c-1) not in visitedpoints:
                queue.append([r,c-1])
    if numBlocks == 4 or numBlocks == 5: #5: should fix, hack so squares are detected
        return visitedpoints
    else: ##make it so not set to 0 anymore
        for point in visitedpoints:
            r = point[0]
            c = point[1]
            grid[r][c] = 1
        return 0
        
        
        
    

def getActivePiece( grid ):
    for rowindex in range(5): ##look at top 5 lines
        for colindex in range(3, len(grid[0]) - 3): #look at middle 4, ie leave 3 buffer on each side
            block = getFour( grid, rowindex, colindex) #if active piece, return the points
            if block!=0:
                ##zero out the board
                for item in block:
                    grid[item[0]][item[1]] = 0
                return block
    return 0 ##return 0 if no active piece

def ExtractScreenData():    
    #pdb.set_trace()
    imarray = getImageArray()
    if size(imarray) < 100:
        print "error getting imarray, size is ", size(imarray)
    #print "imarray", imarray
    vertical = getVerticalBars(imarray)
    #print "vertical bars", vertical
    ##for item in vertical:
    ##    print item

    square = getSquarePosition(vertical) #x,y,width, height
    #print "square", square
    #print square
    numcols = 10 ##Tetris board has 10 cols
    numrows = 18 ##tetris board has rows
    colwidth = square[2] / numcols
    rowwidth = square[3] / numrows
    #print 'rowwidth colwidth', rowwidth, colwidth
    grid = [ [0]*numcols for a in range(numrows)]
    for row in range(numrows):
        for col in range(numcols):
            x = square[0] + col*colwidth
            y = square[1] + row*rowwidth
            grid[row][col] = isFilled( imarray, x,y, rowwidth, colwidth)
            
    #print "first grid"
    #for row in grid:
    #    print row
    activePiece = getActivePiece( grid) ##if active piece present, return coord and 0 out on board
    #print "after"
    #for row in grid:
    #    print row
    #print "active piece: ", activePiece
    ptype = getActivePieceType( activePiece )
    return activePiece, grid, ptype, ActivePieceRelative(activePiece, ptype)


    #########Don't need this ########
    #verticalColumnIndexes = getColumns(vertical)
    #print "vertical column indexes are", verticalColumnIndexes
    #boardWidth = abs(verticalColumnIndexes[1] - verticalColumnIndexes[0])
    #colWidth = boardWidth / 10 ##10 columns on the board
    #plotVerticalBars(vertical, imarray)
    ##imshow(imarray)
    ##x = ginput(3)
    ##print 'you click: ', x
    ##show()
    ##im.save("screenshot.jpg", "JPEG")
    ##
    ##
    ##
    ##
    ##def click(x,y):
    ##    win32api.SetCursorPos((x,y))
    ##    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    ##    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    ##
    ##
    ##for i in range(20000000):
    ##    i+1
    ##    if i%1000000==0:
    ##        print i
    ##        click(5*i/100000, 5*i/100000)
    ##        #win32api.mouse_event(2, 100,10)
    ####    if i%1000000==500000:
    ####        win32api.keybd_event(0x05, 0)
    ##
    ##
    ##import win32api
    ##import win32con
    ##import time
    ##
    ##for a in range(10):
    ##    win32api.keybd_event(0x41, 1)
    ##    time.sleep(1)
    ##    
    
    
    
