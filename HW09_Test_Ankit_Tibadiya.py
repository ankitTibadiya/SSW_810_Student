#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from HW09_Ankit_Tibadiya import Repository


class TestModuleRepository(unittest.TestCase):
    def test_student_data(self):
        students_data = {'10103': ['10103', 'Baldwin, C', 'SFEN', ['SSW 567', 'SSW 564', 'SSW 687', 'CS 501']],
                         '10115': ['10115', 'Wyatt, X', 'SFEN', ['SSW 567', 'SSW 564', 'SSW 687', 'CS 545']],
                         '10172': ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567']],
                         '10175': ['10175', 'Erickson, D', 'SFEN', ['SSW 567', 'SSW 564', 'SSW 687']],
                         '10183': ['10183', 'Chapman, O', 'SFEN', ['SSW 689']],
                         '11399': ['11399', 'Cordova, I', 'SYEN', ['SSW 540']],
                         '11461': ['11461', 'Wright, U', 'SYEN', ['SYS 800', 'SYS 750', 'SYS 611']],
                         '11658': ['11658', 'Kelly, P', 'SYEN', ['SSW 540']],
                         '11714': ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645']],
                         '11788': ['11788', 'Fuller, E', 'SYEN', ['SSW 540']]
                         }

        stevens = Repository('./Stevens_data')
        computed_student_data = dict()

        for cwid, student_details in stevens.students.items():
            computed_student_data[cwid] = student_details.get_student_data_with_major(
            )

        self.assertTrue(students_data['10103'] ==
                        computed_student_data['10103'])
        self.assertTrue(students_data ==
                        computed_student_data)

    def test_instructor_data(self):
        instructors_data_dict = {'98765': ['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4],
                                 '98764': ['98764', 'Feynman, R', 'SFEN', 'SSW 564', 3],
                                 '98763': ['98763', 'Newton, I', 'SFEN', 'SSW 555', 1],
                                 '98762': ['98762', 'Hawking, S', 'SYEN', None, None],
                                 '98761': ['98761', 'Edison, A', 'SYEN', None, None],
                                 '98760': ['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1]}

        stevens = Repository('./Stevens_data')
        computed_instructor_data = dict()

        for cwid, instructor_details in stevens.instructors.items():
            computed_instructor_data[cwid] = instructor_details.get_instructor_data(
            )

        self.assertTrue(instructors_data_dict['98765'] ==
                        computed_instructor_data['98765'])
        self.assertTrue(instructors_data_dict ==
                        computed_instructor_data)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
