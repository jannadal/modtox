import datetime
from src.Schedule.shift import Shift


class MockEmployee:
    def __init__(self, slug) -> None:
        self.slug = slug

    def add_shift(self, shift):
        pass


def test_assign_shift():
    s = Shift(datetime.date(2021, 1, 1), n_shift=1, n_workers=2)
    a = MockEmployee("JN")
    b = MockEmployee("AT")
    s.assign(a)
    s.assign(b)
    assert s.workers == [a, b]


def test_slugs():
    s = Shift(datetime.date(2021, 1, 1), n_shift=1, n_workers=2)
    a = MockEmployee("JN")
    b = MockEmployee("AT")
    s.assign(a)
    s.assign(b)
    assert s.slugs == "JN AT"
