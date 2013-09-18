##FOR EVERYTHING: THE TOP LEFT SQUARE IS 0,0; moving down / right increases the coordinates

from getRandomPiece import getRandomPiece

class coord(object): ##just to allow easy access to x,y coordinates
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

RED = [255,0,0]
GREEN = [0,255,0]
BLUE =[0,0,255]

class ActivePiece(object):
    centerx = 0 #The x y coordinates of the center
    centery = 0
    relativePoints = [] #the positions of the points relative to the center.
    color = RED
    type = 0 #whether square, rectangle etc.
    
    def __init__(self, x, y):
        self.centerx = x
        self.centery = y
        self.type = getRandomPiece() #randomly choosee a type of piece, assign it the appropriate coordinates.
        if self.type == 0: #square
            self.relativePoints = [ coord(0,0), coord(0, -1), coord(1,0), coord(1,-1) ]
        elif self.type==1: # straight
            self.relativePoints = [ coord(0, 1), coord(0, 0), coord(0, -1), coord(0, -2) ]
        elif self.type==2: #T
            self.relativePoints = [ coord(0,1), coord(0,0), coord(-1,0), coord(1,0) ]
        elif self.type==3: #L
            self.relativePoints = [ coord(0,1), coord(0,0), coord(0,-1), coord(-1,-1) ]
        elif self.type==4: #L backwards
            self.relativePoints = [ coord(0,1), coord(0,0), coord(0,-1), coord(1,-1) ]
        elif self.type==5: #S
            self.relativePoints = [ coord(0,0), coord(0,1), coord(-1,0), coord(-1,-1) ]
        elif self.type==6: #S backwards
            self.relativePoints = [ coord(0,0), coord(0,1), coord(1,0), coord(1,-1) ]
             
    def moveDown(self): 
        self.centery+=1

    def moveUp(self):
        self.centery-=1

    def moveLeft(self):
        self.centerx-=1

    def moveRight(self):
        self.centerx+=1
            
    def rotate(self): ##to rotate a point left about the center, swap x and y then make x negative
        if self.type != 0: #don't rotate squares
            for coord in self.relativePoints:
                temp = coord.x
                coord.x = coord.y
                coord.y = temp
                coord.x *=-1
        

        

    
            
