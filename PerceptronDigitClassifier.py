from random import randint
from copy import deepcopy


K=0.2
# 0 is white/gray (foreground), 1 is black
trainingData = list() #[row][col]

weightVectors = [] #An array of pairs (digit, weight vector)
traininglabels = []
classCount = [0] * 10
traininglabels = []
testlabels = []
resultlabels = []
results = [0]*10
testcount = [0.0] * 10
confusion = []
pairs = []
testImages = []

numberCorrect = 0


def readInput():
    with open('digitdata/traininglabels') as input_file:
        for i, line in enumerate(input_file):
            line = line.rstrip()
            for label in line:
                traininglabels.append(int(label))

    truNumber = -1
    isFirstIteration = True
    with open('digitdata/trainingimages') as input_file:
        imageNum = 0
        count = 0
        trainingData = initArray()
        for intputLineNum, line in enumerate(input_file):
            currRow = intputLineNum % 28
            imageNum = int(intputLineNum / 28)
            if currRow == 0:
                if not isFirstIteration:
                    processTrainingDigit(trainingData, trueNumber)
                trainingData = initArray()
                trueNumber = traininglabels[imageNum]  # 0-9
                classCount[trueNumber] += 1.0
            for currCol in range(len(line)):
                count+=1
                feature = line[currCol]
                if feature == "#" or feature == "+":
                    trainingData[currRow][currCol] = 0
                elif feature == " ":
                    trainingData[currRow][currCol] = 1
            isFirstIteration = False


def processTrainingDigit(trainingData, trueNumber):
    chosenBestDigit = chooseBestDigit(trainingData)
    if chosenBestDigit[0] != trueNumber:
        #lower score of wrong answer, raise score of right answer
        #weight of incorrect = weight of incorrect - f(x)
        #weight of correct = weight of correct + f(x)
        augmentWeightVector(chosenBestDigit[0], trainingData, False)
        augmentWeightVector(trueNumber, trainingData, True)
        print("Incorrect. Chosen " + str(chosenBestDigit[0]) + ", correct was " + str(trueNumber))
        return False
    else:
        print("Correct on number " + str(chosenBestDigit[0]))
        return True


def augmentWeightVector(digitNumber, dataVector, shouldIncrement):
    for i in range(0, 28):
        for j in range(0, 28):
            if shouldIncrement:
                weightVectors[digitNumber][i][j] += dataVector[i][j]
            else:
                weightVectors[digitNumber][i][j] -= dataVector[i][j]


#randomInitialValues ia bool. If true, then weight vectors initialized randomly
def initializeWeightVectors(randomInitialValues):
    for digit in range (0, 10):
        digitWeight = [[] for i in range (0, 28)]
        for i in range(0, 28):
            digitWeight[i] = [0] * 28
            if randomInitialValues:
                for j in range(0, 28):
                    digitWeight[i][j] = randint(-10, 10)
        weightVectors.append(digitWeight)


def dotProductDigitVectors(testDigitVector, currentDigitVector):
    currentTotal = 0
    for i in range(0, 28):
        for j in range(0, 28):
            currentTotal += testDigitVector[i][j] * currentDigitVector[i][j]
    return currentTotal


#testDigitVector is an array of size [28][28] of the features of a digit to be checked
def chooseBestDigit(testDigitVector):
    bestDigit = -1
    bestDigitValue = -99999999
    for currentDigit in range(0,10):
        currentDigitValue = dotProductDigitVectors(testDigitVector, weightVectors[currentDigit])
        if currentDigitValue > bestDigitValue:
            bestDigit = currentDigit
            bestDigitValue = currentDigitValue
    return (bestDigit, bestDigitValue)


def initArray():
    colors = [K] * 2
    twodim = list()
    for i in range(28):
        temp = list()
        for j in range(28):
            temp.append(deepcopy(colors))
        twodim.append(deepcopy(temp))
    return deepcopy(twodim)

initializeWeightVectors(False)
readInput()
