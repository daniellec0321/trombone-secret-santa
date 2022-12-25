import sys
from os.path import exists
import csv
import random
 


def createMatchings(info):

    # create elements
    ret = dict()
    found_valid = False
    receivers_left = list()
    for elem in info:
        receivers_left.append(elem)

    # loop until valid dictionary made
    while True:

        for elem in info:

            # check if at last element and last two equal each other: reset
            if (len(receivers_left) == 1) and (receivers_left[0] == elem):
                ret = dict()
                receivers_left = list()
                for elem in info:
                    receivers_left.append(elem)
                break

            # if at last one and don't equal each other, then good
            elif len(receivers_left) == 1:
                found_valid = True

            # find random receiver
            rec = random.choice(receivers_left)
            while (rec == elem):
                rec = random.choice(receivers_left)

            # add to ret and delete from receivers_left
            ret[elem] = rec
            for i in range(0, len(receivers_left)):
                if receivers_left[i] == rec:
                    del receivers_left[i]
                    break

        if found_valid == True:
            break

    return ret



if __name__=='__main__':

    # check for input
    if len(sys.argv) != 2:
        print("Usage: $ python3 client.py [CSV Input]")
        exit()
    
    # check if file exists
    file_exists = exists(sys.argv[1])
    if (file_exists == False):
        print("No file named " + sys.argv[1])
        exit()

    # key: name, value: list of email and preferences
    info = dict()

    # list for reading csv
    csvList = list()

    # read file
    with open(sys.argv[1], mode ='r')as file:
        
        # reading the CSV file
        csvFile = csv.reader(file)

        # displaying the contents of the CSV file
        for lines in csvFile:
            csvList.append(lines)

    # integrate info into dictionary
    for line in csvList:

        # check if already in dictionary
        if line[1] in info:
            print('Duplicate entry "' + line[1] + '" in info dictionary!')
            exit()

        # put into dictionary
        info[line[1]] = [line[0], line[2]]

    # function to create matchings
    matchings = createMatchings(info)

    for elem in matchings:
        print(elem + ": " + matchings[elem])
