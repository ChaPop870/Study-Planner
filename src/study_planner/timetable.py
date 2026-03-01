from abc import ABC, abstractmethod
from datetime import datetime, time, timedelta
from dataclasses import dataclass, field, asdict
from enum import StrEnum

import numpy as np
import pandas as pd


class WeekDay(StrEnum):
    """Distinct weekdays by name."""

    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


@dataclass
class Course:
    """One university course."""
    course_name: str
    credits: int
    week_day: WeekDay
    start_time: str
    duration_minutes: int
    room: str
    lecturer: str


@dataclass
class Timetable:
    """Timetable containing multiple courses over the week."""
    courses: list[Course] = field(default_factory=list)

    def add_course(self, course: Course):
        """Adds a course to the timetable."""
        self.courses.append(course)

    def to_df(self) -> pd.DataFrame:
        """Generate dataframe representation of timetable."""
        courses_dict = asdict(self)
        courses_df = pd.DataFrame(courses_dict["courses"]).set_index("course_name")
        return courses_df

    def __len__(self) -> int:
        """Return the number of courses in the timetable."""
        return len(self.courses)


class Theme(ABC):
    """Abstract base class for themes"""

    @abstractmethod
    def color_list(self, number_of_courses: int) -> list:
        """Creates a list of n colors where n is the number of courses"""
        pass


class TimetableLayout(ABC):
    """Abstract base class for timetable layouts"""
    def __init__(
        self,
        courses: list[Course],
        theme: Theme,
        figsize_timetable: tuple[float, float],
        user: str
    ):
        self.courses = courses
        self.theme = theme
        self.figsize_timetable = figsize_timetable
        self.user = user

    def calc_yrange_for_plotting(self) -> np.ndarray:
        """Calculate the time range on the y-axis for plotting."""
        start_minutes = []
        end_minutes = []

        for subject in self.courses:
            start: int = minutes_since_midnight(subject.start_time)
            end: int = minutes_since_midnight(subject.start_time) + subject.duration_minutes

            # Detect rollover past midnight
            if end < start:
                end += 24 * 60

            start_minutes.append(start)
            end_minutes.append(end)

        earliest_time: int = min(start_minutes) - 120
        latest_time: int = max(end_minutes) + 120

        earliest_hour: int = (earliest_time // 60) * 60
        latest_hour: int = ((latest_time + 59) // 60) * 60

        y_ticks = np.arange(earliest_hour, latest_hour + 1, 60)

        return y_ticks

    @abstractmethod
    def display_timetable(self):
        """Plotting the timetable with courses."""
        pass

    def create_timetable_header(self, ax):
        """Create the timetable header with week days."""
        pass

    def create_timetable_layout(self, ax):
        """Creating timetable layout"""
        pass

    def display_courses(self, ax):
        """Plotting the courses into the timetable layout"""
        pass


def minutes_since_midnight(date: str) -> int:
    """Return the number of minutes since midnight"""
    date_as_datetime = datetime.strptime(date, "%H:%M")
    return date_as_datetime.hour * 60 + date_as_datetime.minute