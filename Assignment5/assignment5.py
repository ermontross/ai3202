#Emma Montross
#Program Assignment 5
#value iteration 

import argparse
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

class Node:
	def __init__(self,x,y,value):
		self.x = x
		self.y = y
		self.typ = value
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
	def __init__(self,world,e,dis):
		#2D world matrix as made by getWorld
		self.world = world
		#epsilon as set by user
		self.e = float(e)
		#discount as given in assignment
		self.discount = float(dis)
	
	#determines if node is in bounds and not a wall and returns the node		
	def getNode(self,x,y):
		if((x<0) or (y<0) or (x>len(self.world)-1) or (y>len(self.world[0])-1) or (self.world[x][y].typ == 2)):
			return None
		else:
			return world[x][y]
			
	def getUtil(self,x,y):
		if((x<0) or (y<0) or (x>len(self.world)-1) or (y>len(self.world[0])-1) or (self.world[x][y].typ == 2)):
			return float("-inf")
		else:
			return self.world[x][y].utility
			
	#goes through the world matrix, setting utilities along the way, until delta < e*(1-discount)/discount	
	def setUtilities(self):
		#value to test delta against
		test = self.e*(1-self.discount)/self.discount
		#delta that is used to test when utilities are done being calculated (max change in utilities)
		delta = 100
		while(delta >= test):
			delta = -100
			for i in range(0,len(self.world)):
				for j in range(0,len(self.world[0])):
					current = self.getNode(i,j)
					if(current != None and current.reward != 50):
						#if the current node is valid, get its adjacent nodes
						right = self.getNode(i+1,j)
						left = self.getNode(i-1,j)
						up = self.getNode(i,j+1)
						down = self.getNode(i,j-1)
						
						if(right == None):
							right = current
						if(left == None):
							left = current
						if(up == None):
							up = current
						if(down == None):
							down = current
						
						#get the right, left, up, and down movement values
						rvalue = 0.8*right.utility + 0.1*up.utility + 0.1*down.utility
						lvalue = 0.8*left.utility + 0.1*up.utility + 0.1*down.utility
						uvalue = 0.8*up.utility + 0.1*right.utility + 0.1*left.utility
						dvalue = 0.8*down.utility + 0.1*right.utility + 0.1*left.utility
						
						#get previous utility for delta calculation
						prevUtility = current.utility
						
						#calculate new utility
						current.utility = self.discount * (current.reward + max(rvalue,lvalue,uvalue,dvalue))
					
						if(abs(current.utility - prevUtility) > delta):
							delta = abs(current.utility - prevUtility)
							
	def printUtilities(self):
		for i in range(0,len(self.world)):
			for j in range(0,len(self.world[0])):
				print i,",", j
				print self.world[i][j].utility
	
	def findPath(self):
		self.setUtilities()
		#self.printUtilities()
		
		#start at bottom left corner
		current = self.getNode(len(self.world)-1,0)
		
		while(current.reward != 50):
			#print current info
			print "Location: (",current.x,",",current.y,")"
			print "Utility: ", current.utility
			#get adjacent utilities
			right = self.getUtil(current.x+1,current.y)
			left = self.getUtil(current.x-1,current.y)
			up = self.getUtil(current.x,current.y+1)
			down = self.getUtil(current.x,current.y-1)
			
			#choose max of adjacents for new current
			maxUtility = max(right,left,up,down)
			if(maxUtility == right):
				current = self.getNode(current.x+1,current.y)
			elif(maxUtility == left):
				current = self.getNode(current.x-1,current.y)
			elif(maxUtility == up):
				current = self.getNode(current.x,current.y+1)
			else:
				current = self.getNode(current.x,current.y-1)
		
		#when reached end, print last node's info
		print "Location: (",current.x,",",current.y,")"
		print "Utility:", current.utility

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("filename", help = "name of the text file that defines the world")
	parser.add_argument("epsilon", help = "value of epsilon you wish to use")
	args = parser.parse_args()
	
	world = getWorld(args.filename)
	valueIteration = Value(world,args.epsilon,0.9)
	valueIteration.findPath()
	#valueIteration.setUtilities()
	#valueIteration.printUtilities()
	
