import sys
from os.path import exists
import csv
import random
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_emails(info, matchings):

    # getting user input
    trombone_email = input("\nEnter the email you will be sending from: ")
    password = input("Enter the 16-character password given by Google: ")

    print("")
    trombone_name = "Trombone Secret Santa"

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

    # create list with names
    names = list()
    for elem in info:
        names.append(elem)

    # shuffle the list
    random.shuffle(names)

    # create return dictionary
    ret = dict()
    for i in range(0, len(names)-1):
        ret[names[i]] = names[i+1]

    # set last value
    ret[names[len(names)-1]] = names[0]

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

    # check for user continuation
    print("\nBefore continuing, make sure you have a valid Gmail account to send emails from. It should have two-factor authentification set up and a password key generated to allow access to the account through Python. If this is not the case, quit the program by typing 'q'. Otherwise, continue the program by entering 'c'.")
    user_input = input('Enter choice here: ')
    while (user_input != 'c') and (user_input != 'q'):
        user_input = input("Please enter either 'q' for quit or 'c' for continue: ")
    if user_input == 'q':
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

    # check matchings
    print("\nThe matchings for Secret Santa are:")
    for elem in matchings:
        print(elem + " -> " + matchings[elem])

    user_input = input("\nIf these matchings look good, enter 'c' to send the confirmation emails. Otherwise, enter 'q' to quit: ")
    while (user_input != 'c') and (user_input != 'q'):
        user_input = input("Please enter either 'q' for quit or 'c' for continue: ")
    if user_input == 'q':
        exit()

    send_emails(info, matchings)
