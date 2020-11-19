# ----------------------------------------------------------------------------
# Claire Fritzler
# CPSC 5110 - Intro to Facility Location
# Implementation of the 2-Median Algorithm
# Dr. Robert Benkoczi
# ----------------------------------------------------------------------------


import networkx as nx
import argparse
import os
from random import randint

# ----------------------------------------------------------------------------
# Function Definitions
# ----------------------------------------------------------------------------


# Check if the Graph is a Path
def isNotSimplePath(G, startNode, endNode):
    paths = list(nx.all_simple_paths(G, str(startNode), str(endNode)))
    if ((len(paths)) != 1):
       return False
    else:
       return True

# Check if the graph has proper weights and lengths
def allNodesHaveWeightsAndLengths(G):
    wrongLengthVals = False
    wrongWeightVals = False

    for source,target,edge in G.edges(data=True):
        if(not edge):
            return False
        elif(edge['length'] < 1):
            wrongLengthVals = True
            break

        for v in G.nodes():
            if(not G.node[v]['weight']):
                return False
            elif(edge['length'] < 1):
                wrongWeightVals = True
                break

    if(wrongLengthVals):
        print("A length between vertices exists that is less than 1, exiting!")
        return False

    if(wrongWeightVals):
        print("A weight for a node exists that is less than 1, exiting!")
        return False

    return True

# Initialize the graph
def initializeNewRandomGraphWithFile(n):

    n = int(n)
    G = nx.path_graph(n)
    print("Note: Smallest weight/length starts at 1.")

    largestWeight = input("Please enter the largest random weight that can be assigned: ")
    largestWeight = str(largestWeight)
    while (not (largestWeight.isdigit())):
        print("Sorry largestWeight is not an integer try again!")
        largestWeight = input("Please enter the largest random weight that can be assigned: ")
        largestWeight = str(largestWeight)
        largestWeight = largestWeight.strip()
        if (largestWeight == "no"):
            exit()

    largestLength = input("Please enter the largest random length that can be assigned: ")
    largestLength = str(largestLength)
    while (not (largestLength.isdigit())):
        print("Sorry largestWeight is not an integer try again!")
        largestLength = input("Please enter the largest random length that can be assigned: ")
        largestLength = str(largestLength)
        largestLength = largestLength.strip()
        if (largestLength == "no"):
            exit()

    count = 0
    largestWeight = int(largestWeight)
    largestLength = int(largestLength)

    while (count < (n - 1)):

        randWeight = randint(1, largestWeight)
        G.node[count]['weight'] = randWeight

        randLength = randint(1, largestLength)
        G[count][count+1]['length'] = randLength

        count = count + 1

    randWeight = randint(1, largestWeight)
    G.node[n-1]['weight'] = randWeight

    # We are now done making our graph, write it out.
    nx.write_gml(G, "file.gml")
    return G

#########################################################################################
# ----------------------------------------------------------------------------
# Algorithm Implementation
# ----------------------------------------------------------------------------

# parse the input
parser = argparse.ArgumentParser(description='___________Calculate the 1-median___________')
parser.add_argument('-n', nargs='?', type=int, help='Specifies the number of nodes needed on the path')
parser.add_argument('file', type=str, help='Specifies the GML file used')
args = parser.parse_args()
n = args.n
file = args.file

createNewFile = False
# If n does not exist read from a file
if(n is None):

    # If there is still nothing in the file.
    if(os.stat(file).st_size == 0):
        print("There are no contents in the file " + file + " ... A new file will now be created.")
        n = input("Please enter an n value to specify the number of nodes for a new graph, or type \"no\" to quit: ")

        while (not (n.isdigit())):
            print("Sorry n is not an integer try again!")
            n = input("Please enter an n value to specify the number of nodes for a new graph, or type \"no\" to quit: ")
            n = n.strip()
            if (n == "no"):
                exit()
        G = initializeNewRandomGraphWithFile(n)

    # If the file is filled
    else:
        try:
            G = nx.read_gml(file)
            print("GML file has been read successfully!")

        # If the file is filled and still cannot be read in properly (i.e. perhaps the wrong extension is used)
        except:
            print("GML file: " + file + " cannot be read ... A new file will now be created.")
            n = input("Please enter an n value to specify the number of nodes for a new graph, or type \"no\" to quit: ")

            while (not (n.isdigit())):
                print("Sorry n is not an integer try again!")
                n = input("Please enter an n value to specify the number of nodes for a new graph, or type \"no\" to quit: ")
                n = n.strip()
                if (n == "no"):
                    exit()
            G = initializeNewRandomGraphWithFile(n)

# Since n exists we generate a path with a value of n nodes.
# Lengths and weights are set randomly
# Save it to "file" overwriting it. Store lengths and weights.
else:
    G = initializeNewRandomGraphWithFile(n)
    # This is so that when the graph is read back in it follows
    # the same format as if it were to be read and checked like a file
    # That's why the temp file is immediately removed.  This saved me
    # from converting all of the types in the path_graph data structure
    # into basic data types.
    nx.write_gml(G, "temp.gml")
    G = nx.read_gml("temp.gml")
    os.remove("temp.gml")


# Check if the graph is a path
if (not (isNotSimplePath(G, 0, len(G) - 1))):
    print("Graph input from file is not a simple path, exiting!")
    exit()

# Check if the graph has nodes without weight and length
if (not allNodesHaveWeightsAndLengths(G)):
    print("Not all nodes have correctly set weight and length attributes")
    print("Script will now quit")
    exit()

nx.write_gml(G, file)


# Implement the 1-median by brute force

facilityCosts = []
for facility in G.nodes():
    facilitySum = 0
    for customer in G.nodes():
        if(customer != facility):
            weight = G.node[customer]['weight']
            distance = nx.shortest_path_length(G,source=customer, target=facility,  weight='length')
            facilitySum = (facilitySum + (weight * float(distance)))

    facilityCosts.append((facilitySum, facility))

minTuple = min(facilityCosts, key=lambda t: (t[0]))
print("The cost for 1-median is: " + str(minTuple[0]))
print("The ID of the 1-median node is: " + str(minTuple[1]))
