from __future__ import annotations

import datetime as dt
from collections.abc import Sequence
from dataclasses import dataclass
from textwrap import dedent

import pytz

ASIA_TOKYO = pytz.timezone("Asia/Tokyo")


@dataclass
class ScheduledMeeting:
    start_datetime: dt.datetime
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

    def __str__(self) -> str:
        string_format = f"""\
            {self.start_datetime}
            {self.topic}
            {self.url}
        """
        # dedentで取れないインデントと、printで2行空かないよう末尾の改行文字を除く
        return dedent(string_format.rstrip())

    # 並び替えにはdataclassが実装する__eq__と以下の__lt__を使う。
    # 1つのZoomアカウントで同じ開始時間のZoom mtgを作るのはナンセンスであり、
    # __eq__を上書きすると、factoryのテストなどの変更が必要になってくる
    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.start_datetime < other.start_datetime


@dataclass
class ScheduledMeetings(Sequence):
    meetings: list[ScheduledMeeting]

    def __getitem__(self, key) -> "ScheduledMeetings" | "ScheduledMeeting":
        if isinstance(key, slice):
            return self.__class__(self.meetings[key])
        return self.meetings[key]

    def __len__(self) -> int:
        return len(self.meetings)

    def sorted(self) -> "ScheduledMeetings":
        return self.__class__(sorted(self.meetings))
