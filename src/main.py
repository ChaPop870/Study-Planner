from pathlib import Path
from datetime import datetime
from enum import StrEnum

import pandas as pd

from src.study_planner.dynamic_timetable import DynamicTimetable
from src.study_planner.static_timetable import StaticTimetable
from src.study_planner.themes import *
from src.study_planner.timetable import WeekDay, Course, Timetable, TimetableLayout, Theme


_MAX_MINUTES_IN_A_DAY: int = 1440

BASE_DIR: Path = Path(__file__).resolve().parents[1]

DATA_DIR: Path = BASE_DIR / "data"


def get_user_inputs() -> Course:
    """Collect one course entry from the user"""

    course_name = input("Enter course name: ")

    while True:
        try:
            credits_ = int(input("Enter credits: "))
            if credits_ >= 0:
                break
            else:
                print("Invalid input. Credits must be a positive integer")
        except ValueError:
            print("Invalid input. Credits must be a positive integer")

    while True:
        try:
            week_day = WeekDay(input("Enter day (Monday, Tuesday, etc): ").capitalize())
            break
        except ValueError:
            print("Invalid input; please enter day (Monday, Tuesday, etc):")

    while True:
        start = input("Enter start time (HH:MM) in 24 hour format: ")
        try:
            # validate format
            datetime.strptime(start, "%H:%M")
            break
        except ValueError:
            print("Invalid time. Please enter time in HH:MM (24-hour format).")

    while True:
        try:
            duration = int(input("Enter duration (in minutes): "))
            if 0 <= duration <= _MAX_MINUTES_IN_A_DAY:
                break
            else:
                print("Invalid input. Please enter a duration between 0 and "
                      f"{_MAX_MINUTES_IN_A_DAY} minutes.")

        except ValueError:
            print("Invalid time. Please enter time in full minutes.")

    room = input("Enter room: ")

    lecturer = input("Enter lecturer: ")

    return Course(course_name, credits_, week_day, start, duration, room, lecturer)


def generate_csv(user_input: Timetable, name: str = "timetable.csv") -> Path:
    """Generates a csv file from the user's inputs and return its path"""
    df = user_input.to_df()

    choice = input("\n Would you like to name the csv file? (y/n): ").lower()
    if choice == "y":
        name = input("Enter name of csv file: ") + ".csv"

    path = DATA_DIR / name
    df.to_csv(path, index=False)

    return path


def load_course_data(file: str) -> pd.DataFrame:
    """Load course data from csv file in a pandas dataframe"""
    filepath = DATA_DIR / file
    df = pd.read_csv(filepath)
    df = df.set_index("course_name")
    return df


# def prepare_df(data: pd.DataFrame) -> pd.DataFrame:
#     """Prepare a dataframe for plotting"""
#     df = data.copy()
#     # df["start_time"] = pd.to_datetime(df["start_time"], format="%H:%M")
#     # df["duration_minutes"] = pd.to_timedelta(df["duration_minutes"], unit="minutes")
#     #df["end_time"] = df["start_time"] + df["duration_minutes"]
#     return df


def show_welcome() -> str:
    """Prints a welcome message to the user."""
    return "Welcome to Chavez & Marieke's timetable app!\n"


def instructions() -> str:
    """Prints an instructions message to the user."""
    return ("To display the desired timetable, press the index of the timetable. \n"
            "To generate your own timetable, press '0' \n"
            "To exit the app, press '-1'")


def available_timetable_list(directory: Path) -> list[str]:
    """List the csv files from the given directory"""
    file_list = [path.name for path in directory.glob("*.csv")]
    return file_list


class LayoutType(StrEnum):
    """Distinct Layout Type Options by name."""
    STATIC = "static"
    DYNAMIC = "dynamic"

def choose_layout(layout_type, courses, theme, figsize_timetable, user) -> TimetableLayout:
    """Choose a layout type by name."""
    if layout_type == LayoutType.STATIC:
        return StaticTimetable(courses, theme, figsize_timetable, user)
    elif layout_type == LayoutType.DYNAMIC:
        return DynamicTimetable(courses, theme, figsize_timetable, user)
    raise ValueError(f"Unknown timetable type: {layout_type}")


class TimetableTheme(StrEnum):
    """Distinct Timetable Theme Options by name."""
    DARK = "dark"
    LIGHT = "light"
    RAINBOW = "rainbow"
    AUTUMN = "autumn"
    NEUTRAL = "neutral"
    NATURE = "nature"


def choose_theme(theme: TimetableTheme) -> Theme:
    theme_dict: dict[TimetableTheme, Theme] = {
        TimetableTheme.DARK: DarkTheme(),
        TimetableTheme.LIGHT: LightTheme(),
        TimetableTheme.RAINBOW: RainbowTheme(),
        TimetableTheme.AUTUMN: AutumnTheme(),
        TimetableTheme.NEUTRAL: NeutralTheme(),
        TimetableTheme.NATURE: NatureTheme(),
    }

    try:
        return theme_dict[theme]

    except KeyError:
        raise ValueError(f"Unknown theme: {theme}")


def main(layout_type, filename, theme, figsize_timetable, user, auto_generate=True):
    if not auto_generate:
        print(show_welcome())
        print("The following timetables are available:\n")
        timetable_list = available_timetable_list(DATA_DIR)
        for i, file in enumerate(timetable_list, start = 1):
            print(f"{i}. {file}")
            if i == len(timetable_list):
                print()

        print(instructions())

        while True:
            try:
                selection = int(input("Choice: "))

                if selection == -1:
                    print("\nThank you. We hope to see you again!")
                    return

                elif selection == 0:
                    all_users_courses = Timetable()
                    while True:
                        users_course = get_user_inputs()
                        all_users_courses.add_course(users_course)

                        choice = input("\nAdd another course? (y/n): ")
                        if choice != "y":
                            break

                    df = all_users_courses.to_df()
                    # df = prepare_df(df)
                    break

                elif 1 <= selection <= len(timetable_list):
                    filename = timetable_list[selection - 1]
                    df = load_course_data(filename)
                    break

                else:
                    print("Choice out of range. Please select the index from the available files.\n")

                    for i, file in enumerate(timetable_list, start=1):
                        print(f"{i}. {file}")

                        if i == len(timetable_list):
                            print()

            except ValueError:
                print("Invalid choice. Please try again.")

        print("\nHow do you want the display?")

        for i, display in enumerate(LayoutType, start=1):
            print(f"{i}. {display}")

        while True:
            try:
                layout_selection = int(input("\nChoice: "))

                if selection == 1:
                    layout_type = "static"
                    break

                elif selection == 2:
                    layout_type = "dynamic"
                    break

                else:
                    print("Choice out of range. Please select '1' for a static display or '2' for a dynamic display.\n")

            except ValueError:
                print("Invalid choice. Please try again.")

        print("\nSelect your desired theme:")

        for i, _theme in enumerate(TimetableTheme, start = 1):
            print(f"{i}. {_theme}")

        while True:
            try:
                theme_selection = int(input("\nChoice: "))

                if 1 <= theme_selection <= len(TimetableTheme):
                    theme = list(TimetableTheme)[theme_selection - 1]
                    break

                else:
                    print("Out of range. Select the number corresponding to the desired theme.")

            except ValueError:
                print("Invalid choice. Please try again.")



    else:
        df = load_course_data(filename)
        # df = prepare_df(df)

    courses = []

    for i, (subject, row) in enumerate(df.iterrows()):
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
    main(
        layout_type="static",
        filename="planner_template - chavez_pope.csv",
        theme="autumn",
        figsize_timetable=(8, 6),
        user="Marieke",
        auto_generate=True
    )