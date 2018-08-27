## Alex Philpott

import json
import subprocess
import re
import datetime as dt
import requests
import argparse

def get_exam_times(year, term):
    """
    Given term, fetch final exam times from the Registrar website

    :param year: int, the term year in YYYY format
    :param term: the season (Fall, Winter) of the term
    :return: times, a dict with the corresponding final exam datetime for the class start time
    """

    ## Validate input year format
    if len(str(year)) != 4:
        raise ValueError('Must provide full four digit year, e.g. 2018')

    ## Fetch data from the website
    term = term.lower()
    url = 'http://ro.umich.edu/calendars/final-exams/{}-{}'.format(year, term)
    lines = requests.get(url)

    ## Validate the URL is good
    if lines.status_code != 200:
        raise ValueError('Input term does not have existing webpage at http://ro.umich.edu/calendars/final-exams/')

    ## Continue through the top part of the webpage until we get to the final exam time table
    lines = lines.text.split('\n')
    for indx, line in enumerate(lines):
        if 'Monday' in line and 'first' in line:
            start = indx
            break

    lines = lines[start:]

    ## Declare variables
    times = {}
    time_re = re.compile('\d\d?:\d\d [ap]m', re.IGNORECASE)
    two_time_re = re.compile('(?P<first>\d\d?:\d\d) or (?P<second>\d\d?:\d\d [ap]m)', re.IGNORECASE)
    date_re = re.compile('\w+, \w+ \d\d?', re.IGNORECASE)
    time_range_re = re.compile('\d\d?:\d\d [ap]m - \d\d?:\d\d [ap]m', re.IGNORECASE)

    ## Loop through table
    for indx, line in enumerate(lines):

        #print(line.replace('\n',''))


        if 'Monday' in line and 'first' in line:
            mode = 'Monday'
            sub_times = {}
            continue

        ## When we get to the Tuesday table, switch modes
        elif 'Tuesday' in line and 'first' in line:
            ## Monday comes first, so it will be defined first
            times[mode] = sub_times

            mode = 'Tuesday'
            sub_times = {}
            continue

        ## Skip lines if they don't have times in them
        if 'Lecture Time' in line:
            continue
        if 'Special Examination' in line:
            break

        ## The table is represented in sequence in code
        ## When we see a class start time line in the code, we fill the final exam date and time at the same time
        ## So when we see a date or time line, it needs to be skipped
        if date_re.search(line) or time_range_re.search(line) or (not time_re.search(line) and not two_time_re.search(line)):
            #print(line)
            continue

        ## If there are two times in one cell, separate them and fill the dict for each
        line_times = []
        if two_time_re.search(line):
            first = two_time_re.search(line).group('first')
            second = two_time_re.search(line).group('second')

            first = first + ' ' + second[-2:]

            line_times.append(first)
            line_times.append(second)

        else:
            line_times.append(time_re.search(line).group())

        ## For each time in the class start time cell, fill the exam date and time
        for class_time in line_times:
            exam_date = date_re.search(lines[indx+1]).group()
            exam_time = time_range_re.search(lines[indx+2]).group()

            time_re = re.compile('(?P<start>\d\d?:\d\d? \w\w) - .+')
            exam_start = time_re.search(exam_time).group('start')

            exam_datetime = dt.datetime.strptime('2018 ' + exam_date + ' ' + exam_start, '%Y %A, %B %d %I:%M %p')

            sub_times[class_time] = exam_datetime.strftime('%A, %B %d %I:%M %p')

    times[mode] = sub_times

    return times

## Define Argparser
parser = argparse.ArgumentParser()
parser.add_argument('--year', '-y', help="Term year. Assumes 2018 if not provided.", default=2018, type=int)
parser.add_argument('--term', '-t', help="Term season, e.g. Fall")
parser.add_argument('--classes', '-c', help='File containing list of class start times', default='classes.txt')
args = vars(parser.parse_args())

## Read input arguments
term = args['term']
year = args['year']

with open(args['classes'], 'r') as f:
    classes = f.readlines()

data = get_exam_times(year, term)

## Output final exam times based on registrar tables
print('\nFinal Exam Times:')
frmat = re.compile('(?P<day>[MT][ou][ne]s?day) (?P<time>\d\d?:\d\d [ap]m)',re.IGNORECASE)
for indx, clss in enumerate(classes):
    day = frmat.search(clss).group('day')
    time = frmat.search(clss).group('time')

    day = day.capitalize()

    if not day in data.keys():
        raise KeyError('Could not find key {} in data, options are: {}'.format(day, data.keys()))

    if not time in data[day].keys():
        raise KeyError('Could not find key {} in data, options are: {}'.format(time, data[day].keys()))

    final_exam_time = data[day][time]
    print('Class {}: {}'.format(indx+1,final_exam_time))