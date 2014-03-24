#!/usr/bin/python

from __future__ import division
from Graph import buildgraph
from Configuration import Configuration
from Vivaldi import Vivaldi, computeCDF

from pylab import *

def cdfValue(x, y, q):
    for (i, j) in zip(x, y):
        if j <= q:
            v = i 
        else:
            break
    return v
    
if __name__== "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s <rtt_file>"%sys.argv[0]
        sys.exit(0)
    
    rttfile = sys.argv[1]
    infile = open(rttfile, 'r')
    rows = infile.readlines()
    num_nodes = len(rows)
    infile.close()
    
    # These parameters are part of the Configuration.
    # Modify them according to your need.
    num_neighbors = 20
    num_iterations = 200

    # build a configuration and load the matrix into the graph
    c = Configuration(num_nodes, num_neighbors, num_iterations)
    init_graph = buildgraph(rows)

    print "Running Vivaldi on a %d size matrix" % num_nodes
    print "Num neighbors = %d " % num_neighbors 
    print "Num iterations = %d " % num_iterations
    
    v = Vivaldi(init_graph, c)

    v.run()
    
    # get predicted graph
    predicted = v.getRTTGraph()
    # get relative errors (one value per node)
    rerr = v.getRelativeError(predicted)
    
    # average of node movements
    average = sum(v.movements) / len(v.movements)
    # variance of node movements
    variance = sum((average - value) ** 2 for value in v.movements) / len(v.movements)
    
    print "Position variation:"
    print "Maximum: %.2f"%max(v.movements)
    print "Average: %.2f"%average
    print "Minimum: %.2f"%min(v.movements)
    print "Variance: %.2f\n"%variance

    # average of relative errors
    average = sum(rerr) / len(rerr)
    # variance of relative errors
    variance = sum((average - value) ** 2 for value in rerr) / len(rerr)
    
    print "Relative error:"
    print "Maximum: %.2f"%max(rerr)
    print "Average: %.2f"%average
    print "Minimum: %.2f"%min(rerr)
    print "Variance: %.2f"%variance

    # Compute CDF
    x,y = computeCDF(rerr)
    
    print "Values: %.2f %.2f %.2f"%(cdfValue(x, y, 0.5), cdfValue(x, y, 0.9), cdfValue(x, y, 0.99))

    fig = figure()
    plot(x,y)
    suptitle('Relative errors CDF', fontsize=20)
    xlabel('Relative error', fontsize=16)
    ylabel('Probability', fontsize=16)
    savefig('output-%d-%d.png'%(num_neighbors, num_iterations))
    show()
