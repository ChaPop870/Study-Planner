from src.study_planner.helper_functions import *

def terminal_generation(
        figsize_timetable: tuple[int, int]
):
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
    terminal_generation((16, 12))