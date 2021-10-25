from __future__ import annotations

import argparse
from dataclasses import dataclass
from urllib.request import urlopen

from bs4 import BeautifulSoup


@dataclass
class AttendeeSubset:
    type: str
    names: list[str]


def tidy_participation_url(url: str) -> str:
    """
    >>> tidy_participation_url(
    ...    "https://test.connpass.com/event/123456/participation/")
    'https://test.connpass.com/event/123456/participation/'
    >>> tidy_participation_url(
    ...     "https://test.connpass.com/event/123456/participation")
    'https://test.connpass.com/event/123456/participation/'
    >>> tidy_participation_url("https://test.connpass.com/event/123456/")
    'https://test.connpass.com/event/123456/participation/'
    >>> tidy_participation_url("https://test.connpass.com/event/123456")
    'https://test.connpass.com/event/123456/participation/'
    """
    if not url.endswith("/"):
        url += "/"
    if not url.endswith("participation/"):
        url += "participation/"
    return url


def find_attendee_type(thead):
    # thead.tr.th.span.text でも取れる
    return thead.find("span", "label_ptype_name").text


def iterate_display_name(tbody):
    for tr in tbody.find_all("tr"):
        yield tr.find("p", "display_name").a.text


def parse_participation_page(html):
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body
    participants_table_divs = body.find_all("div", "participation_table_area")
    attendees = []
    for div in participants_table_divs:
        attendee_type = find_attendee_type(div.table.thead)
        names = list(iterate_display_name(div.table.tbody))
        attendee_subset = AttendeeSubset(attendee_type, names)
        attendees.append(attendee_subset)
    return attendees


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("connpass_url")
    args = parser.parse_args()

    url = tidy_participation_url(args.connpass_url)
    with urlopen(url) as res:
        raw_html = res.read()

    attendees = parse_participation_page(raw_html)

    for attendee_subset in attendees:
        print(f"{attendee_subset.type} ({len(attendee_subset.names)})")
        print("-" * len(attendee_subset.type) * 2)
        for name in attendee_subset.names:
            print(name)
        print()
