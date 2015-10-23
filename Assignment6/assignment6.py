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
	
def calc_marginal(bayes,a):
	node = bayes[a]
	
	return 0
		
def calc_joint(bayes):
	return 0
		
def calc_conditional(bayes):
	return 0

def set_prior(bayes,node,prob):
	bayes[node].set_prob(prob)
	print "changed prior"
	return 0
	
def generate_bayes():
	#add all of the known nodes
	#probabilites
	#conditionals
	#connections
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
			#calcConditional(a[:p], a[p+1:])
		elif o in ("-j"):
			print "flag", o
			print "args", a
		else:
			assert False, "unhandled option"

if __name__ == "__main__":
	main()
	
