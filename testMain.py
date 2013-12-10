#!/usr/bin/python

from Graph import buildgraph
from Configuration import Configuration
from Vivaldi import Vivaldi
import sys

try:
	import __pypy__
except ImportError:
	__pypy__ = None

if __pypy__ == None:
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
	#num_neighbors = 10
	#num_iterations = 200
	num_neighbors = 10
	num_iterations = 1000

	num_dimension = 3
	
	# build a configuration and load the matrix into the graph
	c = Configuration(num_nodes, num_neighbors, num_iterations, num_dimension)
	init_graph = buildgraph(rows)

	print "Running Vivaldi on a %d size matrix" % num_nodes
	print "Num dimensions = %d " % num_dimension
	print "Num neighbors = %d " % num_neighbors 
	print "Num iterations = %d " % num_iterations
	
	# run vivaldi: here, only the CDF of the relative error is retrieved. 
	# Modify to retrieve what's requested.
	v = Vivaldi(init_graph, c)

	v.run()
	for node in v.nodes:
		print "%5.1f %5.1f %5.1f"%(node[0], node[1], node[2])
	
	predicted = v.getRTTGraph()
	rerr = v.getRelativeError(predicted)
	
# 	for i in xrange(c.num_nodes):
# 		for j in xrange(i, c.num_nodes):
# 			print "%3d %3d" % (init_graph.getRTT(i, j), predicted.getRTT(i, j))
# 			d = init_graph.getRTT(i, j) - init_graph.getRTT(j, i) 
# 			if d > 0:
# 				print '%3d %3d  - %4d %4d %4d %5.1f' % (i, j,init_graph.getRTT(i, j), init_graph.getRTT(j, i),  d, predicted.getRTT(i, j))
			
	# media errore
	print sum(rerr) / float(len(rerr))

	if __pypy__ == None:
		# Example (using pylab plotting function):
		x,y = v.computeCDF(rerr)
		plot(x,y)
		show()
