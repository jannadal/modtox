import datetime
from src.Schedule.year import Year
from src.Schedule.day import Day
from src.employee import Employee
import random


def test_create_year():
    y = Year(2021)
    y.create_year()
    assert isinstance(list(y.days.keys())[0], datetime.date)
    assert isinstance(list(y.days.values())[0], Day)
    assert len(y.days) == 371


employees = [
    "Jan Nadal",
    "Ariadna Tapia",
    "Maria Miró",
    "Pau Catasús",
    "Pedro Giménez",
    "Raimon Cambra",
    "Manel Nadal",
]

emps = [Employee(emp) for emp in employees]


def test_create_weeks():
    y = Year(2021)
    y.create_year()
    y.assign_weeks()
    for day in y.weeks[1].days:
        lst = emps.copy()
        for shift in day.shifts:
            for _ in range(shift.n_workers):
                r = lst.pop(random.randint(0, len(lst) - 1))
                shift.assign(r)

    df = y.weeks[1].to_df()
    return
