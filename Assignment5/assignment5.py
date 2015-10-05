#Emma Montross
#Program Assignment 5
#value iteration 

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
	def __init__(self,x,y,value):
		self.x = x
		self.y = y
		#determine utility and reward based on value of sqaure in world matrix
		if(value == 0):
			#open square
			self.reward = 0
			self.utility = 0
		elif(value == 1):
			#mountain
			self.reward = -1
			self.utility = -1
		elif(value == 2):
			#wall
			self.reward = None
			self.utility = None
		elif(value == 3):
			#snake
			self.reward = -2
			self.utility = -2
		elif(value == 4):
			#barn
			self.reward = 1
			self.utility = 1
		elif(value == 50):
			#goal square
			self.reward = 50
			self.utility = 50
		
class Value:
	def __init__(self,world):
		self.world = world


filename = sys.argv[1]
e = float(sys.argv[2]) #epsilon 
world = getWorld(filename)
