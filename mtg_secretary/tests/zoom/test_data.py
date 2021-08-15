import io
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from zoom.data import ScheduledMeeting, ScheduledMeetings


class ScheduledMeetingTestCase(TestCase):
    def test_factory(self):
        actual = ScheduledMeeting.create(
            "2021-04-19T12:00:00Z",
            "Meeting topic",
            "https://test.zoom.us/j/0123456789?pwd=password",
        )

        expected = ScheduledMeeting(
            datetime(2021, 4, 19, 21, 0, 0),
            "Meeting topic",
            "https://test.zoom.us/j/0123456789?pwd=password",
        )
        self.assertEqual(actual, expected)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_print(self, mock_stdout):
        sut = ScheduledMeeting(
            datetime(2021, 8, 9, 20, 30, 0),
            "Print topic",
            "https://print.zoom.us/j/0123456789?pwd=password",
        )
        expected = """\
2021-08-09 20:30:00
Print topic
https://print.zoom.us/j/0123456789?pwd=password
"""

        print(sut)
        actual = mock_stdout.getvalue()

        self.assertEqual(actual, expected)


class ScheduledMeetingsTestCase(TestCase):
    def test_sorted(self):
        meeting1 = ScheduledMeeting(
            datetime(2021, 8, 16, 20, 30, 0),
            "Greater topic",
            "https://greater.zoom.us/j/0123456789?pwd=password",
        )
        meeting2 = ScheduledMeeting(
            datetime(2021, 8, 12, 21, 0, 0),
            "Smaller topic",
            "https://smaller.zoom.us/j/0123456789?pwd=password",
        )
        expected = ScheduledMeetings([meeting2, meeting1])

        sut = ScheduledMeetings([meeting1, meeting2])
        actual = sut.sorted()

        self.assertEqual(actual, expected)

    def test_from_json(self):
        data = [
            {
                "start_time": "2021-04-19T12:00:00Z",
                "topic": "Meeting topic",
                "join_url": "https://test.zoom.us/j/0123456789?pwd=password",
                "other_key": "foobar",
            },
        ]
        expected = ScheduledMeetings(
            [
                ScheduledMeeting(
                    datetime(2021, 4, 19, 21, 0, 0),
                    "Meeting topic",
                    "https://test.zoom.us/j/0123456789?pwd=password",
                )
            ]
        )

        actual = ScheduledMeetings.from_json(data)

        self.assertEqual(actual, expected)
