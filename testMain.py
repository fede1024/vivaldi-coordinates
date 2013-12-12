#!/usr/bin/python

from __future__ import division
from Graph import buildgraph
from Configuration import Configuration
from Vivaldi import Vivaldi, computeCDF
import json

from pylab import *
    
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
    num_neighbors = 10
    num_iterations = 1000

    # build a configuration and load the matrix into the graph
    c = Configuration(num_nodes, num_neighbors, num_iterations)
    init_graph = buildgraph(rows)

    print "Running Vivaldi on a %d size matrix" % num_nodes
    print "Num neighbors = %d " % num_neighbors 
    print "Num iterations = %d " % num_iterations
    
    # run vivaldi: here, only the CDF of the relative error is retrieved. 
    # Modify to retrieve what's requested.
    v = Vivaldi(init_graph, c)


    with open("output.txt", "r") as myfile:
        movements = json.load(myfile)['v']
        
    print type(movements)
    
    fig = figure(figsize=[10,5])
    plot(movements[0][0:300])
    plot(movements[1][0:300])
    plot(movements[2][0:300])
    
    xlabel('Iteration number', fontsize=16)
    ylabel('Movement', fontsize=16)
    savefig('mov.png')
    fig.show()

    1/0

    v.run()
    
    predicted = v.getRTTGraph()
    rerr = v.getRelativeError(predicted)
    
    #print sum(rerr) / float(len(rerr))
    average = sum(rerr) / len(rerr)
    variance = sum((average - value) ** 2 for value in rerr) / len(rerr)
    
    print "Relative error:"
    print "Maximum: %.2f"%max(rerr)
    print "Average: %.2f"%average
    print "Minimum: %.2f"%min(rerr)
    print "Variance: %.2f"%variance

    x,y = computeCDF(rerr)

    fig = figure()
    
    '''
    plot(x,y)
    suptitle('Relative errors CDF', fontsize=20)
    xlabel('Relative error', fontsize=16)
    ylabel('Probability', fontsize=16)
    savefig('output.png')
    fig.show()
    '''
    