#Assignment 6
#CSCI 3202 - Intro to AI
#Emma Montross

import argparse, getopt, sys

class Node():
	def __init__(self,name,parents,prob):
		self.name = name
		self.prob = prob
		self.parents = parents
	
	#sets the probability of the node
	def set_prob(self,p):
		self.prob = p
		
	#adds a parent
	def add_parent(self,parent):
		self.parent.append(parent)
	
#calculates marginal probability
#currently NOT COREECT
def calc_marginal(bayes,a):
	node = bayes[a]
	if a == "S" or a == "P":
		marg = node.prob
	else:
		marg = sum(node.prob.values())
	
	print "Marginal probability of",node.name,"is",marg
	return 0
		
#calculates joint probability
def calc_joint(bayes,args):
	return 0

#calculate conditional probability
def calc_conditional(bayes,need,given):
	return 0
	
#returns the correct node based on the argument
def get_node(bayes,x):
	if(x == 'X' or x == 'x' or x == '~x'):
		return bayes["X"]
	elif(x == 'D' or x == 'd' or x == '~d'):
		return bayes["D"]
	elif(x == 'C' or x == 'c' or x == '~c'):
		return bayes["C"]
	elif(x == 'S' or x == 's' or x == '~s'):
		return bayes["S"]
	elif(x == 'P' or x == 'p' or x == '~p'):
		return bayes["P"]

#resets prior of smoker or pollution
def set_prior(bayes,node,prob):
	bayes[node].set_prob(prob)
	print "changed prior"
	return 0

#make dicitonaries of nodes
#add all known nodes and probabilities	
def generate_bayes():
	bayes = dict()
	bayes["P"] = Node("pollution",None,0.9)
	bayes["S"] = Node("smoker",None,0.3)
	#note: false for pollution is high pollution
	bayes["C"] = Node("cancer",["P","S"],{'ft':.05, 'ff':.02, 'tt':.03, 'tf':.001})
	bayes["X"] = Node("Xray",["C"],{'t':.9, 'f':.2})
	bayes["D"] = Node("dyspnoea",["C"],{'t':.65, 't':.3})
	return bayes
	
def main():
	#build bayes net
	bayes = generate_bayes()
	
	# GETTING COMMAND LINE ARGUMENTS #
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)
	for o, a in opts:
		if o in ("-p"):
			print "flag", o
			print "args", a
			print a[0]
			print float(a[1:])
			set_prior(bayes, a[0], float(a[1:]))
		elif o in ("-m"):
			print "flag", o
			print "args", a
			print type(a)
			calc_marginal(bayes,a)
		elif o in ("-g"):
			print "flag", o
			print "args", a
			print type(a)
			'''you may want to parse a here and pass the left of |
			and right of | as arguments to calcConditional
			'''
			p = a.find("|")
			print a[:p]
			print a[p+1:]
			calc_conditional(bayes, a[:p], a[p+1:])
		elif o in ("-j"):
			print "flag", o
			alist = list(a)
			i = 0
			while i < len(alist):
				if alist[i] == '~':
					alist[i] = alist[i] + alist.pop(i+1)
				i = i+1
			print alist
			calc_joint(bayes,alist)
					
		else:
			assert False, "unhandled option"

if __name__ == "__main__":
	main()
	
