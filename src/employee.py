from __future__ import annotations
import datetime
from enum import Enum, auto


class VacationError(Exception):
    pass


class Employee:
    def __init__(
        self,
        name: str,
        slug: str,
        is_licensed: bool,
        n_vacation_days: int,
        weekly_hours: int,
    ) -> None:
        self.name = name
        self.slug = slug
        self.is_licensed = is_licensed
        self.weekly_hours = weekly_hours
        self.n_vacation_days = n_vacation_days

        self.vacations = list()
        self.shifts = list()

    def add_shift(self, shift: "Shift"):
        self.shifts.append(shift)

    def add_vacation(
        self, first_day: datetime.date, last_day: datetime.date = None
    ):
        if last_day is None:
            vacations_to_add = [first_day.toordinal()]
        else:
            vacations_to_add = list(
                range(first_day.toordinal(), last_day.toordinal() + 1)
            )
        n_result = len(self.vacations) + len(vacations_to_add)

        if n_result > self.n_vacation_days:
            raise VacationError(
                f"{self.name!r} has currently {len(self.vacations)} days of vacation. "
                f"Adding the specified vacations would result in {n_result} days."
            )
        self.vacations.extend(vacations_to_add)

    def is_on_vacation(self, date: datetime.date):
        return date.toordinal() in self.vacations

    def get_week_shifts(self, week):
        shift_days = {shift.date for shift in self.shifts}
        week_days = {day.date for day in week}
        return len(week_days.intersection(shift_days))

    def score(self):
        pass
