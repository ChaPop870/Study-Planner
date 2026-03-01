import pytest
from plotly.graph_objects import Figure
import pytest

from src.study_planner.dynamic_timetable import DynamicTimetable
from src.study_planner.timetable import Course, WeekDay, Theme

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

    return DynamicTimetable(
        courses=courses,
        theme=SimpleTheme(),
        figsize_timetable=(10, 6),
        user="Chavez"
    )

def test_type_static_timetable(layout):
    assert type(layout) == DynamicTimetable


def test_display_timetable_returns_figure(layout):
    fig = layout.display_timetable()

    assert isinstance(fig, Figure)

def test_header_creates_rectangle_per_weekday(layout):
    fig = layout.display_timetable()
    shapes = fig.layout.shapes

    assert all(s.type == "rect" for s in shapes[:7])

def test_header_title_contains_username(layout):
    fig = layout.display_timetable()

    assert "Chavez" in fig.layout.title.text

def test_layout_contains_seven_lines(layout):
    fig = layout.display_timetable()
    lines = [s for s in fig.layout.shapes if s.type == "line"]

    assert len(lines) == 7

def test_body_has_one_rectangle_per_course(layout):
    fig = layout.display_timetable()
    courses = [s for s in fig.layout.shapes[7:] if s.type == "rect"]

    assert len(courses) == 2

def test_course_y_position(layout):
    fig = layout.display_timetable()
    courses = [s for s in fig.layout.shapes[7:] if s.type == "rect"]
    first_course = courses[0]

    assert first_course.y1 == 10*60
    assert first_course.y0 == 10*60 + 90

def test_hover_info_exists_on_the_course(layout):
    fig = layout.display_timetable()
    courses = [s for s in fig.layout.shapes[7:] if s.type == "rect"]
    hover_info = fig.data

    assert len(courses) == len(hover_info)

def test_rectangle_width_equals_day_width(layout):
    fig = layout.display_timetable()
    courses = [s for s in fig.layout.shapes[7:] if s.type == "rect"]
    first_course = courses[0]
    course_width = first_course.x1 - first_course.x0
    expected_width = 10 / len(WeekDay) * 100

    assert course_width == expected_width

def test_no_courses_creates_no_patches():
    empty_layout = DynamicTimetable(
        courses=[],
        theme=SimpleTheme(),
        figsize_timetable=(10, 6),
        user="Chavez",
    )

    fig = empty_layout.display_timetable()
    courses = [s for s in fig.layout.shapes[7:] if s.type == "rect"]

    assert len(courses) == 0




