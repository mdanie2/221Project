import os
import sys

#path = path to csv file
#splitter = way to split desired csv file. default is ","
def main(splitter="\",\""):
    path = sys.argv[1]
    if len(sys.argv) > 2: splitter = sys.argv[2]
    removeCSVspaces(path, splitter)

def removeCSVspaces(path, splitter):
    f = open(path, 'r')

    path = path.split("/")
    firstHalf, secondHalf = "/".join(path[0:-1]), path[-1]

    newF = open(firstHalf+"/copy_of_"+secondHalf, 'w+')
    

    attributes = f.readline()
    numAttributes = len(attributes.split(splitter))
    newF.write(attributes)

    prevLine = f.readline().strip()
    line = f.readline()
    
    while line:
        line = line.strip()
        if line == "":
            #continual check
            while line == "":
                line = f.readline().strip()
            
            prevLine = prevLine + "\t" + line 
        
        else:
            if prevLine[-1] != "\"" or len(prevLine.split(splitter)) < numAttributes: 
                prevLine = prevLine + "\t" + line
            else:
                newF.write(prevLine+"\n")
                prevLine = line.strip()

        line = f.readline()
    
    newF.write(prevLine+"\n")

    f.close()
    newF.close()


if __name__ == "__main__":
  main()
