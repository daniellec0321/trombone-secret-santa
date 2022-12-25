import sys
from os.path import exists
import csv
import random
 


def createMatchings(info):

    # create variables
    receivers_left = list()
    for elem in info:
        receivers_left.append(elem) 
    ret = dict()

    # match one person for each 
    for elem in info:

        rec = random.choice(receivers_left)

        # loop to make sure someone isn't matched with themselves
        while (rec == elem):
            rec = random.choice(receivers_left)

        # add to ret and delete from receivers
        ret[elem] = rec
        receivers_left = [ele for ele in receivers_left if ele != rec]

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
        if line[0] in info:
            print('Duplicate entry "' + line[0] + '" in info dictionary!')
            exit()

        # put into dictionary
        info[line[0]] = [line[1], line[2]]

    # function to create matchings
    matchings = createMatchings(info)

    # function to send emails to each person
    send_emails(info, matchings)
