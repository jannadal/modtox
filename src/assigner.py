from src.Schedule.day import Day

"""Checks the availability of employees and assigns them."""


class WeekDayAssigner:
    def __init__(self, day: Day) -> None:
        self.day = day
        employees = []
