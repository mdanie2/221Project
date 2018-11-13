'''TODO: MAY BE OBSOLETE. DELETE LATER?'''

import sys
import csv

#path = path to csv file
def main():
    path = sys.argv[1]
    removeCSVspaces(path)#, numAttributes, splitter)

def removeCSVspaces(path):

    path = path.split("/")
    firstHalf, secondHalf = "/".join(path[0:-1]), path[-1]

    with open(firstHalf+"/copy_of_"+secondHalf, 'w+') as newF:
        with open("/".join(path)) as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            
            header = reader.next()
            newF.write(','.join(header))
            
            line = reader.next()
            while line:
                print line[7]
                # print "next one is"
                # for it in line:
                # line = ','.join(line)
                # line = line.strip()
                # newF.write(line)
                line = reader.next()


if __name__ == "__main__":
  main()
