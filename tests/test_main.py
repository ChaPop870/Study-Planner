import pandas as pd
import pytest

from src.study_planner.timetable import WeekDay, Course, Timetable, TimetableLayout, Theme
from src.main import get_user_inputs, load_course_data, available_timetable_list, choose_layout, choose_theme, TimetableTheme
from study_planner.static_timetable import StaticTimetable


def test_get_user_inputs(monkeypatch):
    inputs = iter(["Math", 6, WeekDay.MONDAY, "10:00", 90, "A1", "Dr. Euler"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert get_user_inputs() == Course("Math", 6, WeekDay.MONDAY, "10:00", 90, "A1", "Dr. Euler")



def test_load_course_data(tmp_path):
    filepath = tmp_path / "file.csv"
    test_dataframe = pd.DataFrame({"course_name": ["Math", "Physics"],
                                   "credits_": [6,4],
                                   "week_day": [WeekDay.MONDAY, WeekDay.TUESDAY],
                                   "start_time": ["09:00", "10:00"],
                                   "duration_minutes": [90, 120],
                                   "room": ["A1", "B2"],
                                   "lecturer": ["Dr.Euler", "Dr. Newton"]})
    test_dataframe.set_index("course_name", inplace=True)
    test_dataframe.to_csv(str(filepath))
    df_test = load_course_data(str(filepath))

    assert df_test.equals(test_dataframe)

def test_available_timetable_list(tmp_path):
    filepath = tmp_path / "file.csv"
    file_list = [path.name for path in tmp_path.glob("*.csv")]

    assert file_list == available_timetable_list(filepath)

def test_choose_layout():
    courses = []
    theme = "light"
    figsize_timetable = (10, 10)
    user = "Peter"
    static_layout = choose_layout("static", courses, theme, figsize_timetable, user)

    assert isinstance(static_layout, TimetableLayout)

def test_choose_theme():
    theme = TimetableTheme.LIGHT
    light_theme = choose_theme(theme)

    assert isinstance(light_theme, Theme)
