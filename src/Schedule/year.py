from calendar import Calendar
import datetime
from typing import Dict
from src.Schedule.day import Day
from src.Schedule.week import Week


class Year:
    days: Dict[datetime.date, Day]
    weeks: Dict[int, Day]
    months: Dict[int, Day]

    def __init__(self, year) -> None:
        self.year = year

    def create_year(self):
        self.days = dict()
        c = Calendar()
        for month in range(1, 13):
            days = c.itermonthdays4(self.year, month)
            for day in days:
                date = datetime.date(day[0], day[1], day[2])
                self.days[date] = Day(date, weekday=day[3])

        for day in self.days.values():
            day.create_shifts()

    def assign_weeks(self):
        weeks = [
            list(self.days.values())[i : i + 7]
            for i in range(0, len(self.days), 7)
        ]
        self.weeks = {i + 1: Week(week) for i, week in enumerate(weeks)}
        for week_id, week_obj in self.weeks.items():
            for day in week_obj.days:
                day.week_id = week_id

