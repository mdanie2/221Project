import sys
import csv
import string

#path = path to csv file
#splitter = way to split desired csv file. default is ","
def main(wType="political"):
    path, tweetLoc, weights = sys.argv[1], int(sys.argv[2]), {}
    
    if len(sys.argv) > 3: wType = sys.argv[3]
    
    if wType == "political":
        weights = {'rigged': 1, 'democrats': 1, 'clinton': 1, 'liberals': 1,
        'benghazi': 1, 'obama': 1, 'blacksfortrump': 1, 'emails': 1,
        'lockherup': 1, 'hillary': 1, 'crookedhillary': 1, 'makeamericagreatagain': 1,
        'fakenews': 1, 'maga': 1,  
        'democracy': -1, 'imwithher': -1, 'civic': -1, 'conservatives': -1,
        'trump': -1, 'notmypresident': -1, 'republicans': -1, 'racism': -1,
        'hope': -1, 'blue': -1, 'racist': -1, 'gohillary': -1, 'thanksobama': -1,
        'gop': -1, 'proud': -1
        }
    elif wType == "troll":
        weights = {'nigga': 1, 'nastywoman': 1, 'maga': 1, 'racist': 1, 'fuck': 1, 'fucking': 1,
        'civic': -1, 'vote': -1, 'hope': -1, 'respect': -1, 'change': -1, 'lead': -1, 'leader': -1
        }
        
    baselinePrediction(path, weights, tweetLoc, wType)

#extracts just the tweets
def baselinePrediction(path, weights, tweetLoc, wType):
    path = path.split("/")    
    firstHalf, secondHalf = "/".join(path[0:-1]), path[-1]
    path = "/".join(path)

    with open(firstHalf+'/baseline_score_'+wType+'.csv', 'w+') as newF:
        with open(path, 'r') as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            
            header = reader.next()
            
            for line in reader:
                tweet = line[tweetLoc]
                tweet = tweet.rstrip().lower()
                tweet = tweet.translate(None, string.digits)
                score = 0
                for word in tweet.split():
                    score += weights.get(word, 0)

                # dem/republican split
                if secondHalf == 'ExtractedTweets.csv':
                    if score > 0:
                        newF.write("+1  "+line[0]+"  "+tweet+"\n")
                    elif score < 0:
                        newF.write("-1  "+line[0]+"  "+tweet+"\n")
                    else:
                        newF.write("no_class  "+line[0]+"  "+tweet+"\n")
                else:
                    if score > 0:
                        newF.write("+1  "+tweet+"\n")
                    elif score < 0:
                        newF.write("-1  "+tweet+"\n")
                    else:
                        newF.write("no_class  "+tweet+"\n")


    # newF = open(firstHalf+"/baseline_score.csv", 'w+')
    
    # attributes = f.readline()

    # for line in f.readlines():
    #     lowercase = line.strip().lower()
    #     noPunc = lowercase.translate(None, string.punctuation)
    #     noPuncOrDigits = noPunc.translate(None, string.digits)
    #     score = 0
    #     for word in noPuncOrDigits.split():
    #         score += weights.get(word, 0)
    #     if score > 0:
    #         newF.write("+1\t"+line)
    #     elif score < 0:
    #         newF.write("-1\t"+line)
    #     else:
    #         newF.write("no_class\t"+line)

    # f.close()
    # newF.close()


if __name__ == "__main__":
  main()
