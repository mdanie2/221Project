import re
import sys
import os.path
from nltk.corpus import stopwords
from collections import Counter
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
# from keras.layers.embeddings import Embedding

def main():
	kFilePrefix = "./data/train-test-sets/"
	devFile, trainFile = kFilePrefix+"troll.dev", kFilePrefix+"troll.train"
	posDev, negDev = kFilePrefix+"troll.pos.dev", kFilePrefix+"troll.neg.dev"
	posTrain, negTrain = kFilePrefix+"troll.pos.train", kFilePrefix+"troll.neg.train"
	stop_words = set(stopwords.words('english'))

	if not os.path.isfile(posDev) or not os.path.isfile(negDev): 
		writeToFiles(devFile, posDev, negDev, stop_words)
	if not os.path.isfile(posTrain) or not os.path.isfile(negTrain): 
		writeToFiles(trainFile, posTrain, negTrain, stop_words) 

	# vocab, maxLen = countWords(devFile, trainFile, stop_words)
	vocab, maxLen = countChars(devFile, trainFile, stop_words, 6)

	tokens = [k for k,c in vocab.items() if c >= 2] # top 10, bottom 5

	# tokens = [k for k,c in vocab.items() if c >= num] # top 10, bottom 5
	trTrollWords, trTrollCount = getPosOrNegWords(posTrain, vocab)
	trPoliticianWords, trPoliticianCount = getPosOrNegWords(negTrain, vocab)
	devTrollWords, devTrollCount = getPosOrNegWords(posDev, vocab)
	devPoliticianWords, devPoliticianCount = getPosOrNegWords(negDev, vocab)

	trainWords, devWords = trPoliticianWords + trTrollWords, devPoliticianWords + devTrollWords
	tokenizer = Tokenizer()
	Xtrain, ytrain = getTrainOrTestSet(tokenizer, trainWords, trPoliticianCount, trTrollCount, maxLen)
	Xtest, ytest = getTrainOrTestSet(tokenizer, devWords, devPoliticianCount, devTrollCount, maxLen)

	vocabSize = len(tokenizer.word_index) + 1
	myCNN(Xtrain, ytrain, Xtest, ytest, vocabSize, 16, maxLen)
	# myLSTM(Xtrain, ytrain, Xtest, ytest, vocabSize, 32, maxLen) #worse
	

def myCNN(Xtrain, ytrain, Xtest, ytest, vocabSize, embeddingSize, maxLen):
	# define model
	model = Sequential()
	model.add(Embedding(vocabSize, embeddingSize, input_length=maxLen))
	model.add(Conv1D(filters=24, kernel_size=4, activation='relu'))
	model.add(MaxPooling1D(pool_size=2))
	model.add(Flatten())
	model.add(Dense(10, activation='relu'))
	model.add(Dense(1, activation='sigmoid'))
	print(model.summary())
	# compile network
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	# fit network
	model.fit(Xtrain, ytrain, epochs=5)
	# evaluate
	loss, acc = model.evaluate(Xtest, ytest, verbose=0)
	print('Accuracy: %.2f%%' % (acc*100))

def myLSTM(Xtrain, ytrain, Xtest, ytest, vocabSize, embeddingSize, maxLen):
	model = Sequential()
	model.add(Embedding(vocabSize, embeddingSize, input_length=maxLen))
	model.add(Dropout(0.2))
	model.add(LSTM(100))
	model.add(Dropout(0.2))
	model.add(Dense(1, activation='sigmoid'))
	print(model.summary())
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	model.fit(Xtrain, ytrain, epochs=5, batch_size=64)
	# Final evaluation of the model
	loss, acc = model.evaluate(Xtest, ytest, verbose=0)
	print("Accuracy: %.2f%%" % (acc*100))

def getTrainOrTestSet(tokenizer, words, polCount, trollCount, maxLen):
	tokenizer.fit_on_texts(words)
	encodedWords = tokenizer.texts_to_sequences(words)
	X = pad_sequences(encodedWords, maxlen=maxLen, padding='post')
	y = [0 for _ in range(polCount)] + [1 for _ in range(trollCount)]
	return X, y

def countChars(devFile, trainFile, stopwords, n):
	vocab = Counter()
	files = [devFile, trainFile]
	maxLen = float('-inf')
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

				line = "".join(line)

				for i in range(0, len(line)-n): vocab[line[i:i+n]] += 1

	return vocab, n

def countWords(devFile, trainFile, stopwords):
	vocab = Counter()
	files = [devFile, trainFile]
	maxLen = float('-inf')
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
					if len(word) > maxLen: maxLen = len(word)

	return vocab, maxLen

def cleanWords(line, vocab):
	tokens = line.split()
	tokens = [word for word in tokens if word in vocab]
	tokens = ' '.join(tokens)
	return tokens

def getPosOrNegWords(path, vocab):
	words, count = [], 0

	with open(path, "r") as f:
		lines = f.readlines()

		for line in lines:
			count += 1
			tokens = cleanWords(line, vocab)

			words.append(tokens)

	return words, count


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