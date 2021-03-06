from copy import deepcopy
from math import log
from graphics import *
import colorsys

K=0.2
# 0 is white, 1 is gray, 2 is black
trainingData = list() #[class][row][col][whitePerc,grayPerc,BlackPerc]

classCount = [0] * 10
traininglabels = []
testlabels = []
resultlabels = []
results = [0]*10
testcount = [0.0] * 10
confusion = []
pairs = []
prototypicals = [] #[class][min_index,min_value,max_index,max_value]
testImages = []
def readInput():
	with open('digitdata/traininglabels') as input_file:
			for i, line in enumerate(input_file):
				line = line.rstrip()
				for label in line:
					traininglabels.append(int(label))
			for i in range(10):
				prototypicals.append(list([0,9999999.0,0,-999999.9]))

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
		classProb = [0.0] * 10
		for i in range(10):
			classProb[i]=float(classCount[i]/5000.0)
		testimage = []
		for intputLineNum, line in enumerate(input_file):
			currRow = intputLineNum % 28
			imageNum = int(intputLineNum / 28)
			testimage.append(line)
			for currCol in range(len(line)):
				feature = line[currCol]
				for i in range(len(classProb)):
					if feature == "#":
						classProb[i]+=log(trainingData[i][currRow][currCol][0])
					elif feature == "+":
						classProb[i]+=log(trainingData[i][currRow][currCol][1])
					elif feature == " ":
						classProb[i]+=log(trainingData[i][currRow][currCol][2])
			if currRow == 27:
				testImages.append(testimage)
				testimage=list()
				# [class][min_index,min_value,max_index,max_value]
				true_label = testlabels[imageNum]
				# print true_label
				prob_label = classProb[true_label]
				# print prob_label
				if prob_label<prototypicals[true_label][1]:
					prototypicals[true_label][0]=imageNum
					prototypicals[true_label][1]=prob_label
				if prob_label>prototypicals[true_label][3]:
					prototypicals[true_label][2]=imageNum
					prototypicals[true_label][3]=prob_label
				maxIndex = classProb.index(max(classProb))
				if imageNum==58:
					print "max Index: ",maxIndex
				resultlabels.append(int(maxIndex))
				classProb = [1] * 10

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


def numCorrect():
	count = 0.0
	for i in range(10):
		temp = [0.0] * 10
		confusion.append(deepcopy(temp))
	for i in range(len(resultlabels)):
		testcount[testlabels[i]]+=1.0
		if resultlabels[i] == testlabels[i]:
			resultlabels[testlabels[i]]+=1.0
		confusion[testlabels[i]][int(resultlabels[i])]+=1.0

	for i in range(len(testcount)):
		results[i]/=testcount[i]
		for j in range(10):
			confusion[i][j]/=testcount[i]
	
	print "results for each class: "
	for i in range(len(results)):
		print format(results[i], '2.3f'),
	print ''
	# print testcount
	for i in range(10):
		for j in range(10):
			value = confusion[i][j]
			value=format(value, '2.3f')
			print value,
		print ''
	for i in range(len(resultlabels)):
		if resultlabels[i]==testlabels[i]:
			count+=1
	print "total accuracy: ",count/1000.0

def oddsRatios():
	for k in range(4):
		temp = [0]*2
		pairs.append(deepcopy(temp))
	for c in range(4):
		maxForThiscurrentc = 0.0
		for i in range(10):
			for j in range(10):
				if confusion[i][j]>maxForThiscurrentc and i != j:
					maxForThiscurrentc = confusion[i][j]
					pairs[c][0]=i
					pairs[c][1]=j
		confusion[pairs[c][0]][pairs[c][1]]=-10.0
	print pairs

def printGraphics():
	for pair in pairs:
		win = GraphWin("Feature Likelihood for "+str(pair[0])+" and "+str(pair[1]), 900, 300)
		for i in range(28):
			for j in range(28):
				digitClass = pair[0]
				featurelikelyhood1 = trainingData[digitClass][j][i][0]+trainingData[digitClass][j][i][1]
				hue = (1-featurelikelyhood1) * 0.67
				rect = Rectangle(Point(i*10, j*10), Point((i*10)+10, (j*10)+10))
				color = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
				color = color_rgb(255*color[0],255*color[1],255*color[2])
				rect.setFill(color)
				rect.draw(win)

				digitClass = pair[1]
				featurelikelyhood2 = trainingData[digitClass][j][i][0]+trainingData[digitClass][j][i][1]
				hue = (1-featurelikelyhood2) * 0.67
				rect = Rectangle(Point(i*10+300, j*10), Point((i*10)+10+300, (j*10)+10))
				color = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
				color = color_rgb(255*color[0],255*color[1],255*color[2])
				rect.setFill(color)
				rect.draw(win)

				odds = log(featurelikelyhood1)-log(featurelikelyhood2)
				# print "odds: ",odds, " = ",featurelikelyhood1,"/",featurelikelyhood2
				if(odds>5.0):
					odds=5.0
				elif(odds<-5.0):
					odds=-5.0
				odds = (odds + 5.0)/10.0
				hue = (1-odds) * 0.67
				rect = Rectangle(Point(i*10+600, j*10), Point((i*10)+10+600, (j*10)+10))
				color = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
				color = color_rgb(255*color[0],255*color[1],255*color[2])
				rect.setFill(color)
				rect.draw(win)

	while True:
		x = 0

#[class][min_index,min_value,max_index,max_value]
def prototypicalResults():
	for i in range(10):
		minIndex = int(prototypicals[i][0])
		maxIndex = int(prototypicals[i][2])
		print "Class ",i,": lowest probability (image number ",minIndex,")"
		for line in testImages[minIndex]:
			line = line.rstrip()
			print line
		print ''
		print "Highest probability (image number ",maxIndex,")"
		for line in testImages[maxIndex]:
			line = line.rstrip()
			print line
		print ''
initArray()
readInput()
normalize()
readTestInput()
numCorrect()
oddsRatios()
printGraphics()
prototypicalResults()
print prototypicals
# print resultlabels
# print trainingData[2]
# print classCount