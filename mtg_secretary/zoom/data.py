import datetime as dt
from dataclasses import dataclass

import pytz

ASIA_TOKYO = pytz.timezone("Asia/Tokyo")


@dataclass
class ScheduledMeeting:
    datetime: dt.datetime
    topic: str
    url: str

    @classmethod
    def create(
        cls, datetime_string: str, topic: str, url: str
    ) -> "ScheduledMeeting":
        naive_dt = dt.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ")
        jst_dt = ASIA_TOKYO.localize(naive_dt)
        jst_naive_dt = (jst_dt + jst_dt.tzinfo.utcoffset(jst_dt)).replace(
            tzinfo=None
        )
        return cls(jst_naive_dt, topic, url)

    def __str__(self):
        return f"""\
{self.datetime}
{self.topic}
{self.url}\
"""