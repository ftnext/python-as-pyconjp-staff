import datetime as dt
from unittest import TestCase
from unittest.mock import patch

from timetable.data import Program, Programs


class ProgramTestCase(TestCase):
    def test_zero_filled_hour(self):
        for time_str, expected in zip(("11:30", "9:00"), ("11:30", "09:00")):
            with self.subTest(time_str=time_str, expected=expected):
                actual = Program.zero_filled_hour(time_str)

                self.assertEqual(actual, expected)

    @patch(
        "timetable.data.Program.zero_filled_hour",
        side_effect=("09:30", "10:30"),
    )
    def test_create(self, zero_filled_hour):
        actual = Program.create("9:30", "10:30", "Test", ["Room2"])

        expected = Program(dt.time(9, 30), dt.time(10, 30), "Test", ["Room2"])
        self.assertEqual(actual, expected)
        # __eq__で比較していない属性について検証
        self.assertEqual(actual.end, expected.end)
        self.assertEqual(actual.title, expected.title)
        self.assertEqual(actual.rooms, expected.rooms)

    def test_lt_between_program_instances(self):
        """start時刻の大小関係を、プログラムどうしの大小関係とする"""
        program1 = Program(
            dt.time(9, 30), dt.time(10, 30), "Test1", ["Room1", "Room2"]
        )
        program2 = Program(dt.time(11, 0), dt.time(12, 0), "Test2", ["Room3"])

        self.assertTrue(program1 < program2)

    def test_lt_with_not_program_instance(self):
        program = Program(
            dt.time(9, 30), dt.time(10, 30), "Test1", ["Room1", "Room2"]
        )
        a_time = dt.time(11, 0)

        self.assertEqual(program.__lt__(a_time), NotImplemented)

    def test_eq_between_program_instances(self):
        """start時刻が等しければ、プログラムとして等しいとみなす"""
        program1 = Program(dt.time(10, 0), dt.time(11, 0), "Test1", ["Room1"])
        # yamlファイルではstart時刻が等しいプログラムは書かれない想定
        program2 = Program(
            dt.time(10, 0), dt.time(10, 30), "Test2", ["Room2", "Room3"]
        )

        self.assertTrue(program1 == program2)

    def test_eq_with_not_program_instance(self):
        program = Program(dt.time(10, 0), dt.time(11, 0), "Test1", ["Room1"])
        a_time = dt.time(10, 0)

        self.assertEqual(program.__eq__(a_time), NotImplemented)


class ProgramsTestCase(TestCase):
    def setUp(self):
        self.programs_list = [
            Program(dt.time(10, 30), dt.time(11, 30), "Test2", ["Room3"]),
            Program(
                dt.time(9, 30), dt.time(10, 00), "Test1", ["Room1", "Room2"]
            ),
        ]

    def assertProgramEqual(self, actual, expected):
        self.assertEqual(actual, expected)
        self.assertEqual(actual.end, expected.end)
        self.assertEqual(actual.title, expected.title)
        self.assertEqual(actual.rooms, expected.rooms)

    def test_getitem(self):
        programs = Programs(self.programs_list)

        program1 = programs[0]
        expected1 = Program(
            dt.time(10, 30), dt.time(11, 30), "Test2", ["Room3"]
        )
        self.assertProgramEqual(program1, expected1)

        program2 = programs[1]
        expected2 = Program(
            dt.time(9, 30), dt.time(10, 00), "Test1", ["Room1", "Room2"]
        )
        self.assertProgramEqual(program2, expected2)

    def test_len(self):
        programs = Programs(self.programs_list)

        self.assertEqual(len(programs), 2)
