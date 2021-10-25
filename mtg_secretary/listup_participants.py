from __future__ import annotations

import argparse
from dataclasses import dataclass
from urllib.request import urlopen

from bs4 import BeautifulSoup


@dataclass
class Attendees:
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
    attendees_list = []
    for div in participants_table_divs:
        attendee_type = find_attendee_type(div.table.thead)
        names = list(iterate_display_name(div.table.tbody))
        attendees = Attendees(attendee_type, names)
        attendees_list.append(attendees)
    return attendees_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("connpass_url")
    args = parser.parse_args()

    url = tidy_participation_url(args.connpass_url)
    with urlopen(url) as res:
        raw_html = res.read()

    attendees_list = parse_participation_page(raw_html)

    for attendees in attendees_list:
        print(f"{attendees.type} ({len(attendees.names)})")
        print("-" * len(attendees.type) * 2)
        for name in attendees.names:
            print(name)
        print()
