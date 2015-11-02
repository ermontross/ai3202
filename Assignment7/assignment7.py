#Assignment 7 - sampling
#CSCI 3202 - Intro to AI
#Emma Montross

import argparse

#read the text file of numbers into a list
def read_file(filename):
	infile = open(filename,"r")
	numbers = []
	line = infile.readline()
	while line != "":
		numbers.append(float(line))
		line = infile.readline()
	return numbers

#generate the bayesian network
def generate_bayes():
	bayes = dict()
	bayes['C'] = Node("cloudy",0.5)
	bayes['S'] = Node("sprinkler",{'c':0.1,'~c':0.5})
	bayes['R'] = Node("rain",{'c':0.8,'~c':0.2})
	bayes['W'] = Node("wet grass",{'sr':0.99,'s~r':0.9,'~sr':0.9,'~s~r':0.0})
	return bayes

#nodes of the bayesian network
class Node:
	def __init__(self,name,prob):
		self.name = name
		self.prob = prob

class Prior:
	def __init__(self,num,bayes,s):
		#list of numbers from the input file
		self.numbers = []
		self.fill_list(self.numbers,num)
		#dictionary of nodes for bayesian network
		self.bayes = bayes
		#2D array of generated samples
		self.samples = []
		#number of samples
		self.numS = s
	
	def fill_list(self,num,filler):
		for item in filler:
			num.append(item)
	
	'''this function generates a 2D array of samples
		determines whether cloudy is true or false
		based off of that, determines rain and sprinklers
		based off of those values, determines wet grass'''
	def generate_samples(self):		
		for i in range(0,self.numS):
			#getting random numbers from list
			cloudy = self.numbers.pop()
			sprinkler = self.numbers.pop()
			rain = self.numbers.pop()
			wetgrass = self.numbers.pop()
			
			temp = []
			
			#determine if cloudy is true or false
			#cloudy true
			if cloudy < self.bayes['C'].prob:
				temp.append(1)
				#sprinkler true or false
				if sprinkler < self.bayes['S'].prob['c']:
					temp.append(1)
					sprinkler = True
				else:
					temp.append(0)
					sprinkler = False
				#rain true or false
				if rain < self.bayes['R'].prob['c']:
					temp.append(1)
					rain = True
				else:
					temp.append(0)
					rain = False
			#cloudy false
			else:
				temp.append(0)
				#sprinkler true or false
				if sprinkler < self.bayes['S'].prob['~c']:
					temp.append(1)
					sprinkler = True
				else:
					temp.append(0)
					sprinkler = False
				#rain true or false
				if rain < self.bayes['R'].prob['~c']:
					temp.append(1)
					rain = True
				else:
					temp.append(0)
					rain = False
			
			#determining wet grass based on sprinkler and rain
			if sprinkler:
				if rain:
					if wetgrass < self.bayes['W'].prob['sr']:
						temp.append(1)
					else:
						temp.append(0)
				else:
					if wetgrass < self.bayes['W'].prob['s~r']:
						temp.append(1)
					else:
						temp.append(0)
			else:
				if rain:
					if wetgrass < self.bayes['W'].prob['~sr']:
						temp.append(1)
					else:
						temp.append(0)
				else:
					if wetgrass < self.bayes['W'].prob['~s~r']:
						temp.append(1)
					else:
						temp.append(0)
			self.samples.append(temp)			
		
	def prior_c(self):
		numC = 0.0
		for i in range(0,self.numS):
			if self.samples[i][0] == 1:
				numC += 1
		return float(numC/self.numS)
		
	def prior_cgivenr(self):
		numR = 0.0
		numC = 0.0
		for i in range(0,self.numS):
			if self.samples[i][2] == 1:
				numR += 1
				if self.samples[i][0] == 1:
					numC += 1
		return numC/numR
		
	def prior_sgivenw(self):
		numS = 0.0
		numW = 0.0
		for i in range(0,self.numS):
			if self.samples[i][3] == 1:
				numW += 1
				if self.samples[i][1] == 1:
					numS += 1
		return numS/numW
		
	def prior_sgivencw(self):
		numCW = 0.0
		numS = 0.0
		for i in range(0,self.numS):
			if self.samples[i][0] == 1 and self.samples[i][3] == 1:
				numCW += 1
				if self.samples[i][1] == 1:
					numS += 1
		return numS/numCW
			
