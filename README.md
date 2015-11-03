# SQL_python_domain_count

Jessy Yameogo

Version = Python 2.7.6

Scenario:
Given an SQL table 'mailing':

The mailing table will initially be empty.  New addresses will be added on a daily basis.  It is expected that the table will store at least 10,000,000 email addresses and 100,000 domains.

The Python script updates another table which holds a daily count of email addresses by their domain name.

This table is then used to report the top 50 domains by count sorted by percentage growth of the last 30 days compared to the total.

** NOTE **

- The original mailing table should not be modified.

- All processing must be done in Python (eg. no complex queries or sub-queries)

Before testing, please install "peewee" by running this command on Linux => pip install peewee.
Peewee is a simple and small ORM (Object Relational Mapping).

To Test the Program:

  -first run 'create_mailing.py' to generate emails
    -Use this file to create new emails after to simulate new incoming emails

  -then run the 'domain_count.py':
    you will be presented with 4 options:
      -press g (only the first time) to "Creates random dates for existing emails and insert in mail_count table (call this once)"
      -press u to "Update mail_count if new record are inserted" (use create_mailing.py to create new record)
      -press t to "Report the top 50 domains by count sorted by percentage growth of the last 30 days compared to the total" (not completed!)
      -press q to quit the program
