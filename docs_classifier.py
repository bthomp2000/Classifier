from copy import deepcopy
fisher_train_negative_dict = {}
fisher_train_positive_dict = {}

movie_train_negative_dict = {}
movie_train_positive_dict = {}

def readInput():
	with open('docdata/fisher_2topic/fisher_train_2topic.txt') as input_file:
			for i, line in enumerate(input_file):
				line = line.split(" ")
				label = int(line[0])
				for i in range(1,len(line)):
					word = line[i].split(":")[0]
					count = int(line[i].split(":")[1])
					if label==-1:
						if word not in fisher_train_negative_dict:
							fisher_train_negative_dict[word]=0
						fisher_train_negative_dict[word]+=count
					elif label==1:
						if word not in fisher_train_positive_dict:
							fisher_train_positive_dict[word]=0
						fisher_train_positive_dict[word]+=count

	with open('docdata/movie_review/rt-train.txt') as input_file:
			for i, line in enumerate(input_file):
				line = line.split(" ")
				label = int(line[0])
				for i in range(1,len(line)):
					word = line[i].split(":")[0]
					count = int(line[i].split(":")[1])
					if label==-1:
						if word not in movie_train_negative_dict:
							movie_train_negative_dict[word]=0
						movie_train_negative_dict[word]+=count
					elif label==1:
						if word not in movie_train_positive_dict:
							movie_train_positive_dict[word]=0
						movie_train_positive_dict[word]+=count
readInput()
print movie_train_negative_dict