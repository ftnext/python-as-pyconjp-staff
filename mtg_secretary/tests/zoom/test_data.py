from datetime import datetime
from unittest import TestCase

from zoom.data import ScheduledMeeting


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
