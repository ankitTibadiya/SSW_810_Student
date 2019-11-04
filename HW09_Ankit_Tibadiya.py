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
        return [self.cwid, self.name, self.major, list(self.course_grade.keys())]

    def get_student_data(self):
        if not self.course_grade.items():
            return [self.cwid, self.name, None]
        else:
            return [self.cwid, self.name, sorted(list(self.course_grade.keys()))]


class Instructor:
    """ Instructor class with all the details of a instructor  """

    def __init__(self, cwid, name, department):
        self.cwid = cwid
        self.name = name
        self.department = department
        self.course_student = defaultdict(int)

    def add_course_students(self, course):
        self.course_student[course] += 1

    def get_instructor_data(self):
        if not self.course_student.items():
            return [self.cwid, self.name, self.department, None, None]
        else:
            for course, num_students in self.course_student.items():
                return [self.cwid, self.name, self.department, course, num_students]


""" Repository class with all the data for particular university """


class Repository:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.students_path = os.path.join(dir_path, 'students.txt')
        self.instructors_path = os.path.join(dir_path, 'instructors.txt')
        self.grades_path = os.path.join(dir_path, 'grades.txt')

        self.students = dict()
        self.instructors = dict()
        self.grades = list

        self.get_students()
        self.get_instructors()
        self.process_grades()

    def read_file(self, path):
        try:
            fp = open(path)
        except FileNotFoundError:
            raise FileNotFoundError(f'No such file found.')
        else:
            with fp:
                for line in fp:
                    yield line.strip().split('\t')
        finally:
            fp.close()

    def get_students(self):
        """
        Store all the students with CWID, Name and Major 
        """
        for line_num, student_data in enumerate(self.read_file(self.students_path)):
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
        for line_num, instructor_data in enumerate(self.read_file(self.instructors_path)):
            try:
                cwid, name, department = instructor_data
            except ValueError:
                raise ValueError(
                    f'{instructor_data} has unexpected format on line {line_num+1} in instructors.txt')
            else:
                if cwid not in self.instructors:
                    self.instructors[cwid] = Instructor(cwid, name, department)

    def process_grades(self):
        """Reads grades.txt  """
        for line_num, grades_data in enumerate(self.read_file(self.grades_path)):
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
        pt = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])

        for student in self.students.values():
            cwid, name, completed_courses = student.get_student_data()
            pt.add_row([cwid, name, completed_courses])

        print('Student Summary')
        print(pt)

    def instructors_prettyTable(self):
        pt = PrettyTable(
            field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])

        for instructor in self.instructors.values():
            cwid, name, dept, course, num_students = instructor.get_instructor_data()
            pt.add_row([cwid, name, dept, course, num_students])

        print('Instructor Summary')
        print(pt)


def main():
    stevens = Repository(
        '/home/ankit/Desktop/Stevens/Semester 3/SSW-810/Assignments/Assignment-9/Stevens_data')

    stevens.students_prettyTable()
    stevens.instructors_prettyTable()


if __name__ == '__main__':
    main()
