import random
import collections
import math
import sys
from util import *

def main():
    trainExamples = getExamples("train")
    testExamples = getExamples("test")
    w = learnPredictor(trainExamples, testExamples, 20, 0.01)


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
            score, line = line[0], " ".join(line[1:])
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
        if s.isalnum() and s[0:4] != "http":
            mydict[s] += 1
    return mydict
    # END_YOUR_CODE

def learnPredictor(trainExamples, testExamples, numIters, eta):
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
        features.update(extractWordFeatures(x))
    weights.update(dict.fromkeys(features,0.0))

    def loss(w, f, realY):
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
        for t in range(numIters):
            for i in range(n):
                train, realY = trainExamples[i][0], trainExamples[i][1]

                f = featureExtractor(train)

                myloss = loss(weights, f, realY)
                mygradient = gradient(myloss, train, realY, f)

                increment(weights, -1*eta, mygradient)

            trainError = evaluatePredictor(trainExamples, lambda x : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
            testError = evaluatePredictor(testExamples, lambda x : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
            print 'trainError: {}, testError: {}'.format(trainError, testError)
    
    stochasticGradientDescent(loss, gradient, len(trainExamples))
    # END_YOUR_CODE
    return weights

if __name__ == "__main__":
    main()