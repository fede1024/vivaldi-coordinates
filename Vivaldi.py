#!/usr/bin/python
# Basic Vivaldi implementation

from __future__ import division
import random
from Graph import Graph
from math import sqrt
#from operator import sub
import operator
from sys import stdout

class Vivaldi():
    def __init__(self, graph, conf):
        self.graph = graph
        self.conf = conf
        # Initialize nodes coordinates
        self.nodes = [[random.uniform(0, 300) for _i in range(conf.num_dimension)] for _j in range(conf.num_nodes)]
        #self.nodes = [[0 for _i in range(conf.num_dimension)] for _j in range(conf.num_nodes)]
        # Initialize nodes errors
        self.e = [200 for _i in range(conf.num_nodes)]
        # initialize node neighbors
        self.neighbors = []
        for node_i in xrange(self.conf.num_nodes):
            p = []
            for _j in xrange(self.conf.num_neighbors):
                neighbor_i = random.randint(0, self.conf.num_nodes-1)
                while node_i == neighbor_i:     # Dont select yourself as a neigbour
                    neighbor_i = random.randint(0, self.conf.num_nodes-1)
                p.append(neighbor_i)
            self.neighbors.append(p)
        self.movements = []
    
    # Version without considering error estimation
    def run_noerror(self):
        for _iteration in xrange(self.conf.num_interations):
            for node_i in xrange(self.conf.num_nodes):
                node = self.nodes[node_i]
                for neighbor_i in self.neighbors[node_i]:
                    neighbor = self.nodes[neighbor_i]
                    rtt = self.graph.getRTT(node_i, neighbor_i)
                    dist = getNorm(getVet(node, neighbor))
                    if dist == 0:    # Used when all nodes are initialized in zero
                        u = getRandomDirection(self.conf.num_dimension)
                    else:
                        u = getDirection(neighbor, node)
                    new_coords = map(lambda old, ud: old + 0.01 * (rtt - dist) * ud, node, u)
                    #ndist = getNorm(getVet(new_coords, neighbor))
                    #if node_i == -1:
                    #    print "%3d %3d: [%3d %3d] => [%3d %3d]  %6.1f  %6.1f   %3d  %3d %3d  [%4.1f %4.1f]" % \
                    #    (node_i, neighbor_i, node[0],  node[1], new_coords[0], new_coords[1], rtt-dist, rtt-ndist, rtt, dist, ndist, u[0], u[1])
                    node = new_coords
                self.nodes[node_i] = new_coords
    
    # Version with error estimation
    def run(self):
        ce = self.conf.ce   # setting of cc and ce parameters
        cc = ce
        for iteration in xrange(self.conf.num_interations):
            if iteration % 10 == 0: # Print progress
                stdout.write("=> %d%%\r"%(float(iteration) / self.conf.num_interations * 100))
                stdout.flush()
            for node_i in xrange(self.conf.num_nodes):
                mov = []        #    Node movements will be stored here
                node = self.nodes[node_i]   # Current node
                for neighbor_i in self.neighbors[node_i]:
                    neighbor = self.nodes[neighbor_i]   # Neighbor
                    w = self.e[node_i] / (self.e[node_i] + self.e[neighbor_i])
                    rtt = self.graph.getRTT(node_i, neighbor_i)
                    dist = getNorm(getVet(node, neighbor))
                    if dist == 0:    # Used when all nodes are initialized in zero
                        u = getRandomDirection(self.conf.num_dimension)
                    else:
                        u = getDirection(neighbor, node)
                    es = abs(dist-rtt)/rtt
                    self.e[node_i] = es*ce*w + self.e[node_i]*(1-ce*w)
                    delta = cc*w
                    new_coords = map(lambda old, ud: old + delta * (rtt - dist) * ud, node, u) # Calculates new coordinates
                    #ndist = getNorm(getVet(new_coords, neighbor))
                    #if node_i == 0:
                    #    print "%3d %3d: [%3d %3d] => [%3d %3d]  %6.1f  %6.1f   %3d  %3d %3d  [%4.1f %4.1f]" % \
                    #    (node_i, neighbor_i, node[0],  node[1], new_coords[0], new_coords[1], rtt-dist, rtt-ndist, rtt, dist, ndist, u[0], u[1])
                    node = new_coords   # Update coordinates based on one neighbor
                mov.append(getNorm(getVet(new_coords, self.nodes[node_i]))) # Store node movement
                self.nodes[node_i] = node   # Update node for this iteration
            self.movements.append(sum(mov) / len(mov))  # Stores the average of nodes movements in this iteration
    
    # get the predicted RTT graph following Vivaldi.
    def getRTTGraph(self):
        graph = Graph(self.conf.getNumNodes());
        for i, node1 in enumerate(self.nodes):
            for j, node2 in enumerate(self.nodes):
                rtt = getNorm(getVet(node1, node2))
                graph.addVertex(i, j, rtt)
        return graph

    # get the position of a node 
    def getPositions(self, node):
        return self.nodes[node]
    
    # Relative error of the predicted graph wrt real RTT graph
    def getRelativeError(self, predicted_graph):
        out = []
        for i in xrange(self.conf.num_nodes):
            node_error = 0.0;
            for j in xrange(self.conf.num_nodes):
                if i != j:
                    real = self.graph.getRTT(i,j)
                    approx = predicted_graph.getRTT(i, j)
                    link_error = 0 if real == 0 else abs(real - approx) / real
                    node_error += link_error
            node_error /= (self.conf.num_nodes - 1)
            out.append(node_error)
        return out
    
# basic CDF computation
def computeCDF(input_):
    x = sorted(input_)
    y = map(lambda x: x / (len(input_) + 1), range(len(input_)))
    return x,y
    
# Gives the motion vector from a to b
def getVet(a,b):
    return map(operator.sub, b, a)

# Returns the norm of a n-dimension vector
def getNorm(vPos):
    norm = 0
    for i in range(len(vPos)):
        norm += (vPos[i])**2
    return sqrt(norm)

# Get the direction (vector) from point a to b
# Length of vector: always 1 (if a != b)
def getDirection(a, b):
    v = getVet(a, b)
    l = getNorm(v)
    return map(lambda x: 0 if l==0 else x/l, v)
    
# Get random direction
def getRandomDirection(dims):
    return [random.uniform(-1, 1) for _i in range(dims)]
