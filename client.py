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
    password = input('Enter application password: ')

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
                <p>Email me at daniellec0321@gmail.com or text me at <span class="my_contact">719-822-3039</span> if you have any questions!</p>
                <br><p>Out like something,</p>
                <p>Danielle "Something" Croft</p></br>
            </body>
        </html>
        """

        # attach data to message
        part = MIMEText(html, 'html')
        msg.attach(part)

        # connect to server
        smtp_server=smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(trombone_email, password)

        # send email
        smtp_server.sendmail(trombone_email, curr_sender_email, msg.as_string())
        print('Successfully sent email to ' + curr_sender_name)
        smtp_server.quit()



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

    send_emails(info, matchings)
