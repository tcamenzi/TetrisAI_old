class BoardState(object):
    board = 0
    numLeft = 0
    numRight = 0
    numDown = 0
    numRotate = 0

    def __init__(self, board, left, right, down, rotate):
        self.board = board
        self.numLeft = left
        self.numRight = right
        self.numDown = down
        self.numRotate = rotate

    def printBoard(self):
        for row in self.board:
            print row
