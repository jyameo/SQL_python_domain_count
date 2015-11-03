#!/usr/bin/env python

import re
from collections import Counter
from collections import defaultdict
from collections import OrderedDict
from operator import itemgetter
import time
import datetime
import random

#########################################################
import peewee as pw

myDB = pw.MySQLDatabase("mail_db", host="localhost", port=3306, user="root", passwd="mysql")

class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = myDB

class mailing(MySQLModel):
    addr = pw.CharField(max_length=255, unique=True,primary_key=True)

def connect():
    try:
        myDB.connect()
        print("... DB connected")
    except Error as e:
        print(e)
        print("... DB not connected")

#######################################################

class mail_count(MySQLModel):
    domain = pw.CharField(max_length=255)
    count = pw.IntegerField(default=1)
    timestamp = pw.DateTimeField(default=datetime.date.today())

    class Meta:
        database = myDB
        primary_key = pw.CompositeKey('domain', 'timestamp')

def initialize():
    """Create the database and the table if they don't exist."""
    myDB.create_tables([mail_count], safe=True)


def add_mail_count(mail_count_entry):
        try:
            domain_exists = mail_count.select().where(mail_count.domain.contains(mail_count_entry['domain']))
            timestamp_exists = mail_count.select().where(mail_count.timestamp == (mail_count_entry['timestamp']))
            if domain_exists and timestamp_exists:
                mail_record = mail_count.get(domain=mail_count_entry['domain'])
                mail_record.count = mail_count_entry['count']
                mail_record.timestamp = mail_count_entry['timestamp']
                mail_record.save()
                print('Record of domain {} updated successfully!!'.format(mail_count_entry['domain']))
        except :
            mail_count.create(domain=mail_count_entry['domain'],
                        count=mail_count_entry['count'],
                        timestamp=mail_count_entry['timestamp'])
            print('Record of domain {} inserted successfully!!'.format(mail_count_entry['domain']))


def generate_mail_count_for_testing():
    '''Creates random dates for existing emails and insert in mail count table (call this once)'''

    for domain,count in domain_list_from_mailing().iteritems():
        domain_dict = {'domain':domain,
                    'count':count,
                    'timestamp':generate_random_date("2015-01-01", datetime.date.today().strftime("%Y-%m-%d"), random.random())}
        add_mail_count(domain_dict)

def update_mail_count():
    '''Update mail_count if new record are inserted'''

    list_from_mailing = domain_list_from_mailing()
    list_from_mail_count = domain_list_from_mail_count()

    for key,value in list_from_mailing.iteritems():
        list_from_mail_count = domain_list_from_mail_count()
        if key not in list_from_mail_count.keys():
            '''add new entry with value 1 to mail_count at current timestamp'''
            domain_dict = {'domain':key,'count':value,'timestamp': datetime.date.today()}
            print('New entry for domain {} will be added to record'.format(key))
            add_mail_count(domain_dict)
        elif list_from_mail_count[key]!= value:
            ''' update daily count for entry in mail_count '''
            domain_dict = {'domain':key,'count':max(value,list_from_mail_count[key]),'timestamp': datetime.date.today()}
            print('Entry for domain {} will be updated'.format(key))
            add_mail_count(domain_dict)


def strTimeProp(start, end, format, prop):

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def generate_random_date(start, end, prop):
    return strTimeProp(start, end, '%Y-%m-%d', prop)


def domain_list_from_mailing():

    emails = mailing.select()
    domain_list = list()

    for email in emails:
        domain = re.search("@[\w.]+", email.addr)
        domain_list.append(domain.group()[1:])

    domain_entries = Counter(domain_list)
    domain_entries = domain_entries.most_common()

    return dict(domain_entries)

def domain_list_from_mail_count():

    domain_count = mail_count.select()
    domain_list = list()

    for domains in domain_count:
        domain_list.append((domains.domain,domains.count))

    domain_entries = defaultdict(list)
    for tag, num in domain_list:
        domain_entries[tag].append(num)

    domain_sum = ({k: sum(v) for k, v in domain_entries.iteritems()})
    return domain_sum

def top_domains():
    '''Report the top 50 domains by count sorted by percentage growth of the last 30 days compared to the total'''

def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = raw_input('Action: ').lower().strip()

        if choice in menu:
            menu[choice]()

menu = OrderedDict([
    ('g', generate_mail_count_for_testing),
    ('u', update_mail_count),
    ('t', top_domains),
])

#######################################################
if __name__ == '__main__':
    connect()
    initialize()
    menu_loop()

##comment after running the first time to generate data for testing##
#generate_mail_count_for_testing()
#    update_mail_count()
