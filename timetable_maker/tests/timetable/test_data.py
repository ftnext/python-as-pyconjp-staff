from unittest import TestCase

from timetable.data import Program


class ProgramTestCase(TestCase):
    def test_zero_filled_hour(self):
        for time_str, expected in zip(("11:30", "9:00"), ("11:30", "09:00")):
            with self.subTest(time_str=time_str, expected=expected):
                actual = Program.zero_filled_hour(time_str)

                self.assertEqual(actual, expected)
