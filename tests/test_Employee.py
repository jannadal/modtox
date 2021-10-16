from src.employee import Employee, VacationError
import datetime
import pytest


def test_slug():
    e = Employee("Ariadna Tapia")
    assert e.slug == "AT"
    e = Employee("ariadna tapia")
    assert e.slug == "AT"
    e = Employee("Ariadna Tapia")
    assert e.slug == "AT"
    e = Employee("Ariadna")
    assert e.slug == "A"


def test_add_shift():
    e = Employee("Ariadna Tapia")
    e.add_shift("S1")
    e.add_shift("S2")
    assert e.shifts == ["S1", "S2"]


def test_add_range_vacation():
    e = Employee("Ariadna Tapia", n_vacation_days=5)
    first_day = datetime.date(2021, 1, 1)
    last_day = datetime.date(2021, 1, 5)
    e.add_vacation(first_day, last_day)

    vacations = [
        datetime.date(2021, 1, 1),
        datetime.date(2021, 1, 2),
        datetime.date(2021, 1, 3),
        datetime.date(2021, 1, 4),
        datetime.date(2021, 1, 5),
    ]

    assert e.vacations == [vac.toordinal() for vac in vacations]


def test_add_single_vacation():
    e = Employee("Ariadna Tapia")
    first_day = datetime.date(2021, 1, 1)
    e.add_vacation(first_day)
    assert e.vacations == [first_day.toordinal()]


def test_raise_vacation_error():
    e = Employee("Ariadna Tapia", n_vacation_days=2)
    with pytest.raises(VacationError):
        e.add_vacation(datetime.date(2021, 1, 1), datetime.date(2021, 1, 3))


def test_is_on_vacation():
    e = Employee("Ariadna Tapia")
    vac_date = datetime.date(2021, 1, 5)
    non_vac_date = datetime.date(2021, 1, 6)
    e.vacations = [vac_date.toordinal()]
    assert e.is_on_vacation(vac_date) == True
    assert e.is_on_vacation(non_vac_date) == False
