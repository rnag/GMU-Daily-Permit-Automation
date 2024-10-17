# For earlier Python versions like 3.7+
from __future__ import annotations

import os
import platform
import subprocess
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


def get_full_name():
    sys = platform.system()
    if sys == "Darwin":  # macOS
        try:
            # Execute 'id -F' to get the full name of the user
            full_name = subprocess.check_output(["id", "-F"]).strip().decode("utf-8")
            return full_name
        except Exception as e:
            return f"Error retrieving full name on macOS: {e}"

    elif sys == "Windows":  # Windows
        try:
            # Get the username
            username = os.getlogin()
            # Access the registry to find the full name
            import winreg

            registry_path = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList'
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            # Check if the username matches
                            profile_image_path = winreg.QueryValueEx(subkey, 'ProfileImagePath')[0]
                            if username in profile_image_path:
                                # Get full name from profile image path or user account properties
                                full_name = winreg.QueryValueEx(subkey, 'FullName')[0] if 'FullName' in winreg.QueryInfoKey(subkey) else os.path.basename(profile_image_path)
                                return full_name
                        except Exception:
                            continue
        except Exception as e:
            return f"Error retrieving full name on Windows: {e}"

    return "Unsupported OS"
