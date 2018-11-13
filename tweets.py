'''TODO: MAY BE OBSOLETE. DELETE LATER'''

import sys
import csv

#path = path to csv file
#splitter = way to split desired csv file. default is ","
def main():
    path, tweetLoc = sys.argv[1], int(sys.argv[2])
    createSamples(path, tweetLoc)

#extracts just the tweets

def createSamples(path, tweetLoc):
    path = path.split("/")
    firstHalf, secondHalf = "/".join(path[0:-1]), path[-1]

    with open(firstHalf+"/tweets_only_of_"+secondHalf, 'w+') as newF:
        with open("/".join(path)) as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            header = reader.next()
            # newF.write(','.join(header))
            for line in reader:
                tweet = line[tweetLoc]
                print tweet
                tweet = tweet.replace('\n', '')
                print tweet
                print ' '
                counter += 1
                # tweet = tweet.replace('\n', '')
                newF.write(tweet+"\n")
# def createSamples(path, tweetLoc, splitter):
#     f = open(path, 'r')

#     path = path.split("/")
#     firstHalf = "/".join(path[0:-1])

#     newF = open(firstHalf+"/only_tweets.csv", 'w+')
    
#     attributes = f.readline()

#     for line in f.readlines():
#         line = line.split(splitter)
#         line = line[tweetLoc]
#         line = line.strip()
#         newF.write(line+"\n")

#     f.close()
#     newF.close()


if __name__ == "__main__":
  main()
