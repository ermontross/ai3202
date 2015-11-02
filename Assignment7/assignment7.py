#Assignment 7 - sampling
#CSCI 3202 - Intro to AI
#Emma Montross

import argparse

def read_file(filename):
	infile = open(filename,"r")
	numbers = []
	line = infile.readline()
	while line != "":
		numbers.append(int(line))
		line = infile.readline()
	return numbers

def generate_bayes():
	bayes = dict()
	bayes['C'] = Node("cloudy",0.5)
	bayes['S'] = Node("sprinkler",{'c':0.1,'~c':0.5})
	bayes['R'] = Node("rain",{'c':0.8,'~c':0.2})
	bayes['W'] = Node("wet grass",{'sr':0.99,'s~r':0.9,'~sr':0.9,'~s~r':0.0})
	return bayes

class Node:
	def __init__(self,name,prob):
		self.name = name
		self.prob = prob

class Samples:
	def __init__(self,numbers,bayes,v,s):
		self.numbers = numbers
		self.bayes = bayes
		self.samples = [s][v]
		self.numS = s
		self.numV = v
	
	def generate_samples(self):
		#determine if cloudy is true or false
		#based on that, determine sprinklers and rain (independent)
		#based on sprinklers and rain, determine wet grass
		#four numbers per sample, so 25 samples
		
		for i in range(0,self.numS-1):
			#getting random numbers from list
			cloudy = self.numbers.pop()
			sprinkler = self.numbers.pop()
			rain = self.numbers.pop()
			wetgrass = self.numbers.pop()
			
			#determine if cloudy is true or false
			#cloudy true
			if cloudy < self.bayes['C'].prob:
				self.samples[i][0] = 1
				#sprinkler true or false
				if sprinkler < self.bayes['S'].prob['c']:
					self.samples[i][1] = 1
					sprinkler = True
				else:
					self.samples[i][1] = 0
					sprinkler = False
				#rain true or false
				if rain < self.bayes['R'].prob['c']:
					self.samples[i][2] = 1
					rain = True
				else:
					self.samples[i][2] = 0
					rain = False
			#cloudy false
			else:
				self.samples[i][0] = 0
				#sprinkler true or false
				if sprinkler < self.bayes['S'].prob['~c']:
					self.samples[i][1] = 1
					sprinkler = True
				else:
					self.samples[i][1] = 0
					sprinkler = False
				#rain true or false
				if rain < self.bayes['R'].prob['~c']:
					self.samples[i][2] = 1
					rain = True
				else:
					self.samples[i][2] = 0
					rain = False
			
			#determining wet grass based on sprinkler and rain
			if sprinkler:
				if rain:
					if wetgrass < self.bayes['W'].prob['sr']:
						self.samples[i][3] = 1
					else:
						self.samples[i][3] = 0
				else:
					if wetgrass < self.bayes['W'].prob['s~r']:
						self.samples[i][3] = 1
					else:
						self.samples[i][3] = 0
			else:
				if rain:
					if wetgrass < self.bayes['W'].prob['~sr']:
						self.samples[i][3] = 1
					else:
						self.samples[i][3] = 0
				else:
					if wetgrass < self.bayes['W'].prob['~s~r']:
						self.samples[i][3] = 1
					else:
						self.samples[i][3] = 0
				

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("filename", help = "name of the text file that defines the world")
	args = parser.parse_args()
	
	numbers = read_file(args.filename)
	bayes = generate_bayes()
	
	#four variables, 25 samples (4 random numbers per sample, 100 random numbers, 25 samples)
	s = Samples(numbers,bayes,4,25)
	

if __name__ == "__main__":
	main()
	
