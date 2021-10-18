import argparse
from urllib.request import urlopen

from bs4 import BeautifulSoup


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
        print(attendee_type)
        print("-" * len(attendee_type) * 2)

        for name in iterate_display_name(div.table.tbody):
            print(name)

        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("connpass_url")
    args = parser.parse_args()

    url = tidy_participation_url(args.connpass_url)
    with urlopen(url) as res:
        raw_html = res.read()

    parse_participation_page(raw_html)
