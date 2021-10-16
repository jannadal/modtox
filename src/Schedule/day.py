import datetime
from typing import List
from src.Schedule.shift import Shift


class Day:
    shifts: List[Shift]
    week_id: int

    def __init__(self, date: datetime.date, weekday: int) -> None:

        self.date = date
        self.weekday = weekday

        self.create_shifts()

    def create_shifts(self):
        self.shifts = list()
        if self.weekday in [5, 6]:
            self.shifts.append(Shift(self.date, n_shift=1, n_workers=3))
        elif self.weekday == 4:
            self.shifts.append(Shift(self.date, n_shift=1, n_workers=3))
            self.shifts.append(Shift(self.date, n_shift=2, n_workers=4))
        else:
            self.shifts.append(Shift(self.date, n_shift=1, n_workers=3))
            self.shifts.append(Shift(self.date, n_shift=2, n_workers=3))

    def __str__(self):
        day = f"{self.date.day}/{self.date.month}/{self.date.year}"
        first_shift, second_shift = self.slugs
        return f"{day}\n{first_shift}\n{second_shift}"

    @property
    def slugs(self):
        first_shift = self.shifts[0].slugs
        second_shift = ""
        if len(self.shifts) == 2:
            second_shift = self.shifts[1].slugs
        return first_shift, second_shift
