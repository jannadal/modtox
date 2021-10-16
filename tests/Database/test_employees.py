from employee import Employee
from src.Database.employees import EmployeesDB
from src._custom_errors import RepeatedEmployeeError


import pytest


def test_add_employee():
    db = EmployeesDB()
    data = {
        "name": "Ariadna Tapia",
        "slug": "AT",
        "is_licensed": 0,
        "n_vacation_days": 50,
        "weekly_hours": 20,
    }
    db.add_employee(data)


def test_add_employee_data_error():
    db = EmployeesDB()
    data = {
        "name": "Ariadna Tapia",
        "is_licensed": 0,
        "n_vacation_days": 50,
        "weekly_hours": 20,
    }
    with pytest.raises(TypeError):
        db.add_employee(data)


def test_repeated_employee():
    db = EmployeesDB()
    data = {
        "name": "Jan Nadal",
        "slug": "JJ",
        "is_licensed": 1,
        "n_vacation_days": 30,
        "weekly_hours": 40,
    }
    with pytest.raises(RepeatedEmployeeError):
        db.add_employee(data)


def test_fetch_all():
    db = EmployeesDB()
    employees = db.get_employees()
    return


def test_delete_employee():
    db = EmployeesDB()
    db.delete_employee("AT")
    return

