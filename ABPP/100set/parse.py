import sys
from collections import defaultdict

ncol=90

lines = open(sys.argv[1], 'r').readlines()
results = defaultdict(list)
for l in lines:
    es = l.strip().split()
    for i in range(ncol):
        ci = i*2 + 4
        c = float(es[ci])
        results[i].append(c)

#print(results)
for i in range(ncol):
    r10 = results[i][3]/results[i][0]
    r5 = results[i][2]/results[i][0]
    r2 = results[i][1]/results[i][0]
    print( "%d %4.2f %4.2f %4.2f" % (i, r2, r5, r10) )
