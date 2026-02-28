import matplotlib
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import pytest

from src.study_planner.static_timetable import StaticTimetable
from src.study_planner.timetable import Theme
from src.study_planner.timetable import Course, WeekDay, Timetable
from src.study_planner.themes import LightTheme

matplotlib.use("Agg")  # Prevent GUI backend during testing



class SimpleTheme(Theme):
    fontcolor = "black"
    themecolor = "white"

    def color_list(self, number_of_courses: int) -> list:
        return ["#88c0d0"] * number_of_courses

@pytest.fixture
def layout():
    courses = [
        Course(
            course_name="Math",
            credits_=5,
            week_day=WeekDay.MONDAY,
            start_time="10:00",
            duration_minutes=90,
            room="A1",
            lecturer="Dr. Euler",
        ),
        Course(
            course_name="Physics",
            credits_=4,
            week_day=WeekDay.WEDNESDAY,
            start_time="14:00",
            duration_minutes=120,
            room="B2",
            lecturer="Dr. Newton",
        ),
    ]

    return StaticTimetable(
        courses=courses,
        theme=SimpleTheme(),
        figsize_timetable=(10, 6),
        user="Chavez"
    )


def test_type_static_timetable(layout):
    assert type(layout) == StaticTimetable

def test_display_timetable_returns_figure(layout):
    fig = layout.display_timetable()

    assert isinstance(fig, Figure)