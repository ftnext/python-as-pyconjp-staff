from __future__ import annotations

import argparse
from dataclasses import dataclass
from urllib.request import urlopen

from bs4 import BeautifulSoup


@dataclass
class AttendeeSubset:
    type: str
    names: list[str]

    def __len__(self):
        return len(self.names)

    def __str__(self):
        return f"{self.type} ({len(self)})"

    def iter_names(self):
        yield from self.names


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
    for div in participants_table_divs:
        attendee_type = find_attendee_type(div.table.thead)
        names = list(iterate_display_name(div.table.tbody))
        yield attendee_type, names


def create_attendee_subsets(html):
    return [
        AttendeeSubset(type_, names)
        for type_, names in parse_participation_page(html)
    ]


def display(attendee_subset):
    print(attendee_subset)
    print("-" * len(attendee_subset.type) * 2)
    for name in attendee_subset.iter_names():
        print(name)
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("connpass_url")
    args = parser.parse_args()

    url = tidy_participation_url(args.connpass_url)
    with urlopen(url) as res:
        raw_html = res.read()

    attendees = create_attendee_subsets(raw_html)

    for attendee_subset in attendees:
        display(attendee_subset)
