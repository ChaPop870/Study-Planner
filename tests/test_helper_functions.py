import pandas as pd
import pytest

from src.study_planner.helper_functions import TimetableTheme
from src.study_planner.helper_functions import load_course_data, choose_layout, choose_theme
from src.study_planner.themes import *
from src.study_planner.timetable import WeekDay, TimetableLayout


def test_load_course_data(tmp_path):
    filepath = tmp_path / "file.csv"
    test_dataframe = pd.DataFrame({
        "course_name": ["Math", "Physics"],
        "credits": [6,4],
        "week_day": [WeekDay.MONDAY, WeekDay.TUESDAY],
        "start_time": ["09:00", "10:00"],
        "duration_minutes": [90, 120],
        "room": ["A1", "B2"],
        "lecturer": ["Dr.Euler", "Dr. Newton"]
    })
    test_dataframe.set_index("course_name", inplace=True)
    test_dataframe.to_csv(str(filepath))
    df_test = load_course_data(str(filepath))

    assert df_test.equals(test_dataframe)


def test_choose_layout():
    courses = []
    theme = "light"
    figsize_timetable = (10, 10)
    user = "Peter"
    static_layout = choose_layout("static", courses, theme, figsize_timetable, user)

    assert isinstance(static_layout, TimetableLayout)


def test_choose_theme_light():
    theme = choose_theme(TimetableTheme.LIGHT)
    assert isinstance(theme, LightTheme)