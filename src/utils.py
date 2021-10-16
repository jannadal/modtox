from calendar import Calendar
import datetime
from src.schedule import Day

c = Calendar()

month = c.itermonthdays4(2021, 1)

year = dict()


def create_year(year):
    year = dict()
    for month in range(1, 13):
        for day in c.itermonthdays4(year, month):
            date = datetime.date(day[0], day[1], day[2])
            year[date] = Day(date, day[4])
    return year


def create_month(year, month):
    d = dict()
    for day in c.itermonthdays4(year, month):
        date = datetime.date(day[0], day[1], day[2])
        d[date] = Day(date, day[3])
    return d

