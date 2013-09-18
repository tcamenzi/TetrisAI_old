import sys
import winsound
from tetris import runOnce
from invisibleTetris import runOnceInvisible
from assignScores import constantInit

def testSequence(values):
##    bp = float(sys.argv[1])
##    sp = float(sys.argv[2])
##    hp = float(sys.argv[3])
    bp = values[0]
    sp = values[1]
    hp = values[2]
    nahbp = values[3]
    tp = values[4]
    print "\n\n"
    print "bp sp hp nahbp tp", bp, sp, hp, nahbp, tp
    constantInit(bp, sp,hp, nahbp, tp)
    results = []
    for a in range(1):
        results.append(runOnce())
    results.sort()
    print results

testSequence([20, 1, 0, 1, 1])
##testSequence([20, 1, 0, 1, 1])
##testSequence([20, 1, 0, 1, 1])
##testSequence([20, 1, 0, 1, 1])
##testSequence([20, 1, 0, 1, 1])
##testSequence([20, 1, 0, 1, 1])









winsound.Beep(1000,1000)

