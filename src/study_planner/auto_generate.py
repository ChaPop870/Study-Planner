from src.study_planner.timetable import WeekDay, Course, Timetable, TimetableLayout, Theme
from src.study_planner.helper_functions import LayoutType, TimetableTheme
from src.study_planner.helper_functions import load_course_data, choose_layout, choose_theme


def auto_generation(
    layout_type: str,
    filename: str,
    theme,
    figsize_timetable: tuple[int, int],
    user: str,
) -> None:
    """
    Generate and display a timetable without CLI interaction.
    """
    df = load_course_data(filename)

    courses: list[Course] = []

    for subject, row in df.iterrows():
        course = Course(
            subject,
            row["credits_"],
            row["week_day"],
            row["start_time"],
            row["duration_minutes"],
            row["room"],
            row["lecturer"]
        )
        courses.append(course)

    timetable = choose_layout(layout_type, courses, choose_theme(theme), figsize_timetable, user)
    timetable.display_timetable().show()


if __name__ == "__main__":
    auto_generation(
        layout_type=LayoutType.STATIC,
        filename="planner_template - chavez_pope.csv",
        theme=TimetableTheme.DARK,
        figsize_timetable=(10, 10),
        user="Chavez Pope"
    )