#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on :
@author: Ankit Tibadiya
    Implement a class Fraction that supports addition, subtraction, multiplication and division and \
        also support not equal, less than, less than or equal, greater than or equal for the fractions to be compared
"""

""" Import required packages"""




from prettytable import PrettyTable
from collections import defaultdict
import sqlite3
import os
class Student:
    """ Student Class with all the details of a student"""

    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course_grade = defaultdict(str)

    def add_course_grades(self, course, grade=None):
        self.course_grade[course] = grade

    def get_student_data_with_major(self):
        return [self.cwid, self.name, self.major, sorted(list(self.course_grade.keys()))]

    def get_student_data(self):
        return [self.cwid, self.name, self.major, sorted(list(self.course_grade.keys()))]


class Instructor:
    """ Instructor class with all the details of a instructor  """

    def __init__(self, cwid, name, department):
        self.cwid = cwid
        self.name = name
        self.department = department
        self.course_student = defaultdict(int)

    def add_course_students(self, course):
        self.course_student[course] += 1

    def instruct_data_test(self):
        return [self.cwid, self.name, self.department, self.course_student]
    def get_instructor_data(self):
        inst_list = list()
        for course, num_students in self.course_student.items():
            inst_list.append(
                [self.cwid, self.name, self.department, course, num_students])
        return inst_list


class Major:
    '''Calculate the required courses that each student must take to graduate along with the remaining electives'''

    def __init__(self, major):
        self.major = major

        self.required_courses = set()
        self.elective_courses = set()

    def add_req_elec(self, flag, course):
        if flag == 'R':
            self.required_courses.add(course)
        elif flag == 'E':
            self.elective_courses.add(course)
        else:
            raise ValueError(f'Unknown course flag: {flag}')

    def calc_major_grades(self, courses):
        pass_grades = ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C')

        completed_courses = set()
        for course, grade in courses.items():
            if grade == ' ':
                continue
            elif grade in pass_grades:
                completed_courses.add(course)

        required_remaining = self.req_course_remain(completed_courses)
        electives_remaining = self.elec_course_remain(completed_courses)

        return [sorted(list(completed_courses)), required_remaining, electives_remaining]

    def req_course_remain(self, courses):
        if self.required_courses.difference(courses) == set():
            return None
        else:
            return self.required_courses.difference(courses)

    def elec_course_remain(self, courses):
        remaining_courses = self.elective_courses.difference(courses)
        if len(remaining_courses) < len(self.elective_courses):
            return None
        else:
            return self.elective_courses

    def get_majors_data(self):
        return [self.major, sorted(list(self.required_courses)), sorted(list(self.elective_courses))]


""" Repository class with all the data for particular university """


class Repository:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.students_path = os.path.join(dir_path, 'HW11_students.txt')
        self.instructors_path = os.path.join(dir_path, 'HW11_instructors.txt')
        self.grades_path = os.path.join(dir_path, 'HW11_grades.txt')
        self.major_path = os.path.join(dir_path, 'HW11_majors.txt')

        self.students = dict()
        self.instructors = dict()
        self.majors = dict()
        self.grades = list

        self.get_students()
        self.get_instructors()
        self.process_grades()
        self.get_majors()

    def read_file(self, path, sep=',', header=True):
        try:
            fp = open(path)
        except FileNotFoundError:
            raise FileNotFoundError(f'No such file found.')
        else:
            with fp:
                for line in fp:
                    if header:
                        header = False
                        continue
                    else:
                        yield line.strip().split(f'{sep}')

    def get_students(self):
        """
        Store all the students with CWID, Name and Major 
        """
        for line_num, student_data in enumerate(self.read_file(self.students_path, '\t')):
            try:
                cwid, name, major = student_data
            except ValueError:
                raise ValueError(
                    f'{student_data} has unexpected format on line {line_num+1} in students.txt ')
            else:
                if cwid not in self.students.keys():
                    self.students[cwid] = Student(cwid, name, major)

    def get_instructors(self):
        """
        Store all the instructors with CWID, Name and Department 
        """
        for line_num, instructor_data in enumerate(self.read_file(self.instructors_path, sep='\t')):
            try:
                cwid, name, department = instructor_data
            except ValueError:
                raise ValueError(
                    f'{instructor_data} has unexpected format on line {line_num+1} in instructors.txt')
            else:
                if cwid not in self.instructors:
                    self.instructors[cwid] = Instructor(cwid, name, department)

    def get_majors(self):
        """
        Store all the major related information like required courses and elective courses
        """
        for line_num,major_data in enumerate(self.read_file(self.major_path, sep='\t')):
            try:
                major, flag, course = major_data
            except ValueError:
                raise ValueError(
                    f'{major_data} has unexpected format on line {line_num+1} in instructors.txt')
            else:
                if major not in self.majors:
                    self.majors[major] = Major(major)

                self.majors[major].add_req_elec(flag, course)

    def process_grades(self):
        """Reads grades.txt  """
        for line_num, grades_data in enumerate(self.read_file(self.grades_path, sep='\t')):
            try:
                cwid_student, course, grade, cwid_instructor = grades_data
            except ValueError:
                raise ValueError(
                    f'{grades_data} has unexpected format on line {line_num+1} in grades.txt')
            else:
                if cwid_student not in self.students.keys():
                    raise ValueError(
                        f'Student with CWID {cwid_student} is not present in students data')
                if cwid_instructor not in self.instructors.keys():
                    raise ValueError(
                        f'Instructor with CWID {cwid_instructor} is not present in instructors data')

            self.students[cwid_student].add_course_grades(course, grade)
            self.instructors[cwid_instructor].add_course_students(course)

    def students_prettyTable(self):
        pt = PrettyTable(field_names=[
                         'CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])

        for student in self.students.values():
            cwid, name, major, completed_courses = student.get_student_data()
            completed_courses = self.majors[student.major].calc_major_grades(
                student.course_grade)
            student_info = [cwid, name, major]
            for item in completed_courses:
                student_info.append(item)

            pt.add_row(student_info)

        print('Student Summary')
        print(pt)

    def instructors_prettyTable(self):
        pt = PrettyTable(
            field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])

        for instructor in self.instructors.values():
            inst_list = instructor.get_instructor_data()
            for instruct in inst_list:
                pt.add_row(instruct)

        print('Instructor Summary')
        print(pt)

    def major_prettyTable(self):
        pt = PrettyTable(field_names=['Dept', 'Required', 'Electives'])
        dept = None
        required = None
        electives = None
        for major in self.majors.values():
            dept, required, electives = major.get_majors_data()
            pt.add_row([dept, required, electives])

        print('Major Summary')
        print(pt)

    def instructors_prettyTable_db(self,DB_File):
        db = sqlite3.connect(DB_File)

        query = "select CWID,Name,Dept,Course,count(StudentCWID) as num_of_students \
                from HW11_instructors join HW11_grades on CWID = InstructorCWID \
                group by CWID,Name,Dept,Course \
                ORDER BY CWID desc, num_of_students desc"

        pt = PrettyTable(
            field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])

        for row in db.execute(query):
            pt.add_row(row)
        
        print('Instructor Summary')
        print(pt)



def main():
    stevens = Repository(
        '/home/ankit/Desktop/Stevens/Semester 3/SSW-810/Assignments/HW11')
    
    stevens.major_prettyTable()
    stevens.students_prettyTable()
    stevens.instructors_prettyTable()

    DB_File = '/home/ankit/Desktop/Stevens/Semester 3/SSW-810/Assignments/HW11/HW11_db.db'
    stevens.instructors_prettyTable_db(DB_File)


if __name__ == '__main__':
    main()
