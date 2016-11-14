from copy import deepcopy
from math import log

K=1.0
#1 is minimum wage, -1 is life partners
fisher_train_negative_dict = {} #[word count, doc count]
fisher_train_positive_dict = {} #[word count, doc count]

fisher_count_negative = [0.0,0.0] #wordcount for this class, doc count for this class
fisher_count_positive = [0.0,0.0] #wordcount for this class, doc count for this class

#1 is good reviews, -1 is bad reviews
movie_train_negative_dict = {} #[word count, doc count]
movie_train_positive_dict = {} #[word count, doc count]

movie_count_negative = [0.0,0.0] #wordcount for this class, doc count for this class
movie_count_positive = [0.0,0.0] #wordcount for this class, doc count for this class

confusion_fisher_bernouilli  = [0.0,0.0,0.0,0.0] #[TP,FN,FP,TN] 
confusion_fisher_multinomial = [0.0,0.0,0.0,0.0]
confusion_movie_bernouilli   = [0.0,0.0,0.0,0.0]
confusion_movie_multinomial  = [0.0,0.0,0.0,0.0]

def readInput():
	with open('docdata/fisher_2topic/fisher_train_2topic.txt') as input_file:
			for j, document in enumerate(input_file):
				document = document.split(" ")
				label = int(document[0])
				if label==-1:
					fisher_count_negative[1]+=1.0
				else:
					fisher_count_positive[1]+=1.0
				for i in range(1,len(document)):
					word = document[i].split(":")[0]
					count = int(document[i].split(":")[1])
					if label==-1:
						fisher_count_negative[0]+=count
						if word not in fisher_train_negative_dict:
							fisher_train_negative_dict[word]=[K,K]
						fisher_train_negative_dict[word][0]+=count
						fisher_train_negative_dict[word][1]+=1
					elif label==1:
						fisher_count_positive[0]+=count
						if word not in fisher_train_positive_dict:
							fisher_train_positive_dict[word]=[K,K]
						fisher_train_positive_dict[word][0]+=count
						fisher_train_positive_dict[word][1]+=1

	with open('docdata/movie_review/rt-train.txt') as input_file:
			for j, document in enumerate(input_file):
				document = document.split(" ")
				label = int(document[0])
				if label==-1:
					movie_count_negative[1]+=1.0
				else:
					movie_count_positive[1]+=1.0
				for i in range(1,len(document)):
					word = document[i].split(":")[0]
					count = int(document[i].split(":")[1])
					if label==-1:
						movie_count_negative[0]+=count
						if word not in movie_train_negative_dict:
							movie_train_negative_dict[word]=[K,K]
						movie_train_negative_dict[word][0]+=count
						movie_train_negative_dict[word][1]+=1.0
					elif label==1:
						movie_count_positive[0]+=count
						if word not in movie_train_positive_dict:
							movie_train_positive_dict[word]=[K,K]
						movie_train_positive_dict[word][0]+=count
						movie_train_positive_dict[word][1]+=1.0

def normalize():
	for word in fisher_train_negative_dict:
		fisher_train_negative_dict[word][0]/=(fisher_count_negative[0] + len(fisher_train_negative_dict)*K)
		fisher_train_negative_dict[word][1]/=(fisher_count_negative[1] + 2*K)

	for word in fisher_train_positive_dict:
		fisher_train_positive_dict[word][0]/=(fisher_count_positive[0] + len(fisher_train_positive_dict)*K)
		fisher_train_positive_dict[word][1]/=(fisher_count_positive[1] + 2*K)

	for word in movie_train_negative_dict:
		movie_train_negative_dict[word][0]/=(movie_count_negative[0] + len(movie_train_negative_dict)*K)
		movie_train_negative_dict[word][1]/=(movie_count_negative[1] + 2*K)

	for word in movie_train_positive_dict:
		movie_train_positive_dict[word][0]/=(movie_count_positive[0] + len(movie_train_positive_dict)*K)
		movie_train_positive_dict[word][1]/=(movie_count_positive[1] + 2*K)


def classifyMultinomial():
	with open('docdata/fisher_2topic/fisher_test_2topic.txt') as input_file:
		numcCorrectFisher = 0.0
		docCount = 0.0
		#loop through documents
		for i, document in enumerate(input_file):
			docCount += 1.0
			probabilityPos = log(0.5)
			probabilityNeg = log(0.5)
			document = document.split(" ")
			label = int(document[0])
			#loop through words in document
			for j in range(1,len(document)):
				word = document[j].split(":")[0]
				count = int(document[j].split(":")[1])
				for k in range(count):
					if word in fisher_train_positive_dict:
						probabilityPos += log(fisher_train_positive_dict[word][0])
					else:
						probabilityPos += log(K/(fisher_count_positive[0] + len(fisher_train_positive_dict)*K))
					if word in fisher_train_negative_dict:
						probabilityNeg += log(fisher_train_negative_dict[word][0])
					else:
						probabilityNeg += log(K/(fisher_count_negative[0] + len(fisher_train_negative_dict)*K))
			isClassifiedPositive = probabilityPos > probabilityNeg
			if isClassifiedPositive and label==1:
				numcCorrectFisher+=1.0
			elif not isClassifiedPositive and label==-1:
				numcCorrectFisher+=1.0
		print "Multinomial fisher: ",numcCorrectFisher/docCount
	with open('docdata/movie_review/rt-test.txt') as input_file:
		numcCorrectMovie = 0.0
		docCount = 0.0
		#loop through documents
		for i, document in enumerate(input_file):
			docCount += 1.0
			probabilityPos = log(0.5)
			probabilityNeg = log(0.5)
			document = document.split(" ")
			label = int(document[0])
			#loop through words in document
			for j in range(1,len(document)):
				word = document[j].split(":")[0]
				count = int(document[j].split(":")[1])
				for k in range(count):
					if word in movie_train_positive_dict:
						probabilityPos += log(movie_train_positive_dict[word][0])
					else:
						probabilityPos += log(K/(movie_count_positive[0] + len(movie_train_positive_dict)*K))
					if word in movie_train_negative_dict:
						probabilityNeg += log(movie_train_negative_dict[word][0])
					else:
						probabilityNeg += log(K/(movie_count_negative[0] + len(movie_train_negative_dict)*K))
			isClassifiedPositive = probabilityPos > probabilityNeg
			if isClassifiedPositive and label==1:
				numcCorrectMovie+=1.0
			elif not isClassifiedPositive and label==-1:
				numcCorrectMovie+=1.0
		print "Multinomial movie: ",numcCorrectMovie/docCount

