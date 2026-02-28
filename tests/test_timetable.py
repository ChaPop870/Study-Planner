import numpy as np
import pandas as pd
import pytest

from src.study_planner.timetable import (
    WeekDay,
    Course,
    Timetable,
    TimetableLayout,
    minutes_since_midnight
)


# Create a few objects
dynamics = Course(
    course_name="Dynamics",
    credits_=6,
    week_day=WeekDay.TUESDAY,
    start_time="20:35",
    duration_minutes=90,
    room="Grindelberg 5",
    lecturer="Nedjeljka Zagar"
)

math = Course(
    course_name="Mathematics",
    credits_=3,
    week_day=WeekDay("Friday"),
    start_time="9:15",
    duration_minutes=120,
    room="Geom 1528",
    lecturer="John Smith"
)

test_timetable = Timetable([dynamics, math])

# test_layout = TimetableLayout(
#     courses=[dynamics, math],
#     theme=None,
#     figsize_timetable=(8, 6),
#     user="tester"
# )


# Tests for WeekDay class
def test_valid_weekday_value():
    assert WeekDay.SUNDAY == "Sunday"
    assert WeekDay("Monday") == WeekDay.MONDAY
    assert WeekDay.FRIDAY != "friday"


def test_weekday_invalid_enum_value():
    with pytest.raises(ValueError):
        WeekDay("Tomorrow")


# Tests for Course Class
def test_is_valid_attribute():
    assert dynamics.course_name == "Dynamics"
    assert dynamics.credits_ == 6
    assert dynamics.week_day == WeekDay.TUESDAY

def test_is_course():
    assert type(dynamics) == Course
    assert type(math) == Course


# Tests for Timetable Class
def test_add_course():
    new_timetable = Timetable()
    new_timetable.add_course(dynamics)
    new_timetable.add_course(math)

    assert len(new_timetable) == 2

def test_is_timetable():
    assert type(test_timetable) == Timetable

def test_to_df_generates_dataframe():
    df = test_timetable.to_df()

    assert isinstance(df, pd.DataFrame)


# Tests for Timetablelayout Class

# def is_timetable_layout():
#     test_layout = TimetableLayout()
#
#     assert type()

# Tests for yrange_plotting function
# def test_yrange_for_plotting():
#


# Testing functions
def test_minutes_since_midnight():
    assert minutes_since_midnight("0:00") == 0
    assert minutes_since_midnight("2:20") == 140

def test_minutes_since_midnight_invalid_format():
    with pytest.raises(ValueError):
        minutes_since_midnight("25:00")


# Testing calc_yrange_for_plotting function
def calc_yrange_for_plotting():
    start = minutes_since_midnight("23:00")
    end = minutes_since_midnight("1:00")

    # Midnight Rollover
    if end < start:
        end += 24 * 60

    start_minutes.append(start)
    end_minutes.append(end)

    assert start_minutes[0] == 1380
    assert end_minutes[0] == 1500

    # 2-hour padding
    earliest_time = min(start_minutes) - 120
    latest_time = max(end_minutes) + 120

    earliest_hour = (earliest_time // 60) * 60
    latest_hour = ((latest_time + 59) // 60) * 60

    assert earliest_hour == 1260
    assert latest_hour == 1620

    # Y-ticks for labelling y-axis.
    y_ticks = np.arange(earliest_hour, latest_hour + 1, 60)

    assert y_ticks == np.array([1260, 1320, 1380, 1440, 1500, 1560, 1620])