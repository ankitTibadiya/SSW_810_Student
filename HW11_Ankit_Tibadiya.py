#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on :
@author: Ankit Tibadiya
    Implement a class Fraction that supports addition, subtraction, multiplication and division and \
        also support not equal, less than, less than or equal, greater than or equal for the fractions to be compared
"""

""" Import required packages"""


import sqlite3
from prettytable import PrettyTable
DB_File = '/home/ankit/Desktop/Stevens/Semester 3/SSW-810/Assignments/HW11/HW11_db.db'

db = sqlite3.connect(DB_File)

query = "Select CWID, Name, Dept, Course, count(Student_CWID) as num_of_students \
from HW11_instructors join HW11_grades on HW11_grades.Instructor_CWID = CWID \
group by Course \
order by CWID desc, num_of_students desc"

pt = PrettyTable(
    field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])

for row in db.execute(query):
    pt.add_row(row)

print('Instructor Summary')
print(pt)
