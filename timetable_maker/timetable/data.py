from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import time


@dataclass
class Program:
    start: time
    end: time
    title: str
    rooms: list[str]

    @staticmethod
    def zero_filled_hour(time_str: str) -> str:
        if len(time_str) < len("HH:MM"):
            return f"0{time_str}"
        return time_str

    @classmethod
    def create(
        cls, start_str: str, end_str: str, title: str, rooms: list[str]
    ) -> Program:
        args_dict = {
            "start": time.fromisoformat(cls.zero_filled_hour(start_str)),
            "end": time.fromisoformat(cls.zero_filled_hour(end_str)),
            "title": title,
            "rooms": rooms,
        }
        return cls(**args_dict)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.start < other.start

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.start == other.start


@dataclass
class Programs(Sequence):
    programs: list[Program]

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__class__(self.programs[key])
        return self.programs[key]

    def __len__(self):
        return len(self.programs)

    @classmethod
    def create(cls, program_data):
        programs = [
            Program.create(d["start"], d["end"], d["title"], d["rooms"])
            for d in program_data
        ]
        return cls(sorted(programs))

    def rooms(self):
        rooms_set = set()
        for p in self:
            rooms_set.update(p.rooms)
        return tuple(sorted(rooms_set))
