## Alex Philpott
## This script uses ref_times.txt to seed the ref_times.json file

import json
import datetime as dt
import re

with open('ref_times.txt','r') as f:
    lines = f.readlines()

times = {}
for line in lines:
    #print(line.replace('\n',''))

    if 'Monday' in line and 'first' in line:
        mode = 'Monday'
        sub_times = {}
        continue

    elif 'Tuesday' in line and 'first' in line:
        ## Monday comes first, so it will be defined first
        times[mode] = sub_times

        mode = 'Tuesday'
        sub_times = {}
        continue

    if 'Lecture Time' in line:
        continue

    split_line = line.split('!')
    #print(split_line)
    if len(split_line) != 3:
        continue

    class_time = split_line[0].strip()
    exam_date = split_line[1].strip()
    exam_time = split_line[2].strip()

    time_re = re.compile('(?P<start>\d\d?:\d\d? \w\w) - .+')
    exam_start = time_re.search(exam_time).group('start')

    exam_datetime = dt.datetime.strptime('2018 ' + exam_date + ' ' + exam_start, '%Y %A, %B %d %I:%M %p')

    sub_times[class_time] = exam_datetime.strftime('%A, %B %d %I:%M %p')

times[mode] = sub_times

with open('ref_times.json','w') as f:
    json.dump(times, f)
