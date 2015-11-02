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
	print numbers
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

class Samples:
	def __init__(self,numbers,bayes,v,s):
		#list of numbers from the input file
		self.numbers = numbers
		#dictionary of nodes for bayesian network
		self.bayes = bayes
		#2D array of generated samples
		self.samples = []
		#number of samples
		self.numS = s
		#number of variables in the bayesian network
		self.numV = v
	
	'''this function generates a 2D array of samples
		determines whether cloudy is true or false
		based off of that, determines rain and sprinklers
		based off of those values, determines wet grass'''
	def generate_samples(self):		
		for i in range(0,self.numS-1):
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
		print self.samples
		
	def prior_c(self,rain):
		#rain is true or false
				

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("filename", help = "name of the text file that defines the world")
	args = parser.parse_args()
	
	numbers = read_file(args.filename)
	bayes = generate_bayes()
	
	#four variables, 25 samples (4 random numbers per sample, 100 random numbers, 25 samples)
	s = Samples(numbers,bayes,4,25)
	s.generate_samples()
	

if __name__ == "__main__":
	main()
	
