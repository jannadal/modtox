from sqlite3.dbapi2 import IntegrityError
from src.Database.db_manager import DatabaseManager
from src._custom_errors import RepeatedEmployeeError
from typing import Dict

from src.employee import Employee


class EmployeesDB:
    def __init__(self) -> None:
        self.db = DatabaseManager("database.db")
        self.table_name = "employees"
        self.columns = {
            "id": "integer primary key autoincrement",
            "name": "text not null",
            "slug": "text not null unique",
            "is_licensed": "integer not null",
            "n_vacation_days": "integer not null",
            "weekly_hours": "integer not null",
        }
        self.db.create_table(self.table_name, self.columns)

    def add_employee(self, data: Dict):
        required_keys = set(self.columns.keys())
        required_keys.remove("id")
        if set(data.keys()) != set(required_keys):
            raise TypeError("Supplied data does not match database format.")
        try:
            self.db.add(self.table_name, data)
        except IntegrityError as e:
            raise RepeatedEmployeeError("Employee already in database.")

    def fetch_all(self):
        result = self.db.select(self.table_name)
        employees = [
            {
                field: value
                for field, value in zip(self.columns.keys(), employee)
            }
            for employee in result
        ]
        return employees

    def get_employees(self):
        employees = list()
        for employee in self.fetch_all():
            employees.append(
                Employee(
                    name=employee["name"],
                    slug=employee["slug"],
                    is_licensed=bool(employee["is_licensed"]),
                    n_vacation_days=employee["n_vacation_days"],
                    weekly_hours=employee["weekly_hours"],
                )
            )
        return employees

    def delete_employee(self, slug):
        self.db.delete(self.table_name, {"slug": slug})

    def update_employee(self, slug, new_data):
        required_keys = set(self.columns.keys())
        required_keys.remove("id")

        if set(new_data.keys()) != set(required_keys):
            raise TypeError("Supplied data does not match database format.")
        try:
            self.db.update(self.table_name, {"slug": slug}, new_data)
        except IntegrityError as e:
            raise RepeatedEmployeeError("Employee already in database.")

    def _delete_table(self):
        self.db.drop_table(self.table_name)

