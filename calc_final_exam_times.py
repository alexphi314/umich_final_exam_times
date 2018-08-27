## Alex Philpott

import json
import subprocess
import re

## Seed the data file
subprocess.call(['python','seed_times.py'])

## Load the data
with open('ref_times.json','r') as f:
    data = json.load(f)

## Get class times from user
inpt = True
print("""For each class in your schedule, please enter the first day and time it meets during the week.
For example, a class that meets at 8:30 am on Monday, Wednesday, Friday would be 'Monday 8:30 am'.
When you are done entering classes, type 'done'""")
frmat = re.compile('(?P<day>[MT][ou][ne]s?day) (?P<time>\d\d?:\d\d [ap]m)',re.IGNORECASE)
i = 1
classes = []
while inpt:
    clss = input('Class {}: '.format(i))

    if 'done' in clss:
        break

    if not frmat.match(clss):
        print('Input {} is not in the correct format. Please use <Monday|Tuesday> <time> <am|pm>.'.format(clss))

    i += 1
    classes.append(clss)

print('\nFinal Exam Times:')
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

