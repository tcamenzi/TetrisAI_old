from tetris import runOnce
from invisibleTetris import runOnceInvisible
results = []
for a in range(10):
    results.append(runOnceInvisible())
results.sort()
print results


