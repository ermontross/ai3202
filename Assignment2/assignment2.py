#Emma Montross
#Program Assignment 2

import sys

filename = sys.argv[1]
h = sys.argv[2]
infile = open(filename,"r")
worldMatrix = [ map(int,line.split(' ')) for line in f ]
endLocX = 0
endLocY = 9

openList = []
#closedList = []


class Node():
	def __init__(x,y,dist,parent):
		self.x = x
		self.y = y
		self.distanceToStart = dist
		self.parent = parent
		self.adj = []

def AStar(start,end):
	openList.append(start)
	closedList = []
	while !(not openList):
		node = minCostNode
		openList.remove(node)
		if node.x != endLocX or node.y != endLocY:
			closedList.append(node)
			for n in node.adj:
				#calc f(n)
				n.parent = node
				if n in openList:
					#replace if f(n) lower than existing f(n) for n
				else:
					openList.append(n)
		else:
			break
				
		
def minCostNode():
	min = 10000000
	for i in range(0,openList.size()):
		if openList[i].f < min:
			min = openList[i].f
			minNode = openList[i]
	return minNode
	
def calcHeuristic(node):
	return endLocX - node.x + endLocY - node.y
	
def calcDistToStart(node):
	
