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
		self.cost = 0
		self.parent = None
		self.f = 0
		self.typ = typ
	
	def setParent(self, newParent, h):
		self.parent = newParent
		self.cost = newParent.cost + calcDistance(self.x, self.y, newParent.x, newParent.y, self.typ)
		self.f = self.cost + h(self.x,self.y)

class AStar:
	def __init__(self,world,h):
		#lists
		self.openList = []
		self.closedList = []
		#end coordinates
		self.endX = 0
		self.endY = len(world[0]) - 1
		#world aka maze the horse goes through
		self.world = world
		#turn the openList into a heap
		heapq.heapify(self.openList)
		#set heuristic depending on user's input
		if(h == 1):
			self.heuristic = self.manhattan
		else:
			self.heuristic = self.other
		#start in the lower left corner
		self.start = world[len(world) - 1][0]
		
	#manhattan heuristic - only vertical and horizontal movements
	def manhattan(self,x,y):
		return abs(x - self.endX) + abs(y - self.endY)
		
	#straight-line distance formula
	def other(self,x,y):
		return math.sqrt((x - self.endX)**2 + (y - self.endY)**2)
		
	#get all adjacent nodes
	def getAdj(self,node):
		adj = []
		for i in range(node.x - 1, node.x + 2):
			for j in range(node.y - 1, node.y + 2):
				#making sure we are within the world bounds and not evaluating our current node
				if(i >= 0 and i < len(self.world) and j >= 0 and 
				j < len(self.world[i]) and not(i == node.x and j == node.y)):
					#if the node is not a wall, append it to the adj list
					if(world[i][j].typ != 2):
						adjnode = world[i][j]
						adj.append(adjnode)
		return adj
		
	#print final path by traversing backwards from end using parent nodes
	def printPath(self,node):
		cost = 0
		while not(node.x == self.start.x and node.y == self.start.y):
			print "(",node.x,",",node.y,")"
			cost += calcDistance(node.x,node.y,node.parent.x,node.parent.y,node.typ)
			node = node.parent
		print "(",node.x,",",node.y,")"
		print "Total cost: ", cost
		
	#a* search
	def aSearch(self):
		#push the starting node onto the open list heap
		heapq.heappush(self.openList, (self.start.f, self.start))
		#number of locations evaluated
		numLoc = 0
		#while the open list is not empty
		while(len(self.openList) > 0):
			#pop the first node off the list and get it and its f value
			f, node = heapq.heappop(self.openList)
			#increment the number of locations evaluated
			numLoc += 1
			#add the node evaluated to the closed list
			self.closedList.append(node)
			#if we have reached the end of the maze, print the path and the number of locations evaluated
			if(node.x == self.endX and node.y == self.endY):
				self.printPath(node)
				print "locations evaluated: ", numLoc
				break;
			#get adjacent nodes
			adjNodes = self.getAdj(node)
			for n in adjNodes:
				if not(n in self.closedList):
					if((n.f, n) in self.openList):
						#if f(n) is lower than exisiting f(n) for n, keep it on the closed list
						if(n.cost > node.cost + calcDistance(n.x,n.y,node.x,node.y,n.typ)):
							n.setParent(node, self.heuristic)
					#otherwise, push the node to the open list heap
					else:
						n.setParent(node,self.heuristic)
						heapq.heappush(self.openList, (n.f,n))


filename = sys.argv[1]
h = sys.argv[2]
world = getWorld(filename)
aStar = AStar(world,h)
aStar.aSearch()
