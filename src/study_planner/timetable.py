from abc import ABC, abstractmethod
from datetime import datetime, time, timedelta
from dataclasses import dataclass, field, asdict
from enum import StrEnum

import numpy as np
import pandas as pd


class WeekDay(StrEnum):
    """Distinct week days by name."""

    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


@dataclass
class Course:
    """ One university course."""
    course_name: str
    credits: int
    week_day: WeekDay
    start_time: str
    duration_minutes: int
    room: str
    lecturer: str

@dataclass
class Timetable:
    """ Timetable containing multiple courses over the week. """
    courses: list[Course] = field(default_factory=list)

    def add_course(self, course: Course):
        self.courses.append(course)

    def to_df(self) -> pd.DataFrame:
        """Generate dataframe representation of timetable."""
        courses_dict = asdict(self)
        courses_df = pd.DataFrame(courses_dict["courses"]).set_index("course_name")
        print(courses_df)
        return courses_df


class Theme(ABC):
    """Abstract base class for themes"""
    @abstractmethod
    def color_list(self, number_of_courses: int) -> list:
        """Creates a list of n colors where n is the number of courses"""
        pass

def minutes_since_midnight(date: str) -> int:
    """Return the number of minutes since midnight"""
    date_as_datetime = datetime.strptime(date, "%H:%M")
    return date_as_datetime.hour * 60 + date_as_datetime.minute


class TimetableLayout(ABC):
    """Abstract base class for timetable layouts"""
    def __init__(self, courses, theme, figsize_timetable, user):
        self.courses = courses
        self.theme = theme
        self.figsize_timetable = figsize_timetable
        self.user = user

    def calc_yrange_for_plotting(self):
        """Calculate the time range on the y-axis for plotting."""
        # earliest_time = datetime(year=1900, month=1, day=2, hour=0, minute=0)
        # latest_time = datetime(year=1900, month=1, day=1, hour=0, minute=0)
        #
        # for subject in self.courses:
        #     endtime = datetime.combine(datetime.today().date(),
        #                                datetime.time(subject.start_time)) + subject.duration_minutes
        #     y = subject.start_time.hour * 60 + subject.start_time.minute  # Any better name that self.y?
        #
        #     if subject.start_time < earliest_time:
        #         earliest_time = subject.start_time
        #     if endtime > latest_time:
        #         latest_time = endtime
        #
        # y_bounds = [
        #     (earliest_time - timedelta(hours=2)).hour,
        #     (latest_time + timedelta(hours=2)).hour,
        # ]
        # y_ticks = np.arange(y_bounds[0] * 60, y_bounds[1] * 60 + 1, 60)

        start_minutes = []
        end_minutes = []

        for subject in self.courses:
            start = minutes_since_midnight(subject.start_time)
            end = minutes_since_midnight(subject.start_time) + subject.duration_minutes

            # Detect rollover past midnight
            if end < start:
                end += 24 * 60

            start_minutes.append(start)
            end_minutes.append(end)

        earliest_time = min(start_minutes)
        earliest_time -= 120

        latest_time = max(end_minutes)
        latest_time += 120

        y_ticks = np.arange(earliest_time, latest_time + 1, 60)

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