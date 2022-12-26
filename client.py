import sys
from os.path import exists
import csv
import random
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_emails(info, matchings):

    trombone_email = "dcrofttest0321@gmail.com"
    trombone_name = "Trombone Secret Santa"
    # password = input('Enter application password: ')
    password='kpovbrohervzjtuh'

    # loop through each entry
    for elem in info:

        # find variables
        curr_sender_name = elem
        curr_receiver_name = matchings[elem]
        curr_sender_email = info[elem][0]
        curr_receiver_preferences = info[matchings[elem]][1]
        
        # create message container
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Trombone Secret Santa Assignments!'
        msg['From'] = 'Trombone Secret Santa'
        msg['To'] = curr_receiver_name

        html = """
        <html>
            <head>
                <style>
                    .my_contact{color: red;}
                </style>
            </head>
            <body>
                <br></br>
                <p>Hi """ + curr_sender_name + """!</p>
                <p>Thank you for participating in Trombone Christmas 2023! You will be giving a gift to <b>""" + curr_receiver_name + """</b>. Try to keep the price of the gift at around $10. Make sure to have it ready by [some date] at [some time]!</p>
                <p>""" + curr_receiver_name + """'s gift preferences are: <b>""" + curr_receiver_preferences + """</b></p>
                <p>Email me at <span class="my_contact">daniellec0321@gmail.com</span> or text me at <span class="my_contact">719-822-3039</span> if you have any questions!</p>
                <br><p>Out like something,</p>
                <p>Danielle "Something" Croft</p></br>
            </body>
        </html>
        """

        part = MIMEText(html, 'html')
        msg.attach(part)

        smtp_server=smtplib.SMTP("smtp.gmail.com",587)
        smtp_server.ehlo() #setting the ESMTP protocol
        smtp_server.starttls() #setting up to TLS connection
        smtp_server.ehlo() #calling the ehlo() again as encryption happens on calling startttls()
        smtp_server.login(trombone_email,password) #logging into out email id

        smtp_server.sendmail(trombone_email,curr_sender_email,msg.as_string())
        print('Successfully sent an email to ' + curr_sender_name) #printing a message on sending the mail
        smtp_server.quit()#terminating the server

    """
    sender_add='dcrofttest0321@gmail.com' #storing the sender's mail id
    receiver_add='daniellec0321@gmail.com' #storing the receiver's mail id
    password='kpovbrohervzjtuh' #storing the password to log in
    #creating the SMTP server object by giving SMPT server address and port number

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = "Trombone Secret Santa"
    msg['To'] = "Colton Kammes"

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    # html = "\
        <html>
            <head></head>
            <body>
                <p>Hi!<br>
                    How are you?<br>
                    Here is the <a href="http://www.python.org">link</a> you wanted.
                </p>
            </body>
        </html>
        "

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    smtp_server=smtplib.SMTP("smtp.gmail.com",587)
    smtp_server.ehlo() #setting the ESMTP protocol
    smtp_server.starttls() #setting up to TLS connection
    smtp_server.ehlo() #calling the ehlo() again as encryption happens on calling startttls()
    smtp_server.login(sender_add,password) #logging into out email id
    #writing the message in HTML
    html_msg="From: Trombone Secret Santa
    To: daniellec0321@gmail.com
    MIME-Version: 1.0
    Content-type: text/html
    Subject: Trombone Secret Santa Assignment!
    <br><p> Hi there! You are getting a present for <b>Colton Kammes.</b></p></br>
    "
    #sending the mail by specifying the from and to address and the message 
    # smtp_server.sendmail(sender_add,receiver_add,html_msg)
    # smtp_server.sendmail(sender_add,receiver_add,em.as_string())
    smtp_server.sendmail(sender_add,receiver_add,msg.as_string())
    print('Successfully the mail is sent') #printing a message on sending the mail
    smtp_server.quit()#terminating the server

    """
 


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
