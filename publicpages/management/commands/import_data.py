from django.core.management.base import BaseCommand, CommandError
from publicpages.models import UserGroup2, WHICHWEEK, WEEKDAYS
from datetime import time

import csv


WEEKDAYS_LOOKUP = {
    '' : None,
    'Sunday' : 0,
    'Sun' : 0,
    'Monday' : 1,
    'Mon' : 1,
    'Tuesday' : 2,
    'Tues' : 2,
    'Tue' : 2,
    'Wednesday' : 3,
    'Wednes' : 3,
    'Wed' : 3,
    'Thursday' : 4,
    'Thurs' : 4,
    'Thu' : 4,
    'Friday' : 5,
    'Fri' : 5,
    'Saturday' : 6,
    'Satur' : 6,
    'Sat' : 6,
}


def weekday_lookup (wd_str):
    '''
    look up the weekday from the abbreviation using WEEKDAYS_LOOKUP, then
    get the canonical weekday string from WEEKDAYS and return that
    '''
    answer = ''
    if wd_str:
        wd_num = WEEKDAYS_LOOKUP[wd_str]
        answer = WEEKDAYS[wd_num]
    return answer

def mystrptime (time_str):
    '''
    Given a string in format 'HH:MM[:SS]', return a time object
    '''
    parts = time_str.split (':')
    #answer = time_str
    answer = None
    if 2 == len (parts):
        answer = time (int (parts[0]), int (parts[1]))
    elif 3 == len (parts):
        answer = time(int (parts[0]), int (parts[1]), int (parts[2]))

    return answer


def dumprow (row, stdout):
    '''
    having receive a row of data, dump it to stdout
    '''
    stdout.write ('Name:\t%s\n' % row[0])
    stdout.write ('\tweekday:\t%s/%s\n' % (row[1], weekday_lookup (row[1])))
    if row[2]:
        stdout.write ('\tweek of month:\t%s/%s\n' % (row[2], WHICHWEEK[row[2]]))
    else:
        stdout.write ('\tweek of month:\n')
    stdout.write ('\tdescription:\t%s\n' % row[3])
    stdout.write ('\tlocation:\t%s\n' % row[4])
    stdout.write ('\taddress:\t%s\n' % row[5])
    stdout.write ('\tnote:\t%s\n' % row[6])
    stdout.write ('\ttime:\t%s\n' % mystrptime (row[7]))
    stdout.write ('\tweb site:\t%s\n' % row[8])
    stdout.write ('\temail site:\t%s\n' % row[9])
    stdout.write ('\tother site:\t%s\n' % row[10])
    stdout.write ('\n\n')


class Command (BaseCommand):

    args = '<csv-file>'
    help = 'imports data from csv-file'

    def handle (self, *args, **options):

        csvfile_name = args[0]

        # open the csv file
        csvfile = open (csvfile_name, 'rb')
        datareader = csv.reader (csvfile, delimiter = ',', quotechar = '"')
        # open the rejects file
        rejectsfile = open ('rejects', 'wb')
        # throw away the first line
        datareader.next ()
        # each line in file:
        for row in datareader:
            # dump data
            dumprow (row, self.stdout)
            ## create model
            ug2 = UserGroup2.objects.create ()
            ug2.name = row[0]
            if row[1]:
                ug2.meet_weekday = int (WEEKDAYS_LOOKUP[row[1]])
            if row[2]:
                if 'last' != row[2]:
                    ug2.meet_week_of_month = int (row[2])
                else:
                    ug2.meet_week_of_month = 6
            ug2.meet_description = row[3]
            ug2.location_name = row[4]
            ug2.location_address = row[5]
            ug2.location_note = row[6]
            if row[7]:
                ug2.meeting_time = mystrptime (row[7])
            ug2.web_site = row[8]
            ug2.email_site = row[9]
            ug2.other_url = row[10]
            self.stdout.write (ug2.dump ())
            # save model
            ug2.save ()
            ## if not successful, write to other file "rejects"
            ## ???
        # close csv file
        csvfile.close ()
        # close rejects file
        rejectsfile.close ()
