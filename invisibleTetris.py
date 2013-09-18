def runOnceInvisible():
    ROWS_CLEARED = 0
    from boardClass import board
    from draw import drawBoard
    from getRandomPiece import writeToFile
    
    NUMROWS = 25
    NUMCOLS = 10
    SQUARE_SIZE = 25
    size=[NUMCOLS*SQUARE_SIZE,NUMROWS*SQUARE_SIZE]
    board = board( NUMROWS, NUMCOLS, size )

    ##pygame stuff, temp
##    import pygame
##    pygame.init()
##    screen = pygame.display.set_mode(size)
##    clock = pygame.time.Clock()

    while(not board.hasLost):
        if(board.numRotations!=0):
            board.rotatePiece()
            board.numRotations-=1
        elif( board.numLeft!=0):
            board.movePieceLeft()
            board.numLeft-=1
        elif( board.numRight!=0):
            board.movePieceRight()
            board.numRight-=1
        board.movePieceDown()
        
    ##you've lost here
    print "You have lost. You have cleared this many rows: ", board.numRowsCleared
    ROWS_CLEARED = board.numRowsCleared
    writeToFile() #store the sequence of randgen numbers
    return ROWS_CLEARED
