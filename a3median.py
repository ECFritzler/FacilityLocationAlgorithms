#######################################################################################
# a3median.py
# Claire Fritzler - 001167579
# 4110 Assignment 3
#
# The a3median.py program should:
# - Take an optional parameter -n value
# - If the optional parameter is not included, then we read from the input GML file
# - Check if the network is a path
# - Check if the nodes all have weights
# - Check if the edges all have lengths
# - Return the OPT-1-Median and the ID of the node where the 1 median will be located
#######################################################################################

import networkx as nx
import random
import argparse
import itertools 
# Function to initialize the graph with n nodes and write the graph to a GML file
def initGraph(n, f):
	Graph = nx.path_graph(n)
	
	#Initialize weights
	for i in range(0, n):
		weight = random.randint(1, 20)
		Graph.node[i]['weight'] = weight
		Graph.node[i]['index'] = i
	
	#initialize lengths		
	for i in range(1, n):
		length = random.randint(1, 10)
		Graph.edges[i-1, i]['length'] = length
		
	f = f + ".gml"
	nx.write_gml(Graph, f)
	return Graph

# Function to check if the network is a path
# Property of paths: number of nodes - number of edges = 1
def isPath(Graph):
	edges = nx.number_of_edges(Graph)
	nodes = nx.number_of_nodes(Graph)
	
	if((nodes - edges) != 1):
		return False
	else:
		return True
		
# Function to check if the nodes all have weights		
def haveWeights(Graph):
	for i in Graph.nodes():
		if(not Graph.node[i]['weight']):
			return False
		if(Graph.node[i]['weight'] < 1):
			return False
	return True

# Function to check if all the edges have lengths
def haveLengths(Graph):
	for source, target, edge in Graph.edges(data = True):
		if(not edge):
			print("Your graph is missing an edge")
			return False
		elif(edge['length'] < 1):
			print("Your graph has invalid edge lengths")
			return False
	return True
	
# Parse the input user arguments 	
parser = argparse.ArgumentParser(description='1-Median Calculator for a Graph')
parser.add_argument('-n', nargs='?', type=int, help='Number of nodes')
parser.add_argument('file', type=str, help='GML File')
parser.add_argument('-p', type=int, help='Number of facilities to be placed')
args = parser.parse_args()
n = args.n
file = args.file
p = args.p
	
	
############################################################################################
# 1-Median Calculation:
# Calculate the cost of each node and store it in a list 
# Go through the list and find the minimum value
############################################################################################

#costs = []
#for facility in Graph.nodes():
#	sum = 0
#	for customer in Graph.nodes():
#		if(customer != facility):
#			weight = Graph.node[customer]['weight']
#			distance = nx.shortest_path_length(Graph, customer, facility, 'length')
#			sum = sum + (weight + distance)
#	costs.append((sum, facility))
#	
#optimalFacility = min(costs, key=lambda t: (t[0]))
# print("The cost of the 1-Median is: " + str(optimalFacility[0]))
# print("The ID of the 1-Median is: " + str(optimalFacility[1]))


############################################################################################
# P-Median Calculation:
# Calculate the cost of the medians at each node and store them in a matrix
# Go through the matrix and find the minimum value
############################################################################################

# Function to calculate the weighted distance of two vertices
# Take the weight of the first vertex multiplied by the distance to the second vertex
	
F = [list() for x in range(n)]
G = []
row = []
def PMedian(Graph):
	for q in range(1, p): #Iterate through the number of facilities
		sum = 0
		cost = []
		for j in range(1, n): #Iterate through the number of nodes 
			# Compute G
			for k in range(j+1, n+1): #from the current node to the number of nodes
				if(q == 1):
					for t in range(j, 1):
						weight = Graph.node[t]['weight']
						distance = nx.shortest_path_length(Graph, t, j, 'length')
						sum = sum + (weight + distance)
						cost.append(sum)
						G.append(cost)
				if(q > 1):
					for t in range(j, k-1):
						if(j!=t):
							weight = Graph.node[t]['weight']
							distance = nx.shortest_path_length(Graph, t, j, 'length')
							sum = sum + (weight + distance)
							cost.append(sum + F[q-1][k])				
							G[q].append(cost)
			for k in range(j, n):
				for t in range(j, k):	
					if(j != t):
						weight = Graph.node[t]['weight']
						distance = nx.shortest_path_length(Graph, t, k, 'length')
						sum = sum + (weight + distance)							
						cost.append(sum + G[q][k]) 
						F[q].append(cost)
print(G)					




# If the user does not provide integer n then read the GML file
if(n is None):
	try:
		Graph = nx.read_gml(file)
		print("GML file has been read")
	except:
		print(file + ": File cannot be read")
# If n is provided, construct the network
else:
	print("A random graph with " + str(n) + " nodes will be generated for you")
	Graph = initGraph(n, file)
	PMedian(Graph)
	

if(not isPath(Graph)):
	print("Your graph is not a simple path")
	exit()
	
if(not haveWeights(Graph)):
	print("Your graph has invalid weights")
	exit()

if(not haveLengths(Graph)):
	print("Your graph has invalid lengths")
	exit()



#def F(q,j):
#	if (q == 1):
#		for j in range(1, n):
#			for t in range(j to n):
#				sum = sum + d(vt, vk)
#	for j in range(1, n): 
#		for k in range(j, n):
#			for t in range(j, k):
#				sum = d(vt, vk) + G(q,k)
				
#				
#def G(q, j):
#	if (q == 1):
#		for j in range(1, n):
#			for t in range(j to n):
#				sum = sum + d(vt, vj)
#	for j in range(1, n):
#		for k in range((j+1), (n+1)):
#			for t in range(j, (k-1)):
#				sum = d(vt, vj) + F(q-1, k) 









