#!/usr/bin/env python

import string
import random

import peewee as pw

myDB = pw.MySQLDatabase("mail_db", host="localhost", port=3306, user="root", passwd="mysql")

class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = myDB

class mailing(MySQLModel):
    addr = pw.CharField(max_length=255, unique=True, primary_key=True)

def connect():
    try:
        myDB.connect()
        print("... DB connected")
    except Error as e:
        print(e)
        print("... DB not connected")

#######################################################
def generate_id(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_domain():
    DOMAINS = ["aol.com", "att", "comcast", "facebook", "gmail", "gmx", "googlemail",
    "google", "hotmail", "mac", "me", "mail", "msn",
    "live", "sbcglobal", "verizon", "yahoo"]

    TOP_LEVEL = ['.com ','.net ','.org ','.gov ','.edu ','.us', '.co.uk']

    return random.choice(DOMAINS) + random.choice(TOP_LEVEL)

def generate_email():
    return generate_id() + '@' + generate_domain()

def add_email(email):
    try:
        mailing.create(addr=email)
        print(email)
    except IntegrityError:
        print('Record of email {} already exist'.format(email))

#######################################################
if __name__ == '__main__':
    connect()
    numb = input('How many emails would you like to generate?\n   > ')
    for _ in range(numb):
        email = generate_email()
        add_email(email)
    print ('\n\n {} emails generated in "mailing" table'.format(numb))
