def runOnce():
    ROWS_CLEARED = 0
    # Define the colors we will use in RGB format
    black = [  0,  0,  0]
    white = [255,255,255]
    blue =  [  0,  0,255]
    green = [  0,255,  0]
    red =   [255,  0,  0]

    # Import a library of functions called 'pygame'
    import pygame
    from boardClass import board
    from draw import drawBoard
    from getRandomPiece import writeToFile
     
    # Initialize the game engine
    pygame.init()
      
    # Set the height and width of the screen

    NUMROWS = 25
    NUMCOLS = 10
    SQUARE_SIZE = 25

    size=[NUMCOLS*SQUARE_SIZE,NUMROWS*SQUARE_SIZE]
    screen=pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")

    board = board( NUMROWS, NUMCOLS, size )
            
    #Loop until the user clicks the close button.
    done=False
    clock = pygame.time.Clock()
    counter = 0

    SIDE_DELAY = 5 #delay in loops before it starts moving left/right
    left_counter = 0 #how long left key has been held in game loops
    right_counter = 0 #how long right key has been held
    clock_speed = 20

    while done==False:
        counter +=1 #how many times loop has been run total
     
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(clock_speed)
         
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: #pressed left, move left
                    board.movePieceLeft()
                if event.key == pygame.K_RIGHT: #pressed right, move right
                    board.movePieceRight()
                if event.key == pygame.K_UP: #pressed up, so rotate the block
                    board.rotatePiece()
                if event.key == pygame.K_p:
                    ##print "enter new clock speed: "
                    clock_speed = int(raw_input("enter new clock speed: "))

        ##If you hold down left/right, have a brief delay then move quickly L/R
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]: ##Left arrow is held
             left_counter +=1
             if left_counter > 25: ##delay for .25s bfore moving quickly
                 board.movePieceLeft()
        else:
            left_counter = 0 ##not held, reset for delay

        if keys[pygame.K_RIGHT]:
             right_counter +=1
             if right_counter > 5:
                 board.movePieceRight()
        else:
            right_counter = 0

        ##If you hold down down, move down rapidly with no delay
        if keys[pygame.K_DOWN]:
            board.movePieceDown()

        if counter % 1 == 0: ##every other second but stagger with moveDowns
            if board.numRotations != 0:
                board.rotatePiece()
                board.numRotations-=1
            elif board.numLeft != 0:
                board.movePieceLeft()
                board.numLeft-=1
            elif board.numRight !=0:
                board.movePieceRight()
                board.numRight-=1
            ##force the square to move down every .5 seconds     
            board.movePieceDown()
            
        if board.hasLost: ##Flagged upon losing condition.
            print "You have lost. You have cleared this many rows: ", board.numRowsCleared
            ROWS_CLEARED = board.numRowsCleared
            writeToFile() #store the sequence of randgen numbers
            pygame.quit()
            return ROWS_CLEARED
            #done = True
         
        # Clear the screen and set the screen background
        screen.fill(white)

        #draw the board
        drawBoard( screen, board, pygame )
     
        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
     
    # Be IDLE friendly
    pygame.quit ()
