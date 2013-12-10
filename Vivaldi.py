#!/usr/bin/python
# Basic Vivaldi implementation

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
		#self.nodes = [[random.uniform(0, 300) for _i in range(conf.num_dimension)] for _j in range(conf.num_nodes)]
		self.nodes = [[0 for _i in range(conf.num_dimension)] for _j in range(conf.num_nodes)]
		self.e = [200 for _i in range(conf.num_nodes)]
		self.neighbors = []
		for node_i in xrange(self.conf.num_nodes):
			p = []
			for _j in xrange(self.conf.num_neighbors):
				neighbor_i = random.randint(0, self.conf.num_nodes-1)
				while node_i == neighbor_i: 	# Dont select yourself as a neigbour
					neighbor_i = random.randint(0, self.conf.num_nodes-1)
				p.append(neighbor_i)
			self.neighbors.append(p)
			print node_i, p
		
	
	# Core of the Vivaldi algorithm
	def norun(self):
		movements = []
		# for each iteration
		# for each node pick up K random neighbors
		# check how much the node has to "move" in terms of RTT towards/away his neighbors
		# compute the new coordinates following the Vivaldi algorithm
		for _iteration in xrange(self.conf.num_interations):
			#print "-----------------------------------------"
			for node_i in xrange(self.conf.num_nodes):
				node = self.nodes[node_i]
				for neighbor_i in self.neighbors[node_i]:
					#neighbor_i = random.randint(lower, upper)
					#neighbor_i = random.choice(self.neighbors[node_i])
					neighbor = self.nodes[neighbor_i]
					rtt = self.graph.getRTT(node_i, neighbor_i)
					dist = getNorm(getVet(node, neighbor))
					if dist == 0:
						u = getRandomDirection(self.conf.num_dimension)
					else:
						u = getDirection(neighbor, node)
					#new_coords = map(lambda old, ud: old + self.conf.delta * (rtt - dist) * ud, node, u)
					new_coords = map(lambda old, ud: old + 0.01 * (rtt - dist) * ud, node, u)
					ndist = getNorm(getVet(new_coords, neighbor))
					if node_i == -1:
						print "%3d %3d: [%3d %3d] => [%3d %3d]  %6.1f  %6.1f   %3d  %3d %3d  [%4.1f %4.1f]" % \
						(node_i, neighbor_i, node[0],  node[1], new_coords[0], new_coords[1], rtt-dist, rtt-ndist, rtt, dist, ndist, u[0], u[1])
					#movements[iteration].append(rtt-dist)
					node = new_coords
				self.nodes[node_i] = new_coords
# 		for iteration in xrange(self.conf.num_interations):
# 			for node_i in xrange(self.conf.num_nodes):
# 			print "     %6.1f %6.1f %6.1f %6.1f"%(movements[0][iteration], movements[1][iteration], movements[2][iteration], movements[3][iteration])
	
	# Core of the Vivaldi algorithm
	def run(self):
		# for each iteration
		# for each node pick up K random neighbors
		# check how much the node has to "move" in terms of RTT towards/away his neighbors
		# compute the new coordinates following the Vivaldi algorithm
		ce = self.conf.ce
		cc = 0.01
		for iteration in xrange(self.conf.num_interations):
			if iteration % 10 == 0:
				stdout.write("\r=> %d%%"%(float(iteration) / self.conf.num_interations * 100))
				stdout.flush()
			for node_i in xrange(self.conf.num_nodes):
				node = self.nodes[node_i]
				for neighbor_i in self.neighbors[node_i]:
					neighbor = self.nodes[neighbor_i]
					w = self.e[node_i] / (self.e[node_i] + self.e[neighbor_i])
					#w = self.e[node_i] / (self.e[node_i] + ej)
					rtt = self.graph.getRTT(node_i, neighbor_i)
					dist = getNorm(getVet(node, neighbor))
					if dist == 0:
						u = getRandomDirection(self.conf.num_dimension)
					else:
						u = getDirection(neighbor, node)
					es = abs(dist-rtt)/rtt
					self.e[node_i] = es*ce*w + self.e[node_i]*(1-ce*w)
					delta = cc*w*0.1
					#delta = 0.25
					if node_i == -1:
						print "%7.2f %1.4f"%(self.e[node_i], delta)
					new_coords = map(lambda old, ud: old + delta * (rtt - dist) * ud, node, u)
					ndist = getNorm(getVet(new_coords, neighbor))
					if node_i == 0:
						print "%3d %3d: [%3d %3d] => [%3d %3d]  %6.1f  %6.1f   %3d  %3d %3d  [%4.1f %4.1f]" % \
						(node_i, neighbor_i, node[0],  node[1], new_coords[0], new_coords[1], rtt-dist, rtt-ndist, rtt, dist, ndist, u[0], u[1])
					node = new_coords
				self.nodes[node_i] = node
	
	# Core of the Vivaldi algorithm
	def oldrun(self):
		# for each iteration
		# for each node pick up K random neighbors
		# check how much the node has to "move" in terms of RTT towards/away his neighbors
		# compute the new coordinates following the Vivaldi algorithm
		for _iteration in xrange(self.conf.num_interations):
			for node_i in xrange(self.conf.num_nodes):
				node = self.nodes[node_i]
				for _neighbour in xrange(self.conf.num_neighbors):
					neighbor_i = random.randint(0, self.conf.num_nodes-1)
					while node_i == neighbor_i: 	# Dont select yourself as a neigbour
						neighbor_i = random.randint(0, self.conf.num_nodes-1)
					neighbor = self.nodes[neighbor_i]
					rtt = self.graph.getRTT(node_i, neighbor_i)
					dist = getNorm(getVet(node, neighbor))
					u = getDirection(neighbor, node)
					new_coords = map(lambda old, ud: old + self.conf.delta * (rtt - dist) * ud, node, u)
					node = new_coords
				self.nodes[node_i] = node
	
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
			for j in xrange(self.conf.num_nodes):
				if i != j:
					#print self.graph.getRTT(i,j), predicted_graph.getRTT(i, j), self.graph.getRTT(i,j) - predicted_graph.getRTT(i, j)
					#out.append((self.graph.getRTT(i,j) - predicted_graph.getRTT(i, j))**2)
					real = self.graph.getRTT(i,j)
					approx = predicted_graph.getRTT(i, j)
					#approx = getNorm(getVet(self.nodes[i], self.nodes[j]))
					v = 0 if real == 0 else abs(real - approx) / real
					if v > 100:
						print i, j, real, approx, v
					out.append(v)
					#print real, approx, 0 if real == 0 else abs((real - approx) / real)
		return out
	
	# basic CDF computation
	def computeCDF(self, input_):
		print ">>>" + str(len(input_))
		x = sorted(input_)
		y = map(lambda x: x / float((len(input_) + 1)), range(len(input_)))
		return x,y
	
#def get2DNorm(x, y):
#	return math.sqrt(x*x + y*y)

# Gives the motion vector from a to b
def getVet(a,b):
	return map(operator.sub, b, a)

def getNorm(vPos):
	norm = 0
	for i in range(len(vPos)):
		norm += (vPos[i])**2
	return sqrt(norm)

def getDirection(a, b):
	v = getVet(a, b)
	l = getNorm(v)
	return map(lambda x: 0 if l==0 else x/l, v)
	
def getRandomDirection(dims):
	return [random.uniform(-1, 1) for _i in range(dims)]
