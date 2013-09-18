import random
import os.path
SEQUENCE = []
#FIRST = True
READ = ""
COUNTER = 0
FILE = 407

def writeToFile():
    global SEQUENCE
    if len(SEQUENCE) == 0:
        return
    start = 0
    while(os.path.isfile("randgenFiles/"+str(start)+".txt")):
        start+=1
    f = open("randgenFiles/"+str(start)+".txt", "w")
    for item in SEQUENCE:
        f.write(str(item))
    f.close()
    print "File written, sequence size", len(SEQUENCE), "file # is ", start
    SEQUENCE = []

def getRandomPieceRead():
    global COUNTER
    global READ
    if COUNTER == 0: ##first time, open file
        global FILE
        f = open("randgenFiles/"+str(FILE)+".txt", "r")
        READ = f.read()
        f.close()
    COUNTER+=1
    return int(READ[COUNTER-1])

def getRandomPieceWrite():
    temp = random.randint(0,6)
    global SEQUENCE
    SEQUENCE.append(temp)
    #print SEQUENCE
    return temp

def getRandomPiece():
    return getRandomPieceWrite()
