#Assignment 6
#CSCI 3202 - Intro to AI
#Emma Montross

class Node():
	def __init__(self,name):
		self.name = name
		self.prob = 0.0
		self.cprob = {}
	
	#sets the probability of the node
	def set_prob(self,p):
		self.prob = p
		
	#adds a conditional probability to the cprob dictionary
	def add_cprob(self,name,p):
		self.cprob[name] = p

def handle_args():
	#determine what program needs to do
	#return a value
	#that gets passed to the bayes net class
	
class Bayes():
	def __init__(self):
	
