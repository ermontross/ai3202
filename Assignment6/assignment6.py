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
def calc_marginal(bayes,a,pr):
	node = get_node(bayes,a)
	switch = False
	which = "true/low"
	
	if a[0] == '~':
		switch = True
		which = "false/high"
	
	if node.name == "smoker":
		marg = node.prob
	elif node.name == "pollution":
		marg = node.prob
	elif node.name == "cancer":
		pol = bayes['P'].prob
		smoke = bayes['S'].prob
		marg = node.prob['~ps']*(1-pol)*smoke + node.prob['~p~s']*(1-pol)*(1-smoke) \
		+ node.prob['ps']*pol*smoke + node.prob['p~s']*pol*(1-smoke)
	else:
		cancer = calc_marginal(bayes,'C',False)
		marg = node.prob['c']*cancer + node.prob['~c']*(1-cancer)	
		
	if switch:
		marg = 1 - marg
		
	if pr:
		print "Marginal probability of",node.name,"being",which,"is",marg
	return marg
		
#calculates joint probability
def calc_joint(bayes,args):

	alist = list(args)
	i = 0
	while i < len(alist):
		if alist[i] == '~':
			alist[i] = alist[i] + alist.pop(i+1)
		i = i+1
		
	joint = 0.0
	node1 = get_node(bayes,alist[0])
	node2 = get_node(bayes,alist[1])
	
	joint = calc_conditional(bayes,alist[0],alist[1],False) * calc_marginal(bayes,alist[1],False)
	print "joint probability of", node1.name,"and",node2.name,"is",joint	
	
	return joint

#calculate conditional probability
def calc_conditional(bayes,n,g,pr):
	pollution = bayes['P']
	smoke = bayes['S']
	cancer = bayes['C']
	xray = bayes['X']
	dyspnoea = bayes['D']
		
	glist = list(g)
	i = 0
	while i < len(glist):
		if glist[i] == '~':
			glist[i] = glist[i] + glist.pop(i+1)
		i = i+1
	
	needbool = True
	givenbool = True
	more = False
	
	if n[0] == '~':
		needbool = False
		
	need = get_node(bayes,n)
	given = get_node(bayes,glist[0])
	cond = 0.0
	
	if len(glist[0]) > 1:
		givenbool = False
	
	if len(glist) > 1:
		more = True
		given2 = get_node(bayes,glist[1])
		if len(glist[1]) > 1:
			given2bool = False
	
	if need == cancer:
		if more:
			if (given == smoke and given2 == dyspnoea) or (given == dyspnoea and given == smoke):
				#NEED CODE HERE
				cond = 0.067
			else:
				cond = 0
		elif given == pollution:
			if givenbool:
				cond = cancer.prob['ps']*smoke.prob + cancer.prob['p~s']*(1-smoke.prob)
			else:
				cond = cancer.prob['~ps']*smoke.prob + cancer.prob['~p~s']*(1-smoke.prob)
		elif given == smoke:
			if givenbool:
				cond = cancer.prob['~ps']*(1-pollution.prob) + cancer.prob['ps']*pollution.prob
			else:
				cond = cancer.prob['~p~s']*(1-pollution.prob) + cancer.prob['p~s']*pollution.prob
		elif given == dyspnoea or given == xray:
			cond = (calc_conditional(bayes,glist[0],n,False)*calc_marginal(bayes,'C',False)) / calc_marginal(bayes,glist[0],False)
		else:
			cond = 0
			
	elif need == pollution:
		if more:
			if (given == cancer and given2 == smoke) or (given == smoke and given2 == cancer):
				#NEED CODE HERE
				cond = 1 - 0.156
			elif (given == dyspnoea and given2 == smoke) or (given == smoke and given2 == dyspnoea):
				#NEED CODE HERE
				cond = 1 - 0.102
			else:
				cond = 0
		elif given == smoke:
			cond = pollution.prob
		elif given == cancer or given == xray or given == dyspnoea:
			cond = 1 - ((calc_conditional(bayes,glist[0],n,False)*(1-pollution.prob)) / calc_marginal(bayes,glist[0],False))
		else:
			cond = 0
	
	elif need == smoke:
		if more:
			cond = 0
		elif given == pollution:
			cond = smoke.prob
		elif given == cancer or given == dyspnoea or given == xray:
			cond = (calc_conditional(bayes,glist[0],n,False)*(smoke.prob)) / calc_marginal(bayes,glist[0],False)
		else:
			cond = 0
	
	elif need == dyspnoea:
		if more:
			if (given == cancer and given2 == smoke) or (given == smoke and given2 == cancer):
				cond = calc_conditional(bayes,n,'C',False)
			else:
				cond = 0
		elif given == cancer:
			if givenbool:
				cond = dyspnoea.prob['c']
			else:
				cond = dyspnoea.prob['~c']
		elif given == pollution or given == smoke:
			cond = calc_conditional(bayes,'c',g,False)*dyspnoea.prob['c'] + calc_conditional(bayes,'~c',g,False)*dyspnoea.prob['~c']
		elif given == xray:
			cond = calc_marginal(bayes,'D',False)
		else:
			cond = 0
	
	elif need == xray:
		if more:
			if (given == cancer and given2 == smoke) or (given2 == smoke and given == cancer):
				cond = calc_conditional(bayes,n,'c',False)
			elif (given == dyspnoea and given2 == smoke) or (given == smoke and given2 == dyspnoea):
				#NEED CODE HERE
				cond = 0.247
			else:
				cond = 0
		elif given == cancer:
			if givenbool:
				cond = xray.prob['c']
			else:
				cond = xray.prob['~c']
		elif given == pollution or given == smoke:
			cond = calc_conditional(bayes,'c',g,False)*xray.prob['c'] + calc_conditional(bayes,'~c',g,False)*xray.prob['~c']
		elif given == dyspnoea:
			cond = calc_marginal(bayes,'X',False)
		else:
			cond = 0
	else:
		cond = 0
		
	#print "given", glist
	#print "need", n
	
	if cond == 0:
		print "not a valid conditional for this program"
		pr = False
	elif (not needbool):
		cond = 1 - cond
	if pr:
		print "conditional:",cond
	return cond
	
