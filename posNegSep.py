import re
import sys
from collections import Counter

def main():
	kFilePrefix = "./data/train-test-sets/"

	devFile = kFilePrefix+"troll.dev"
	trainFile = kFilePrefix+"troll.train"

	posDev, negDev = kFilePrefix+"troll.pos.dev", kFilePrefix+"troll.neg.dev"
	posTrain, negTrain = kFilePrefix+"troll.pos.train", kFilePrefix+"troll.neg.train"\

	if len(sys.argv) < 2:
		from nltk.corpus import stopwords #improper but it speeds our program slightly

		stop_words = set(stopwords.words('english'))

		# writeToFiles(devFile, posDev, negDev, stop_words) #MAY PROVE USELESS
		# writeToFiles(trainFile, posTrain, negTrain, stop_words) #MAY PROVE USELESS
		vocab = countWords(devFile, trainFile, stop_words)
		print "vocab total: ", len(vocab)
		shortened = [(k, c) for k,c in vocab.items() if c >= 2]
		print "length of words with more than 2 occurences", len(shortened)

	# elif sys.argv[1] == "-c":
		# posCounter, negCounter = Counter(int), Counter(int)
		# getCounts(p)

	else: print "Improper usage... python posNegSep.py [-c]"

def countWords(devFile, trainFile, stopwords):
	vocab = Counter()
	files = [devFile, trainFile]

	for path in files:
		with open(path, "r") as f:
			lines = f.readlines()
			regex = re.compile(r"http\S+") #strip urls

			for line in lines:
				line = line.replace("rt ", "") #eliminate RT
				line = regex.sub("", line)
				line = line.strip().split()
				_, line = line[0], line[1:]
				
				line = [word for word in line if word.isalpha()]

				line = [word for word in line if not word in stopwords]

				line = [word for word in line if len(word) > 1]

				for word in line:
					vocab[word] += 1

	return vocab

def writeToFiles(writeFrom, posFilePath, negFilePath, stopwords):
	posFile, negFile = open(posFilePath, "w+"), open(negFilePath, "w+")
	with open(writeFrom, "r") as f:
		lines = f.readlines()
		regex = re.compile(r"http\S+") #strip urls

		for line in lines:
			line = line.replace("rt ", "") #TODO: pay attention to this line
			line = regex.sub("", line)
			line = line.strip().split()
			classification, line = line[0], line[1:]
			
			# more data clensing
			line = [word for word in line if word.isalpha()]

			line = [word for word in line if not word in stopwords]

			#remove single characters
			line = [word for word in line if len(word) > 1]

			toWrite = ' '.join(line) + "\n"
			if classification == "+1": posFile.write(toWrite)
			else: negFile.write(toWrite)

	posFile.close()
	negFile.close()

if __name__ == "__main__":
	main()