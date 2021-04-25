import datetime as dt
from unittest import TestCase

from timetable.data import Program


class ProgramTestCase(TestCase):
    def test_zero_filled_hour(self):
        for time_str, expected in zip(("11:30", "9:00"), ("11:30", "09:00")):
            with self.subTest(time_str=time_str, expected=expected):
                actual = Program.zero_filled_hour(time_str)

                self.assertEqual(actual, expected)

    def test_eq_between_program_instances(self):
        """start時刻が等しければ、プログラムとして等しいとみなす"""
        program1 = Program(dt.time(10, 0), dt.time(11, 0), "Test1", ["Room1"])
        # yamlファイルではstart時刻が等しいプログラムは書かれない想定
        program2 = Program(
            dt.time(10, 0), dt.time(10, 30), "Test2", ["Room2", "Room3"]
        )

        self.assertTrue(program1 == program2)

    def test_lt_between_program_instances(self):
        """start時刻の大小関係を、プログラムどうしの大小関係とする"""
        program1 = Program(
            dt.time(9, 30), dt.time(10, 30), "Test1", ["Room1", "Room2"]
        )
        program2 = Program(dt.time(11, 0), dt.time(12, 0), "Test2", ["Room3"])

        self.assertTrue(program1 < program2)