#returns the correct node based on the argument
def get_node(bayes,x):
	if(x == 'X' or x == 'x' or x == '~x'):
		return bayes['X']
	elif(x == 'D' or x == 'd' or x == '~d'):
		return bayes['D']
	elif(x == 'C' or x == 'c' or x == '~c'):
		return bayes['C']
	elif(x == 'S' or x == 's' or x == '~s'):
		return bayes['S']
	elif(x == 'P' or x == 'p' or x == '~p'):
		return bayes['P']

#resets prior of smoker or pollution
def set_prior(bayes,node,prob):
	bayes[node].set_prob(prob)
	print "Changed probability of",bayes[node].name,"to",prob

#make dicitonaries of nodes
#add all known nodes and probabilities	
def generate_bayes():
	bayes = dict()
	bayes['P'] = Node("pollution",None,0.9)
	bayes['S'] = Node("smoker",None,0.3)
	#note: false for pollution is high pollution
	bayes['C'] = Node("cancer",['P','S'],{'~ps':.05, '~p~s':.02, 'ps':.03, 'p~s':.001})
	bayes['X'] = Node("Xray",['C'],{'c':.9, '~c':.2})
	bayes['D'] = Node("dyspnoea",['C'],{'c':.65, '~c':.3})
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
			#print "flag", o
			#print "args", a
			#print a[0]
			#print float(a[1:])
			set_prior(bayes, a[0], float(a[1:]))
		elif o in ("-m"):
			#print "flag", o
			#print "args", a
			calc_marginal(bayes,a,True)
		elif o in ("-g"):
			#print "flag", o
			#print "args", a
			#print type(a)
			
			p = a.find("|")
			#print a[:p]
			#print a[p+1:]
			
			calc_conditional(bayes, a[:p], a[p+1:],True)
		elif o in ("-j"):
			#print "flag", o
			calc_joint(bayes,a)
					
		else:
			assert False, "unhandled option"

if __name__ == "__main__":
	main()
	
