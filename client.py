import sys
from os.path import exists
import csv
import random
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_emails(info, matchings):

    print("in send_emails")

    """
    sender_add='dcrofttest0321@gmail.com' #storing the sender's mail id
    receiver_add='daniellec0321@gmail.com' #storing the receiver's mail id
    password='kpovbrohervzjtuh' #storing the password to log in
    #creating the SMTP server object by giving SMPT server address and port number
    smtp_server=smtplib.SMTP("smtp.gmail.com",587)
    smtp_server.ehlo() #setting the ESMTP protocol
    smtp_server.starttls() #setting up to TLS connection
    smtp_server.ehlo() #calling the ehlo() again as encryption happens on calling startttls()
    smtp_server.login(sender_add,password) #logging into out email id
    msg_to_be_sent ='''
    Hello, receiver!
    Hope you are doing well.
    Welcome to PythonGeeks!
    '''
    print("uhhhhhh")
    #sending the mail by specifying the from and to address and the message 
    smtp_server.sendmail(sender_add,receiver_add,msg_to_be_sent)
    print('Successfully the mail is sent') #priting a message on sending the mail
    # smtp_server.quit()#terminating the server
    """

    sender_add='dcrofttest0321@gmail.com' #storing the sender's mail id
    receiver_add='dcrofttest0321@gmail.com' #storing the receiver's mail id
    password='kpovbrohervzjtuh' #storing the password to log in
    #creating the SMTP server object by giving SMPT server address and port number

    # attempt to create context
    em = EmailMessage()
    em['From'] = 'Danielle Croft'
    em['To'] = 'Colton Kammes'
    em['Subject'] = 'Trombone Secret Santa Assignment!'
    body = """
    Your secret santa assignemnt is <b>Caroline Lubbe</b>.
    """
    em.set_content(body)

    smtp_server=smtplib.SMTP("smtp.gmail.com",587)
    smtp_server.ehlo() #setting the ESMTP protocol
    smtp_server.starttls() #setting up to TLS connection
    smtp_server.ehlo() #calling the ehlo() again as encryption happens on calling startttls()
    smtp_server.login(sender_add,password) #logging into out email id
    #writing the message in HTML
    html_msg="""From: Trombone Secret Santa
    To: daniellec0321@gmail.com
    MIME-Version: 1.0
    Content-type: text/html
    Subject: Trombone Secret Santa Assignment!
    <br><p> Hi there! You are getting a present for <b>Colton Kammes.</b></p></br>
    """
    #sending the mail by specifying the from and to address and the message 
    # smtp_server.sendmail(sender_add,receiver_add,html_msg)
    smtp_server.sendmail(sender_add,receiver_add,em.as_string())
    print('Successfully the mail is sent') #printing a message on sending the mail
    smtp_server.quit()#terminating the server
 


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

    send_emails(info, matchings)
