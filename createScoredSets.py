import sys
import csv
import string
import re
import math

def main():
    extractTraining("./data/russian-troll-tweets/tweets.csv", "w+", "+1", 7)
    extractTraining("./data/democratvsrepublicantweets/ExtractedTweets.csv", "a", "-1", 2)

def extractTraining(path, mode, score, tweetLoc):
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
            
        header = reader.next() # don't need var, but kept for clarity

        row_count = len(list(reader))
        cutoff, i = int(math.ceil(row_count * 0.7)), 0

        # to return to top of our file
        f.seek(0)
        header = reader.next() # don't need var, but kept for clarity

        trainF = open("./data/train-test-sets/troll.train", mode)
        devF = open("./data/train-test-sets/troll.dev", mode)

        regex = re.compile(r"&\S+") #to remove special HTML characters (&amp; &lquo; etc.)

        for line in reader:
            tweet = line[tweetLoc]
            tweet = tweet.lower()
            tweet = regex.sub("", tweet) # remove special HTML characters (&amp; &lquo; etc.)
            tweet = " ".join(tweet.split()) # eliminate white space
            tweet = tweet.translate(None, string.punctuation)

            # eliminates most emojis
            emoji_pattern = re.compile(
                u"(\ud83d[\ude00-\ude4f])|"  # emoticons
                u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
                u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
                u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
                u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
                "+", flags=re.UNICODE)

            tweet = tweet.decode('utf-8') #to unicode to delete emojis
            tweet = emoji_pattern.sub(r'', tweet)
            tweet = tweet.encode('utf-8')
            

            if i < cutoff:
                trainF.write(score + "\t" + tweet + "\n")
            else:
                devF.write(score + "\t" + tweet + "\n")

            i += 1

        trainF.close()
        devF.close()

if __name__ == "__main__":
    main()