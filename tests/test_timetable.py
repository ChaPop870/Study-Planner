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
    timetable = Timetable()
    timetable.add_course(dynamics)
    timetable.add_course(math)

    assert len(timetable) == 2

def test_is_timetable():
    assert type(Timetable([dynamics, math])) == Timetable

def test_to_df_generates_dataframe():
    timetable = Timetable([dynamics, math])
    df = timetable.to_df()

    assert isinstance(df, pd.DataFrame)