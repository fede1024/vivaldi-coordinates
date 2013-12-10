from Graph import buildgraph
import sys

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
    
    for x in xrange(size):
        sys.stdout.write("\r=> %d%%"%(float(x) / size * 100))
        sys.stdout.flush()
        for z in xrange(size):
            for y in xrange(size):
                d_xz = graph.getRTT(x, z)
                d_xy = graph.getRTT(x, y)
                d_yz = graph.getRTT(y, z)
                # d_xz <= d_xy + d_yz
                err = d_xz - (d_xy + d_yz)
                if err > 0:
                    errors.append([x, z, y, err])
                    
    print ""
    
    errors = sorted(errors, key = lambda x: -x[3])
    
    for x in errors[0:10]:
        print "%d %d %d %f"%(x[0], x[1], x[2], x[3])
        print "d:(%d, %d) = %d"%(x[0], x[2], graph.getRTT(x[0], x[2])) 
        print "d:(%d, %d) = %d"%(x[0], x[1], graph.getRTT(x[0], x[1])) 
        print "d:(%d, %d) = %d\n"%(x[1], x[2], graph.getRTT(x[1], x[2])) 
    
    print len(errors), "over", 200*200*200, "=", float(len(errors))/(200*200*200)*100, "%"
    print sum([x[3] for x in errors]) / float(len(errors))