class Rejection:
	def __init__(self,num,bayes):
		#list of numbers from the input file
		self.numbers = []
		self.fill_list(self.numbers,num)
		self.numbers1 = []
		self.fill_list(self.numbers1,num)
		self.numbers2 = []
		self.fill_list(self.numbers2,num)
		#dictionary of nodes for bayesian network
		self.bayes = bayes
		#2D array of generated samples
	
	def fill_list(self,num,filler):
		for item in filler:
			num.append(item)
	
	def rej_c(self):
		samples = 0.0
		numC = 0.0
		while(self.numbers):
			samples += 1
			cloudy = self.numbers.pop()
			if cloudy < self.bayes['C'].prob:
				numC += 1
		return numC/samples
		
	def rej_cgivenr(self):
		numC = 0.0
		numR = 0.0
		while(self.numbers1):
			cloudy = self.numbers1.pop()
			rain = self.numbers1.pop()
			if cloudy < self.bayes['C'].prob:
				if rain < self.bayes['R'].prob['c']:
					numR += 1
					numC += 1
			else:
				if rain < self.bayes['R'].prob['~c']:
					numR += 1
		return numC/numR			
		
	def rej_sgivencw(self):
		numCW = 0.0
		numS = 0.0
		while(len(self.numbers2) >= 4):
			cloudy = self.numbers2.pop()
			if cloudy < self.bayes['C'].prob:
				sprinkler = self.numbers2.pop()
				rain = self.numbers2.pop()
				wetgrass = self.numbers2.pop()
				#sprinkler 
				if sprinkler < self.bayes['S'].prob['c']:
					sprinkler = True
				else:
					sprinkler = False
				#rain
				if rain < self.bayes['R'].prob['c']:
					rain = True
				else:
					rain = False

				
				if sprinkler:
					if rain:
						if wetgrass < self.bayes['W'].prob['sr']:
							numCW += 1
							numS += 1
					else:
						if wetgrass < self.bayes['W'].prob['s~r']:
							numCW += 1
							numS += 1
				else:
					if rain:
						if wetgrass < self.bayes['W'].prob['~sr']:
							numCW += 1
					else:
						if wetgrass < self.bayes['W'].prob['~s~r']:
							numCW += 1
		return numS/numCW	

def main():
	#command-line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("filename", help = "name of the text file that defines the world")
	args = parser.parse_args()
	
	#getting numbers from input file
	numbers = read_file(args.filename)
	#generating bayesian network
	bayes = generate_bayes()
	
	#four variables, 25 samples (4 random numbers per sample, 100 random numbers, 25 samples)
	#setting up prior samples
	s = Prior(numbers,bayes,25)
	s.generate_samples()
	
	#prior calculations
	priorc = s.prior_c()
	priorcr = s.prior_cgivenr()
	priorsw = s.prior_sgivenw()
	priorscw = s.prior_sgivencw()
	print ""
	print "PRIOR PROBABILITIES"
	print "P(c):",priorc
	print "P(c|r):",priorcr
	print "P(s|w):",priorsw
	print "P(s|c,w):",priorscw
	print ""
	
	#rejection sampling
	r = Rejection(numbers,bayes)
	rejc = r.rej_c()
	rejcr = r.rej_cgivenr()
	rejscw = r.rej_sgivencw()
	
	print "REJECTION PROBABILITIES"
	print "P(c):",rejc
	print "P(c|r):",rejcr
	print "P(s|w):",priorsw #prior and rejection will be the same for s given w
	print "P(s|c,w):",rejscw
	print ""

if __name__ == "__main__":
	main()
	
