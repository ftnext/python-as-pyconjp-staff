from datetime import date, datetime, time, timedelta

import timetable

DUMMY_DATE = date(2021, 1, 8)


def increment_time(base_time: time, step_delta: timedelta) -> time:
    dummy_datetime = datetime.combine(DUMMY_DATE, base_time)
    return (dummy_datetime + step_delta).time()


def format_time(time_obj) -> str:
    return time_obj.strftime("%H:%M").lstrip("0")


def build_timetable(
    programs: "timetable.Programs", step_min: int, marker: str
):
    rooms = programs.rooms()
    step_delta = timedelta(minutes=step_min)

    timetable = []
    header = ("time", "program") + rooms
    timetable.append(header)

    start_time = programs[0].start
    for program in programs:
        if program.end < start_time:
            continue  # 今のプログラムは処理し終わったので次の項目へ

        while start_time < program.start:
            # プログラムどうしの合間の時間の行を作る処理
            room_status = tuple("" for room in rooms)
            timetable_row = (format_time(start_time), "") + room_status
            timetable.append(timetable_row)
            start_time = increment_time(start_time, step_delta)

        while program.start <= start_time < program.end:
            room_status = tuple(
                marker if room in program.rooms else "" for room in rooms
            )
            timetable_row = (
                format_time(start_time),
                program.title,
            ) + room_status
            timetable.append(timetable_row)
            start_time = increment_time(start_time, step_delta)

    return timetable
