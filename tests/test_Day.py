import datetime

from mock.mock import PropertyMock
from src.Schedule.day import Day
from src.Schedule.shift import Shift
from mock import patch

# Integration test with shifts
def test_create_shifts_weekday():
    date = datetime.date(2021, 1, 1)
    weekday = Day(date, 1)
    friday = Day(date, 4)
    weekend = Day(date, 5)
    assert len(weekday.shifts) == 2
    assert len(friday.shifts) == 2
    assert len(weekend.shifts) == 1


def test_workers_per_day():
    date = datetime.date(2021, 1, 1)
    weekday = Day(date, 1)
    workers = [shift.n_workers for shift in weekday.shifts]
    assert sum(workers) == 6

    friday = Day(date, 4)
    workers = [shift.n_workers for shift in friday.shifts]
    assert sum(workers) == 7

    weekend = Day(date, 5)
    workers = [shift.n_workers for shift in weekend.shifts]
    assert sum(workers) == 3


@patch("src.Schedule.shift.Shift.slugs", new_callable=PropertyMock)
def test_slugs(mock):
    mock.return_value = "AA BB CC"
    date = datetime.date(2021, 1, 1)
    weekday = Day(date, 0)
    first_slug, second_slug = weekday.slugs
    assert first_slug == second_slug == "AA BB CC"

    weekend = Day(date, 5)
    first_slug, second_slug = weekend.slugs
    assert first_slug == "AA BB CC"
    assert second_slug == ""


@patch("src.Schedule.shift.Shift.slugs", new_callable=PropertyMock)
def test_str_method(mock):
    mock.return_value = "AA BB CC"
    date = datetime.date(2021, 1, 1)
    weekday = Day(date, 1)
    assert weekday.__str__() == "1/1/2021\nAA BB CC\nAA BB CC"

    mock.return_value = "AA BB CC DD"
    friday = Day(date, 4)
    assert friday.__str__() == "1/1/2021\nAA BB CC DD\nAA BB CC DD"

    mock.return_value = "AA BB CC DD"
    weekend = Day(date, 5)
    assert weekend.__str__() == "1/1/2021\nAA BB CC DD\n"

