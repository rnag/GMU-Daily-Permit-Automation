# For earlier Python versions like 3.7+
from __future__ import annotations

from datetime import date, timedelta
from enum import IntEnum


class Day(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @classmethod
    def fromstr(cls, weekday: str):
        return cls[weekday.upper()]


def next_day(from_date: date | None = None,
             weekday: Day | int = Day.MONDAY,
             always_next_weekday: bool = False) -> date:

    if from_date is None:
        from_date = date.today()

    # Find the day of the week (0 = Monday, 6 = Sunday)
    day_of_week = from_date.weekday()

    # If weekdays match for `from_date` and `weekday`,
    # return `from_date` if `next_if_same_day` is False
    if weekday == day_of_week and not always_next_weekday:
        return from_date

    # Calculate days until next `weekday`
    days_ahead = (weekday - day_of_week - 1) % 7 + 1

    # Add the calculated days to the current date
    return from_date + timedelta(days=days_ahead)
