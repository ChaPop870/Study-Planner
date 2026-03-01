from src.study_planner.auto_generate import auto_generation
from src.study_planner.terminal_generation import terminal_generation


def main(layout_type, filename, theme, figsize_timetable, user, auto_generate=False):
    if not auto_generate:

        terminal_generation(figsize_timetable)

    else:

        auto_generation(layout_type, filename, theme, figsize_timetable, user)


if __name__ == "__main__":
    main(
        layout_type="static",
        filename="planner_template - chavez_pope.csv",
        theme="autumn",
        figsize_timetable=(8, 6),
        user="Marieke",
        auto_generate=False
    )