def classifyBernoulli():
	with open('docdata/fisher_2topic/fisher_test_2topic.txt') as input_file:
		numcCorrectFisher = 0.0
		docCount = 0.0
		vocabularyNeg = fisher_train_negative_dict.keys()
		vocabularyPos = fisher_train_positive_dict.keys()
		#loop through documents
		for i, document in enumerate(input_file):
			docCount += 1.0
			probabilityPos = log(0.5)
			probabilityNeg = log(0.5)
			items = document.split(" ")
			label = int(items[0])
			#loop through words in document
			docWords = []
			for j in range(1,len(items)):
				word = items[j].split(":")[0]
				docWords.append(word)
			for word in list(set(vocabularyNeg+docWords)):
				if word in docWords and word in fisher_train_negative_dict:
					probabilityNeg+=log(fisher_train_negative_dict[word][1])
				elif word in docWords and word not in movie_train_negative_dict:
					probabilityNeg+=log(K/(fisher_count_negative[1] + 2*K))
				elif word not in docWords and word in fisher_train_negative_dict:
					probabilityNeg+=log(1-fisher_train_negative_dict[word][1])
			for word in list(set(vocabularyPos+docWords)):
				if word in docWords and word in fisher_train_positive_dict:
					probabilityPos+=log(fisher_train_positive_dict[word][1])
				elif word in docWords and word not in fisher_train_positive_dict:
					probabilityPos+=log(K/(fisher_count_positive[1] + 2*K))
				elif word not in docWords and word in fisher_train_positive_dict:
					probabilityPos+=log(1-fisher_train_positive_dict[word][1])

			#[TP,FN,FP,TN] 
			isClassifiedPositive = probabilityPos > probabilityNeg
			if isClassifiedPositive:
				if label==1:
					numcCorrectFisher+=1.0
					confusion_fisher_bernouilli[0]+=1.0
				else:
					confusion_fisher_bernouilli[1]+=1.0
			elif not isClassifiedPositive:
				if label==-1:
					confusion_fisher_bernouilli[3]+=1.0
					numcCorrectFisher+=1.0
				else:
					confusion_fisher_bernouilli[2]+=1.0
		for i in range(4):
			confusion_fisher_bernouilli[i]/=49.0
		print "Bernoulli fisher: ",numcCorrectFisher/docCount
		print "Bernoulli fisher confusion: "
		print confusion_fisher_bernouilli[0],confusion_fisher_bernouilli[1]
		print confusion_fisher_bernouilli[2],confusion_fisher_bernouilli[3]

	with open('docdata/movie_review/rt-test.txt') as input_file:
		numCorrectMovie = 0.0
		docCount = 0.0
		vocabularyNeg = movie_train_negative_dict.keys()
		vocabularyPos = movie_train_positive_dict.keys()
		#loop through documents
		for i, document in enumerate(input_file):
			docCount += 1.0
			probabilityPos = log(0.5)
			probabilityNeg = log(0.5)
			items = document.split(" ")
			label = int(items[0])
			#loop through words in document
			docWords = []
			for j in range(1,len(items)):
				word = items[j].split(":")[0]
				docWords.append(word)
			for word in list(set(vocabularyNeg+docWords)):
				if word in docWords and word in movie_train_negative_dict:
					probabilityNeg+=log(movie_train_negative_dict[word][1])
				elif word in docWords and word not in movie_train_negative_dict:
					probabilityNeg+=log(K/(movie_count_negative[1] + 2*K))
				elif word not in docWords and word in movie_train_negative_dict:
					probabilityNeg+=log(1-movie_train_negative_dict[word][1])
			for word in list(set(vocabularyPos+docWords)):
				if word in docWords and word in movie_train_positive_dict:
					probabilityPos+=log(movie_train_positive_dict[word][1])
				elif word in docWords and word not in movie_train_positive_dict:
					probabilityPos+=log(K/(movie_count_positive[1] + 2*K))
				elif word not in docWords and word in movie_train_positive_dict:
					probabilityPos+=log(1-movie_train_positive_dict[word][1])

			isClassifiedPositive = probabilityPos > probabilityNeg
			if isClassifiedPositive and label==1:
				numCorrectMovie+=1.0
			elif not isClassifiedPositive and label==-1:
				numCorrectMovie+=1.0
		print "Bernoulli movie: ",numCorrectMovie/docCount

readInput()
normalize()
classifyMultinomial()
classifyBernoulli()
# print movie_train_negative_dict
# print fisher_count_positive