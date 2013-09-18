black = [0,0,0]

##Draw an individual black square, or don't draw if uncolored.
def drawSquare(board, screen, rowIndex, colIndex, pygame):
    if board.board[rowIndex][colIndex] == 1:
        x_coord = colIndex * board.colpixWidth
        y_coord = rowIndex * board.rowpixWidth
        pygame.draw.rect( screen, black, [x_coord, y_coord, board.colpixWidth, board.rowpixWidth]) 

def drawBoard( screen, board, pygame ):
    ##Iterate over the board and draw all black squares
    for rowIndex in range(len(board.board)):
        for colIndex in range(len(board.board[rowIndex])):
            drawSquare( board, screen, rowIndex, colIndex, pygame)
            
    ##Draw the active piece.
    for coord in board.piece.relativePoints:
        xcoord = board.colpixWidth * (coord.x + board.piece.centerx)
        ycoord = board.rowpixWidth * (coord.y + board.piece.centery)
        pygame.draw.rect( screen, board.piece.color, [xcoord, ycoord, board.colpixWidth, board.rowpixWidth] )
        
                
