from __future__ import division
import random
import operator
import math

def getVet(a,b):
    return map(operator.sub, b, a)

def getNorm(vPos):
    norm = 0
    for i in range(len(vPos)):
        norm += (vPos[i])**2
    return math.sqrt(norm)

n = 200 #number of nodes

# create random nodes
nodes = [[random.uniform(0, 300) for _i in range(3)] for _j in range(n)]

# print matrix
for i in xrange(n):
    for j in xrange(n):
        print "%.2f"%(getNorm(getVet(nodes[i], nodes[j])) + random.uniform(0, 20)),
    print ""
