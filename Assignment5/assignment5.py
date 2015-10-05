#Emma Montross
#Program Assignment 2

import sys
import heapq
import math

def getWorld(filename):
	infile = open(filename,"r")
	world = []
	line = infile.readline()
	while line != "":
		world.append(line.split())
		line = infile.readline()
	for i in range(0,len(world)):
		for j in range(0,len(world[i])):
			world[i][j] = Node(i,j,int(world[i][j]))
	return world
	
def calcDistance(x1,y1,x2,y2,typ):
	return 10 + int(x1 != x2 and y1 != y2) * 4 + typ * 10

class Node:
	def __init__(self,x,y,typ):
		self.x = x
		self.y = y
		self.utility = 0
		self.typ = typ
		
class Value:
	def __init__(self,world):
		self.world = world


filename = sys.argv[1]
h = int(sys.argv[2])
world = getWorld(filename)
