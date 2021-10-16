import datetime
from src.employee import Employee


class Shift:
    def __init__(
        self, date: datetime.date, n_shift: int, n_workers: int,
    ) -> None:
        self.date = date
        self.n_shift = n_shift
        self.n_workers = n_workers
        self.workers = list()

    def assign(self, employee: Employee):
        employee.add_shift(self)
        self.workers.append(employee)

    @property
    def slugs(self):
        return " ".join([worker.slug for worker in self.workers])

