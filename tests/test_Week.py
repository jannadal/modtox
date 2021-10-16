import datetime
from src.Schedule.week import Week, WeekError, WeekLengthError, WeekdayError
from src.Schedule.day import Day

import pytest


def test_len_error():
    days = [
        Day(datetime.date(2021, 1, 1), 0),
        Day(datetime.date(2021, 1, 2), 1),
        Day(datetime.date(2021, 1, 3), 2),
        Day(datetime.date(2021, 1, 4), 3),
        Day(datetime.date(2021, 1, 5), 4),
    ]
    with pytest.raises(WeekLengthError):
        w = Week(days)


def test_weekday_error():
    days = [
        Day(datetime.date(2021, 1, 1), 0),
        Day(datetime.date(2021, 1, 2), 1),
        Day(datetime.date(2021, 1, 3), 2),
        Day(datetime.date(2021, 1, 4), 3),
        Day(datetime.date(2021, 1, 5), 4),
        Day(datetime.date(2021, 1, 6), 5),
        Day(datetime.date(2021, 1, 7), 5),
    ]
    with pytest.raises(WeekdayError):
        w = Week(days)


def test_week_error():
    days = [
        Day(datetime.date(2021, 1, 1), 0),
        Day(datetime.date(2021, 1, 2), 1),
        Day(datetime.date(2021, 1, 3), 2),
        Day(datetime.date(2021, 1, 4), 3),
        Day(datetime.date(2021, 1, 5), 4),
        Day(datetime.date(2021, 1, 6), 5),
        Day(datetime.date(2021, 1, 6), 6),
    ]
    with pytest.raises(WeekError):
        w = Week(days)


def test_no_error():
    days = [
        Day(datetime.date(2021, 1, 1), 0),
        Day(datetime.date(2021, 1, 2), 1),
        Day(datetime.date(2021, 1, 3), 2),
        Day(datetime.date(2021, 1, 4), 3),
        Day(datetime.date(2021, 1, 5), 4),
        Day(datetime.date(2021, 1, 6), 5),
        Day(datetime.date(2021, 1, 7), 6),
    ]
    w = Week(days)
    assert w.days == days
