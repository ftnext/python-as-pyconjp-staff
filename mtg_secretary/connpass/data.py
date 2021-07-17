from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class EventInfo:
    title: str
    start_date: str
    start_time: str
    end_date: str
    end_time: str
    mtg_url: str

    @classmethod
    def from_json(cls, json_path: Path) -> EventInfo:
        contents = json_path.read_text()
        data = json.loads(contents)
        return cls(**data)

    def as_dict(self) -> dict:
        return asdict(self)
