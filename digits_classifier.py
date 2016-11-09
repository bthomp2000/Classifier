from copy import deepcopy
K=1.0
# 0 is white, 1 is gray, 2 is black
trainingData = list() #[class][row][col][whitePerc,grayPerc,BlackPerc]

classCount = [0] * 10
traininglabels = []
testlabels = []
resultlabels = []
def readInput():
	with open('digitdata/traininglabels') as input_file:
			for i, line in enumerate(input_file):
				line = line.rstrip()
				for label in line:
					traininglabels.append(int(label))

	with open('digitdata/trainingimages') as input_file:
		imageNum = 0
		count = 0
		for intputLineNum, line in enumerate(input_file):
			currRow = intputLineNum % 28
			imageNum = int(intputLineNum / 28)
			if currRow == 0:
				trueNumber = traininglabels[imageNum] #0-9
				classCount[trueNumber]+=1.0
			for currCol in range(len(line)):
				count+=1
				feature = line[currCol]
				if feature == "#":
					trainingData[trueNumber][currRow][currCol][0]+=1.0
				elif feature == "+":
					trainingData[trueNumber][currRow][currCol][1]+=1.0
				elif feature == " ":
					trainingData[trueNumber][currRow][currCol][2]+=1.0

def readTestInput():
	with open('digitdata/testlabels') as input_file:
			for i, line in enumerate(input_file):
				line = line.rstrip()
				for label in line:
					testlabels.append(int(label))

	with open('digitdata/testimages') as input_file:
		imageNum = 0
		classProb = [1] * 10
		for intputLineNum, line in enumerate(input_file):
			currRow = intputLineNum % 28
			imageNum = int(intputLineNum / 28)
			for currCol in range(len(line)):
				feature = line[currCol]
				for i in range(len(classProb)):
					if feature == "#":
						classProb[i]*=trainingData[i][currRow][currCol][0]
					elif feature == "+":
						classProb[i]*=trainingData[i][currRow][currCol][1]
					elif feature == " ":
						classProb[i]*=trainingData[i][currRow][currCol][2]
			if currRow == 27:
				maxIndex = classProb.index(max(classProb))
				resultlabels.append(int(maxIndex))
				classProb = [1] * 10

def numCorrect():
	count = 0.0
	for i in range(len(resultlabels)):
		if resultlabels[i] == testlabels[i]:
			count += 1
	print count/len(resultlabels)

def initArray():
	colors = [K] * 3
	twodim = list()
	for i in range(28):
		temp = list()
		for j in range(28):
			temp.append(deepcopy(colors))
		twodim.append(deepcopy(temp))
	for i in range(10):
		trainingData.append(deepcopy(twodim))

def normalize():
	for i in range(10):
		for j in range(28):
			for k in range(28):
				for l in range(3):
					trainingData[i][j][k][l]=float(trainingData[i][j][k][l]/((3.0*K)+classCount[i]))

initArray()
readInput()
normalize()
readTestInput()
numCorrect()
# print resultlabels
# print trainingData[2]
# print classCount