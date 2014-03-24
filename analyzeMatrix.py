from __future__ import division
from Graph import buildgraph
from Vivaldi import computeCDF
import math
import sys

from pylab import figure, plot, suptitle, xlabel, ylabel, show, savefig

if __name__== "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s <rtt_file>"%sys.argv[0]
        sys.exit(0)
    
    rttfile = sys.argv[1]
    infile = open(rttfile, 'r')
    rows = infile.readlines()
    num_nodes = len(rows)
    infile.close()

    graph = buildgraph(rows)
    
    size = graph.getGraphSize()
    
    errors = []
    symm = []
    
    # Check error in triangle inequality
    for x in xrange(size):
        sys.stdout.write("\r=> %d%%"%(float(x) / size * 100))
        sys.stdout.flush()
        for z in xrange(size):
            if z > x and graph.getRTT(x, z) != graph.getRTT(z, x):
                symm.append([x, z, abs(graph.getRTT(x, z) - graph.getRTT(z, x))])
            for y in xrange(size):
                d_xz = graph.getRTT(x, z)
                d_xy = graph.getRTT(x, y)
                d_yz = graph.getRTT(y, z)
                # d_xz <= d_xy + d_yz
                err = d_xz - (d_xy + d_yz)
                errors.append([x, z, y, err if err > 0 else 0])
                    
    print ""
    
    # Take worst results frst
    symm = sorted(symm, key = lambda x: -x[2])
    # Print worst paths
    for x in symm[0:4]:
        print "%d %d %d %d %f"%(x[0], x[1], graph.getRTT(x[0], x[1]), graph.getRTT(x[1], x[0]),  x[2])
    average = sum([x[2] for x in symm]) / len(symm)
    print "Average: %.2f"%average
    print len(symm), "over", 200*200, "=", len(symm)/(200*200)*100, "%"
    
    errors = sorted(errors, key = lambda x: -x[3])
    
    for x in errors[0:10]:
        print "%d %d %d %f"%(x[0], x[1], x[2], x[3])
        print "d:(%d, %d) = %d"%(x[0], x[2], graph.getRTT(x[0], x[2])) 
        print "d:(%d, %d) = %d"%(x[0], x[1], graph.getRTT(x[0], x[1])) 
        print "d:(%d, %d) = %d\n"%(x[1], x[2], graph.getRTT(x[1], x[2])) 
    

    err = [e[3] for e in errors]
    err2 =  [e[3] for e in errors if e[3] > 0]
    print len(err2), "over", 200*200*200, "=", len(err2)/(200*200*200)*100, "%"

    average = sum(err) / len(err)
    average2 = sum(err2) / len(err2)
    
    print "Maximum: %.2f"%max(err)
    print "Average: %.2f"%average
    print "Average of violations: %.2f"%average2
    print "Minimum: %.2f"%min(err)

    # plot error distribution
    x,y = computeCDF(err)

    fig = figure()
    #plot(x,[1-ny for ny in y])
    ax = fig.add_subplot(1,1,1)
    #plot([math.log(nx+1, 10) for nx in x], y)
    plot(x, y)
    ax.set_xscale('log')
    ax.set_xlim(1, max(x))
    ax.set_ylim(0.5, 1)
    suptitle('Triangle inequality violations', fontsize=20)
    xlabel('Violation in ms', fontsize=16)
    ylabel('Frequency', fontsize=16)
    savefig('Matrix errors.png')

    show()