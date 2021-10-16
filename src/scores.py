from src.schedule import Shift
from typing import List

scores = {
    "consecutive_day": 5,
    "double_shit": 20,
}


class Scorer:
    def __init__(self, shifts: List[Shift]) -> None:
        self.shifts = shifts

    def double_shift(self):
        days = [shift.date for shift in self.shifts]
        return len(days) != set(days)

    def consecutive_day(self):
        ordinals = [shift.date.toordinal() for shift in self.shifts]
        return

