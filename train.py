import random
import collections
import math
import sys
from util import *

'''TODO: Improve'''

def main():
    trainExamples = getExamples("train")
    testExamples = getExamples("test")
    # w = learnPredictor(trainExamples, testExamples, extractWordFeatures, 100, eta)
    print "========= WORDS ========"
    w = learnPredictor(trainExamples, testExamples, extractWordFeatures, 100, 0.1)
    print "========= 2GRAMS ========"
    w = learnPredictor(trainExamples, testExamples, extractWordFeatures, 100, 0.1)
    print "========= 3GRAMS ========"
    w = learnPredictor(trainExamples, testExamples, extractWordFeatures, 100, 0.1)
    print "========= 4GRAMS ========"
    w = learnPredictor(trainExamples, testExamples, extractWordFeatures, 100, 0.1)
    print "========= 5GRAMS ========"
    w = learnPredictor(trainExamples, testExamples, extractWordFeatures, 100, 0.1)
    print "========= 6GRAMS ========"
    w = learnPredictor(trainExamples, testExamples, extractWordFeatures, 100, 0.1)
    print "========= 7GRAMS ========"
    w = learnPredictor(trainExamples, testExamples, extractWordFeatures, 100, 0.1)
    print "========= 8GRAMS ========"
    w = learnPredictor(trainExamples, testExamples, extractWordFeatures, 100, 0.1)



def getExamples(exType):
    path = "./data/train-test-sets/"
    if exType == "train":
        path = path + "troll.train"
    else:
        path = path + "troll.dev"
    
    exList = []

    with open(path, "r") as f:
        for line in f.readlines():
            line = line.split()
            score, line = float(line[0]), " ".join(line[1:])
            exList.append((line, score))

    return exList

def extractWordFeatures(x):
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x: 
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    mydict = collections.defaultdict(float)
    for s in x.split(' '):
        if s.isalnum():
            mydict[s] += 1
    return mydict
    # END_YOUR_CODE

def learnPredictor(trainExamples, testExamples, featureExtractor, numIters, eta):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    '''
    weights = {}  # feature => weight
    # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
    features = {}
    for x,y in trainExamples:
        features.update(featureExtractor(x))
    weights.update(dict.fromkeys(features,0.0))

    def loss(w, f, realY):
        # print dotProduct(w,f)
        score = 1 if dotProduct(w,f) >= 0 else -1
        margin = score * realY
        return 0 if margin >= 0 else 2

    def gradient(loss, words, realY, f):
        if loss == 0:
            return {}

        for k,v in f.items():
            f[k] = -1 * v * realY
        return f

    def stochasticGradientDescent(loss, gradient, n):
        # n = number of points
        for t in range(1, numIters+1):
            for i in range(n):
                train, realY = trainExamples[i][0], trainExamples[i][1]

                f = featureExtractor(train)
                myloss = loss(weights, f, realY)
                mygradient = gradient(myloss, train, realY, f)

                increment(weights, -1*eta, mygradient)
            if t % 5 == 0:
                trainError, trainTrollError, trainPolError = evaluatePredictor(trainExamples, lambda x : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
                testError, testTrollError, testPolError = evaluatePredictor(testExamples, lambda x : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
                print 'train accuracy: {}, troll train accuracy: {}, politician train accuracy: {}'.format(1-trainError, 1-trainTrollError, 1-trainPolError)
                print 'test accuracy: {}, troll test accuracy: {}, politician train accuracy: {}'.format(1-testError, 1-testTrollError, 1-testPolError)
    
    stochasticGradientDescent(loss, gradient, len(trainExamples))
    # END_YOUR_CODE
    return weights

def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    You may assume that n >= 1.
    '''
    def extract(x):
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        translated, ngrams = ''.join(filter(lambda y: y != '', x.split(' '))), ''
        for i in xrange(len(translated)-n+1):
            ngrams = ngrams + ' ' + translated[i:i+n] 
        return extractWordFeatures(ngrams)
        # END_YOUR_CODE
    return extract

if __name__ == "__main__":
    main()