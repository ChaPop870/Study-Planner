from datetime import datetime
from pathlib import Path

from src.study_planner.helper_functions import LayoutType, TimetableTheme
from src.study_planner.helper_functions import choose_layout, choose_theme, load_course_data
from src.study_planner.helper_functions import DATA_DIR, _MAX_MINUTES_IN_A_DAY
from src.study_planner.timetable import Course, Timetable, WeekDay


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


def terminal_generation(
        figsize_timetable: tuple[int, int]
) -> None:
    """Generate study-planner using a command line interface."""

    print(show_welcome())

    user = input("\nWhat is your name? ")

    print("The following timetables are available:\n")

    timetable_list = available_timetable_list(DATA_DIR)

    for i, file in enumerate(timetable_list, start = 1):
        print(f"{i}. {file}")

        if i == len(timetable_list):
            print()

    print(instructions())

    while True:
        try:
            selection = int(input("\nChoice: "))

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

            if layout_selection == 1:
                layout_type = "static"
                break

            elif layout_selection == 2:
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

    courses = []

    for i, (subject, row) in enumerate(df.iterrows()):
        course = Course(
            subject,
            row["credits"],
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
    terminal_generation((16, 12))