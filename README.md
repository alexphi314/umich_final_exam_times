# Installation

This project was written in Python 3 and requires the third party 'requests' library.

Install the required libraries:
`pip install -r requirements.txt`

# Running the script
In a text file, write down the first day and time your class meets each week.
If your class meets Mondays, Wednesdays, and Fridays at 10:00 am, you would write
`monday 10:00 am` in the file. Put one class per line.

An example of this is shown in the classes.txt file.

When you run the script, supply the year and term as arguments. For example, 
if you were finding the exam times for the Fall 2018 term:
`python calc_final_exam_times.py --term Fall --year 2018 --classes classes.txt`

To view more information on the arguments:
`python calc_final_exam_times.py -h`