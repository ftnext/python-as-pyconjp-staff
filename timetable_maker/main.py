from __future__ import annotations

import csv
import textwrap
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime
from enum import Enum
from pathlib import Path

import gspread
import yaml

from timetable import Programs, build_timetable

# for sample.yaml
expected = [
    ("time", "program", "Room A", "Room B", "Room C"),
    ("9:00", "素敵なオープニング", "◯", "◯", "◯"),
    ("9:15", "素敵なオープニング", "◯", "◯", "◯"),
    ("9:30", "素敵なオープニング", "◯", "◯", "◯"),
    ("9:45", "素敵なオープニング", "◯", "◯", "◯"),
    ("10:00", "", "", "", ""),
    ("10:15", "基調講演（すごい人による）", "◯", "", ""),
    ("10:30", "基調講演（すごい人による）", "◯", "", ""),
    ("10:45", "基調講演（すごい人による）", "◯", "", ""),
    ("11:00", "基調講演（すごい人による）", "◯", "", ""),
    ("11:15", "基調講演（すごい人による）", "◯", "", ""),
]


class Mode(Enum):
    CSV_FILE = "to_csv"
    SPREADSHEET = "to_sheet"


def parse_args():
    description = "Create timetable from yaml file."
    parser = ArgumentParser(description=description)
    parser.add_argument("timetable_yaml", type=Path)
    parser.add_argument("--step_min", type=int, default=15)
    parser.add_argument("--marker", default="◯")

    subparsers = parser.add_subparsers(dest="output_mode")

    to_csv_parser_help = """\
    Dump timetable to CSV file.

    Example: Create timetable as CSV with a star as marker
        and 1 line for every 10 minutes

        python %(prog)s --step_min 10 --marker ☆ sample.yml to_csv <CSV path>
    """
    to_csv_parser = subparsers.add_parser(
        Mode.CSV_FILE.value,
        formatter_class=RawDescriptionHelpFormatter,
        help=textwrap.dedent(to_csv_parser_help),
    )
    to_csv_parser.add_argument("output_csv", type=Path)

    to_sheet_parser_help = """\
    Dump timetable to Google spreadsheet.

    Example: Create timetable as spreadsheet with a circle as marker
        and 1 line for every 5 minutes

        python %(prog)s sample.yml --step_min 5 \\
            to_sheet <spreadsheet ID> <service account JSON path> \\
            --output_worksheet_name awesome_timetable

    If you want overwrite the worksheet, specify `--overwrite`.
    """
    to_sheet_parser = subparsers.add_parser(
        Mode.SPREADSHEET.value,
        formatter_class=RawDescriptionHelpFormatter,
        help=textwrap.dedent(to_sheet_parser_help),
    )
    to_sheet_parser.add_argument("output_sheet_id")
    to_sheet_parser.add_argument("service_account_file")
    to_sheet_parser.add_argument(
        "--output_worksheet_name",
        default=f"timetable_{datetime.now():%Y%m%d_%H%M}",
    )
    to_sheet_parser.add_argument("--overwrite", action="store_true")

    return parser.parse_args()


def handle_existing_worksheet(spreadsheet, worksheet_name, do_overwrite):
    """Return worksheet when overwrite, otherwise stash and return None"""
    worksheet = spreadsheet.worksheet(worksheet_name)
    if do_overwrite:
        worksheet.clear()
        return worksheet

    new_title = f"{worksheet_name}_stash_{datetime.now():%Y%m%d_%H%M%S}"
    worksheet.update_title(new_title)
    return None


if __name__ == "__main__":
    args = parse_args()

    with args.timetable_yaml.open(encoding="utf-8") as stream:
        data = yaml.load(stream, Loader=yaml.BaseLoader)

    programs = Programs.create(data)
    timetable = build_timetable(programs, args.step_min, args.marker)

    if args.output_mode == Mode.CSV_FILE.value:
        with args.output_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(timetable)

    if args.output_mode == Mode.SPREADSHEET.value:
        gc = gspread.service_account(filename=args.service_account_file)
        spreadsheet = gc.open_by_key(args.output_sheet_id)

        worksheet_names = {wks.title for wks in spreadsheet.worksheets()}
        worksheet = None
        if args.output_worksheet_name in worksheet_names:
            worksheet = handle_existing_worksheet(
                spreadsheet, args.output_worksheet_name, args.overwrite
            )
        if worksheet is None:
            worksheet = spreadsheet.add_worksheet(
                title=args.output_worksheet_name, rows="1", cols="1"
            )
        worksheet.update("A1", timetable)
