import matplotlib
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import pytest

from src.study_planner.static_timetable import StaticTimetable
from src.study_planner.timetable import Theme
from src.study_planner.timetable import Course, WeekDay, Timetable

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


def test_header_creates_rectangle_per_weekday(layout):
    fig = layout.display_timetable()
    ax_header = fig.axes[0]

    assert len(ax_header.patches) == len(WeekDay)
    assert all(isinstance(p, Rectangle) for p in ax_header.patches)

def test_header_title_contains_username(layout):
    fig = layout.display_timetable()
    ax_header = fig.axes[0]

    assert "Chavez" in ax_header.get_title()

def test_body_axis_is_inverted(layout):
    fig = layout.display_timetable()
    ax_body = fig.axes[1]

    bottom, top = ax_body.get_ylim()
    assert bottom > top

def test_body_has_one_rectangle_per_course(layout):
    fig = layout.display_timetable()
    ax_body = fig.axes[1]

    assert len(ax_body.patches) == 2

def test_course_y_position(layout):
    fig = layout.display_timetable()
    ax_body = fig.axes[1]

    rect = ax_body.patches[0]

    assert rect.get_y() == 10 * 60

def test_course_height_equals_duration(layout):
    fig = layout.display_timetable()
    ax_body = fig.axes[1]

    rect = ax_body.patches[0]
    assert rect.get_height() == 90

def test_vertical_day_lines_exist(layout):
    fig = layout.display_timetable()
    ax_body = fig.axes[1]

    assert len(ax_body.lines) == len(WeekDay)

def test_legend_is_created(layout):
    fig = layout.display_timetable()
    ax_body = fig.axes[1]

    assert ax_body.get_legend() is not None

def test_no_courses_creates_no_patches():
    empty_layout = StaticTimetable(
        courses=[],
        theme=SimpleTheme(),
        figsize_timetable=(10, 6),
        user="Chavez",
    )

    fig = empty_layout.display_timetable()
    ax_body = fig.axes[1]

    assert len(ax_body.patches) == 0

def test_rectangle_width_equals_day_width(layout):
    fig = layout.display_timetable()
    ax_body = fig.axes[1]

    rect = ax_body.patches[0]
    expected_width = 10 / len(WeekDay)

    assert rect.get_width() == expected_width