#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sqlite3
from HW10_Ankit_Tibadiya import Repository


class TestModuleRepository(unittest.TestCase):
    def test_student_data(self):
        students_data = {'10103': ['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'],{'SSW 540', 'SSW 555'},None],
                         '10115': ['10115', 'Bezos, J', 'SFEN', ['SSW 810'],{'SSW 540', 'SSW 555'},{'CS 501', 'CS 546'}],
                         '10183': ['10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'],{'SSW 540'},{'CS 501', 'CS 546'}],
                         '11714': ['11714', 'Gates, B', 'CS', ['CS 546','CS 570', 'SSW 810'],None,None],
                         '11717': ['11717', 'Kernighan, B', 'CS', [], {'CS 570', 'CS 546'}, {'SSW 810', 'SSW 565'}]
                         }

        stevens = Repository('./')

        computed_student_data = dict()

        for cwid,student in stevens.students.items():
            cwid, name, major, completed_courses = student.get_student_data()
            completed_courses = stevens.majors[student.major].calc_major_grades(
                student.course_grade)
            student_info = [cwid, name, major]
            for item in completed_courses:
                student_info.append(item)
            computed_student_data[cwid] = student_info

        self.assertTrue(students_data ==
                        computed_student_data)
        

    def test_instructor_data(self):
        instructors_data_dict = [['98764', 'Cohen, R', 'SFEN', 'CS 546', 1],
                                 ['98763', 'Rowland, J', 'SFEN', 'SSW 810', 4],
                                 ['98763', 'Rowland, J', 'SFEN', 'SSW 555', 1],
                                 ['98762', 'Hawking, S', 'CS', 'CS 501', 1],
                                 ['98762', 'Hawking, S', 'CS', 'CS 546', 1],
                                 ['98762', 'Hawking, S', 'CS','CS 570', 1]
                                ]

        stevens = Repository('./')
        computed_instructor_data = list()

        for instructor in stevens.instructors.values():
            inst_list = instructor.get_instructor_data()
            for instruct in inst_list:
                computed_instructor_data.append(instruct)
        
        self.assertTrue(instructors_data_dict ==
                        computed_instructor_data)
        

    def test_major_data(self):
        major_data_dict = {'SFEN': ['SFEN', ['SSW 540', 'SSW 555', 'SSW 810'], ['CS 501', 'CS 546']],
                           'CS': ['CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']]}

        stevens = Repository('./')
        computed_major_data = dict()
        for major, major_details in stevens.majors.items():
            computed_major_data[major] = major_details.get_majors_data()

        self.assertTrue(major_data_dict['SFEN'] == computed_major_data['SFEN'])
        self.assertTrue(major_data_dict == computed_major_data)
        
    def test_instructor_db_data(self):
        instruct_data = [('98764', 'Cohen, R', 'SFEN', 'CS 546', 1),
                                 ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),
                                 ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),
                                 ('98762', 'Hawking, S', 'CS', 'CS 501', 1),
                                 ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
                                 ('98762', 'Hawking, S', 'CS','CS 570', 1)
                                ]

        db = sqlite3.connect('/home/ankit/Desktop/Stevens/Semester 3/SSW-810/Assignments/HW11/HW11_db.db')
        query = "select CWID,Name,Dept,Course,count(StudentCWID) as num_of_students \
                from HW11_instructors join HW11_grades on CWID = InstructorCWID \
                group by CWID,Name,Dept,Course \
                ORDER BY CWID desc, num_of_students desc"
        db_data = list()
        for row in db.execute(query):
            db_data.append(row)
        self.assertTrue(instruct_data == db_data)
        


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
