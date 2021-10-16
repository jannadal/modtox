import datetime
from typing import List
from src.Schedule.day import Day
import pandas as pd


class WeekdayError(Exception):
    pass


class WeekError(Exception):
    pass


class WeekLengthError(Exception):
    pass


class Week:
    def __init__(self, days: List[Day]) -> None:
        self.validate_length(days)
        self.validate_weekdays(days)
        self.validate_consecutive(days)
        self.days = days

    @staticmethod
    def validate_length(days):
        if len(days) != 7:
            raise WeekLengthError("A week has 7 days.")

    @staticmethod
    def validate_weekdays(days):
        weekdays = sorted([day.weekday for day in days])
        if weekdays != list(range(0, 7)):
            raise WeekdayError("Provided days do not constitute a week.")

    @staticmethod
    def validate_consecutive(days):
        ord_days = sorted([day.date.toordinal() for day in days])
        if ord_days != [ord_days[0] + i for i in range(0, 7)]:
            raise WeekError("Provided days are not consecutive.")

    def to_df(self):
        records = list()
        for day in self.days:
            for shift in day.shifts:
                for worker in shift.workers:
                    rec = [day.weekday, shift.n_shift, worker.name]
                    records.append(rec)
        df = pd.DataFrame(records, columns=["Weekday", "Shift", "Worker"])
        return df

    def __str__(self):
        m = {
            0: "Mon",
            1: "Tue",
            2: "Wed",
            3: "Thu",
            4: "Fri",
            5: "Sat",
            6: "Sun",
        }

        s = "\t\t".join(m.values()) + "\n"

        first_shift_slugs = {day: [] for day in m.values()}
        second_shift_slugs = {day: [] for day in m.values()}
        for week_day, day in enumerate(self.days):
            for i, shift in enumerate(day.shifts):
                for worker in shift.workers:
                    if i == 0:
                        first_shift_slugs[m[week_day]].append(worker.slug)
                    if i == 1:
                        second_shift_slugs[m[week_day]].append(worker.slug)

        for d in [first_shift_slugs, second_shift_slugs]:
            a = [" ".join(workers) for workers in d.values()]
            b = "\t".join(a) + "\n"
            s = s + b

        return s
