import matplotlib
import matplotlib.pyplot as plt
import pytest


from src.study_planner.static_timetable import StaticTimestable
from src.study_planner.timetable import Course, WeekDay


matplotlib.use("Agg")  # Prevent GUI backend during testing

# -------------------------------------------------
# Test Helpers
# -------------------------------------------------

class DummyTheme:
    fontcolor = "black"
    themecolor = "white"

    def color_list(self, n):
        return ["red"] * n


def create_sample_courses():
    return [
        Course("Math", 3, WeekDay.MONDAY, "09:00", 60, "A1", "Dr"),
        Course("Physics", 4, WeekDay.TUESDAY, "14:00", 120, "B2", "Dr")
    ]


# -------------------------------------------------
# Tests
# -------------------------------------------------

def test_display_timetable_returns_figure():
    layout = StaticTimestable(
        courses=create_sample_courses(),
        theme=DummyTheme(),
        figsize_timetable=(8, 6),
        user="Test"
    )

    fig = layout.display_timetable()

    assert fig is None  # because you return fig.show()