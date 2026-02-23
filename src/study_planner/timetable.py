# Imports  # remove, obvious imports clutter teh code (-> see old slides coding style)
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from enum import StrEnum
from pathlib import Path

import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

_MAX_MINUTES_IN_A_DAY = 1440

# If you have a distinct list of values, you can use Enums.
#  I gave you an example below.
WEEK_DAYS: list[str] = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]

# You can work with the values as with strings, but the options are limited
# class WeekDay(StrEnum):
#     """Distinct week days by name."""
#
#     SUNDAY = "Sunday"
#     MONDAY = "Monday"
#     TUESDAY = "Tuesday"
#     WEDNESDAY = "Wednesday"
#     THURSDAY = "Thursday"
#     FRIDAY = "Friday"
#     SATURDAY = "Saturday"



BASE_DIR = Path(__file__).resolve().parents[2]

# types are especially relevant in function signatures and on attributes.
#  If the value you assign already has a clear type, explicit typing is not necessary
DATA_DIR = BASE_DIR / "data"

# you should not store data on a module level.
# If you would work with multiple planners, this would mix up planners.
# Below is an example how you can utilize (data-) classes to store the information.
BLANK_INPUT_DICT: dict[str, list[str | int| str| str| int| str| str]] = {
    "course_name": [],
    "credits": [],
    "day": [],
    "start_time": [],
    "duration": [],
    "room": [],
    "lecturer": []
}

# @dataclass
# class Course:
#     """One university course."""
#
#     course_name: str
#     credits: int
#     week_day: WeekDay
#     start_time: str
#     duration_minutes: int
#     room: str
#     lecturer: str
#
# @dataclass
# class Timetable:
#     """Timetable containing multiple courses over the week."""
#
#     courses: list[Course] = field(default_factory=list)
#
#     def to_df(self) -> pd.DataFrame:
#         """Generate DataFrame representation of timetable."""
#         ...  # hint: use alist comprehension, `from dataclasses import asdict` and `pd.DataFrame.from_records`
#
# # Examples
# sample_course = Course(
#     course_name='sample_course',
#     credits=1,
#     week_day=WeekDay.MONDAY,
#     start_time="12:00",
#     duration_minutes=60,
#     room="63-580",
#     lecturer="Bob",
# )
# timetable_bob = Timetable()
# timetable_bob.courses.append(sample_course)


# %%  # remove, it is a nice feature during development, but once a function is written, it can be removed :)
# def get_user_inputs() -> Course:
def get_user_inputs() -> tuple[str, int, str, str, int, str, str]:
    """Collect one course entry from the user."""

    course = input("Enter course name: ")

    while True:
        try:
            credits = int(input("Enter credits: "))
            break
        except ValueError:
            print("Invalid input; please enter an integer.")

    while True:
        try:
            week_day = input("Enter day (Monday, Tuesday, etc): ").capitalize()  # Variable names should speak for themselves
            # week_day = WeekDay(input("Enter day (Monday, Tuesday, etc): "))  # following check would be unnecessary
            if week_day in WEEK_DAYS:
                break
            else:
                print("Invalid input. Please enter a valid day (Monday, Tuesday, etc).")
        except ValueError:
            print("Invalid input; please enter day (Monday, Tuesday, etc):")

    while True:
        start = input("Enter start time (HH:MM) in 24 hour format: ")
        try:
            # The following line is a good example for a good comment,
            # otherwise someone would be irritated about code which isn't assigned to a variable.
            # btw. Why are you not using datetime.time, but instead a string?

            # verify format
            datetime.strptime(start, "%H:%M")  # value not needed
            break
        except ValueError:
            print("Invalid time. Please enter time in HH:MM (24-hour format).")

    while True:
        try:
            duration = int(input("Enter duration (in minutes): "))  # Variable names should speak for themselves
            if duration <= _MAX_MINUTES_IN_A_DAY:
                break
            else:
                print("Invalid input. Please enter a valid duration (in minutes). "
                      f"Maximum duration is one day ({_MAX_MINUTES_IN_A_DAY} minutes).")

        except ValueError:
            print("Invalid time. Please enter time in full minutes.")

    room = input("Enter room: ")  # Variable names should speak for themselves

    lecturer = input("Enter lecturer: ")  # Variable names should speak for themselves

    return course, credits, week_day, start, duration, room, lecturer
    # return Course(course, credits, week_day, start, duration, room, lecturer)


# Generally speaking names of function etc. should be domain based. a "dict" could be everything...
# Ask yourself: "What does the dictionary represent domain-wise.
def dict_from_user_input() -> dict:  # return type to broad, maybe use Timetable class instead
    """Generates a dictionary from repeated user inputs."""

    data = BLANK_INPUT_DICT  # This will just link the BLANK, but will not copy it.

    choice = "y"
    while choice.lower() == "y":
        course, cred, da, start, dur, r, lect = get_user_inputs()

        # The following structure is quite vulnerable to changes of the keys.
        # That's why the (data-)classes make sense. :)
        data["course_name"].append(course)
        data["credits"].append(cred)
        data["day"].append(da)
        data["start_time"].append(start)
        data["duration"].append(dur)
        data["room"].append(r)
        data["lecturer"].append(lect)

        choice = input("\nAdd another course? (y/n): ")

    return data


# def generate_csv(user_input: Timetable, file_name: str = "timetable.csv") -> Path:
def generate_csv(user_input: dict, file_name: str = "timetable.csv") -> Path:
    """Generates a csv file from the user's inputs and return its path."""
    df = pd.DataFrame(user_input)  # how to do this is hinted in the class definition

    choice = input("\n Would you like to name the csv file? (y/n): ").lower()
    if choice == "y":
        file_name = f'{input("Enter name of csv file: ")}.csv"'  # fstrings are the preferred way for this as strings. "Addition" of strings is considered bad style.

    path = DATA_DIR / file_name
    df.to_csv(path, index=False)

    return path


def load_course_data(file: str) -> pd.DataFrame:
    """Load course data from csv file in a padas dataframe."""
    filepath: Path = DATA_DIR / file
    df = pd.read_csv(filepath).set_index("course_name")
    return df


def prepare_df(data: pd.DataFrame) -> pd.DataFrame:
    """Docstring."""
    df = data.copy()
    df["start_time"] = pd.to_datetime(df["start_time"], format="%H:%M")
    df["duration"] = pd.to_timedelta(df["duration"], unit="minutes")
    df["end_time"] = df["start_time"] + df["duration"]
    return df


# Haven't seen this definition before my suggestion at the top. Maybe reuse my dataclass approach to be slightly shorter.
# No the question rises for me: Why do handle the "BLANK_..." dict structure if you could directly use a list of courses
# (in the data class case you can set additional attributes in the `__post_init__()` method)
class Course:
    """Docstring."""

    def __init__(
        self,
        name: str,
        credits: int,  # unfortunately "credits" is a build-in function. The usual way to circumvent this is like this: "credits_"
        day: str,
        start_time: datetime,
        duration: timedelta,
        room: str,
        lecturer: str,
        color: str,
        figsize_timetable,  # type? and why is this part of the course? Seems to be a visualization aspect...
    ) -> None:
        """Docstring."""
        self.name = name
        self.credits = credits
        self.day = day
        self.start_time = start_time
        self.duration = duration
        self.room = room
        self.lecturer = lecturer
        self.color = color

        self.endtime = datetime.combine(datetime.today().date(), datetime.time(start_time)) + duration
        self.y = start_time.hour * 60 + start_time.minute # Any better name that self.y?
        day_to_x = {
            day: i * figsize_timetable[0] / len(WEEK_DAYS)
            for i, day in enumerate(WEEK_DAYS)
        }
        self.x = day_to_x[day]


class Timetable(ABC):
    """Docstring."""

    @abstractmethod
    def decorator(self, courses, themecolor, figsize_timetable, user):  # typing, and maybe you can come up with a better method name. Maybe `show`/`display`?
        """Docstring."""
        pass


class StaticTimestable(Timetable):
    """Docstring."""

    def decorator(self, courses, themecolor, figsize_timetable, user):  # typing
        """Docstring."""
        # please divide the method in to smaller protected methods. It is doing a lot!
        earliest_time = datetime(year=1900, month=1, day=2, hour=0, minute=0)
        latest_time = datetime(year=1900, month=1, day=1, hour=0, minute=0)

        for subject in courses:
            if subject.start_time < earliest_time:
                earliest_time = subject.start_time
            if subject.endtime > latest_time:
                latest_time = subject.endtime

        y_bounds = [
            (earliest_time - timedelta(hours=2)).hour,
            (latest_time + timedelta(hours=2)).hour,
        ]
        yticks = np.arange(y_bounds[0] * 60, y_bounds[1] * 60 + 1, 60)

        height_ratios = [1, 8]
        day_width = figsize_timetable[0] / len(WEEK_DAYS)
        text_offset = [day_width / 2, height_ratios[0] / 2]

        fig = plt.figure(figsize=figsize_timetable)
        fig.subplots_adjust(left=0.1, right=0.95)
        gs = fig.add_gridspec(2, 1, height_ratios=height_ratios, hspace=0.0)

        # ax1 for days
        ax1 = fig.add_subplot(gs[0])
        for i in range(len(WEEK_DAYS)):
            rec = Rectangle(
                (i * day_width, 0),
                day_width,
                1,
                edgecolor="black",
                facecolor=themecolor,
            )
            ax1.add_patch(rec)

            ax1.text(
                i * day_width + text_offset[0],
                text_offset[1],
                f"{WEEK_DAYS[i]}",
                ha="center",
                va="center",
                fontsize=12,
            )

        ax1.set_xlim(0, figsize_timetable[0])
        ax1.set_ylim(0, 1)
        ax1.axis("off")
        ax1.set_title(
            f"{user}'s Study Timetable \n",
            fontsize=16,
            color=themecolor,
            fontweight="bold",
        )

        # ax2 for actual timetable
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        ax2.set_yticks(yticks)
        ax2.set_ylim(yticks[0], yticks[-1])
        ax2.invert_yaxis()
        ax2.set_yticklabels([f"{int(h / 60):02d}:00" for h in yticks])
        ax2.set_ylabel("Hour")
        ax2.set_xticks([])
        daylines = [
            i * figsize_timetable[0] / len(WEEK_DAYS) for i, day in enumerate(WEEK_DAYS)
        ]
        for x in daylines:
            ax2.axvline(x, color="black", alpha=0.5)

        # plotting the courses:
        for subject in courses:
            width = figsize_timetable[0] / len(WEEK_DAYS)  # One day wide
            height = (subject.duration).total_seconds() / 60  # Duration in minutes

            period = Rectangle(
                xy=(subject.x, subject.y),
                width=width,
                height=height,
                facecolor=subject.color,
                edgecolor="black",
                label=subject.name,
            )
            ax2.add_patch(period)
            ax2.text(
                subject.x + width * 0.3, subject.y + height * 0.7, subject.name[0:6]
            )

        ax2.legend()

        return fig.show()


class DynamicTimetable(Timetable):
    """Docstring."""

    def decorator(self, courses, themecolor, figsize_timetable, user):  # typing
        """Docstring."""
        # please divide the method in to smaller protected methods. It is doing a lot!
        earliest_time = datetime(year=1900, month=1, day=2, hour=0, minute=0)
        latest_time = datetime(year=1900, month=1, day=1, hour=0, minute=0)

        for subject in courses:
            if subject.start_time < earliest_time:
                earliest_time = subject.start_time
            if subject.endtime > latest_time:
                latest_time = subject.endtime

        y_bounds = [
            (earliest_time - timedelta(hours=2)).hour,
            (latest_time + timedelta(hours=2)).hour,
        ]
        yticks = np.arange(y_bounds[0] * 60, y_bounds[1] * 60 + 1, 60)

        height_ratios = [1, 8]
        day_width = figsize_timetable[0] / len(WEEK_DAYS)
        text_offset = [day_width / 2, height_ratios[0] / 2]

        fig = make_subplots(
            2, 1, shared_xaxes=True, vertical_spacing=0, row_heights=height_ratios
        )
        fig.update_layout(title=f"{user}'s Study Timetable")

        # create the days as a header in subplot 1:
        for i in range(len(WEEK_DAYS)):
            fig.add_shape(
                type="rect",
                x0=i * day_width * 100,
                x1=i * day_width * 100 + day_width * 100,
                y0=0,
                y1=1,
                xref="x1",
                yref="y1",
                row=1,
                col=1,
                fillcolor=themecolor,
                # opacity = 0.5
            )

            fig.add_annotation(
                x=(i * day_width + text_offset[0]) * 100,
                y=text_offset[1],
                text=f"{WEEK_DAYS[i]}",
                showarrow=False,
                col=1,
                row=1,
            )
        fig.update_yaxes(range=[0, height_ratios[0]], visible=False, col=1, row=1)

        # create timetable in subplot 2:  # this could be a sub method with a name like the comment.
        # -> removes comment, makes structure clear by good naming of methods. -> Jackpot
        day_lines = [
            i * figsize_timetable[0] * 100 / len(WEEK_DAYS)
            for i, _ in enumerate(WEEK_DAYS)
        ]
        for x in day_lines:
            fig.add_shape(
                type="line",
                x0=x,
                x1=x,
                y0=yticks[0],
                y1=yticks[-1],
                xref="x2",
                yref="y2",
                opacity=0.5,
                fillcolor="black",
                col=1,
                row=2,
            )

        # plot the courses:
        for subject in courses:
            fig.add_shape(
                type="rect",
                x0=subject.x * 100,
                x1=subject.x * 100 + day_width * 100,
                y1=subject.y,
                y0=subject.y + int((subject.duration).total_seconds() / 60),
                xref="x2",
                yref="y2",
                fillcolor=subject.color,
                col=1,
                row=2,
            )
            fig.add_annotation(
                x=(subject.x * 100 + 0.5 * day_width * 100),
                y=subject.y + 0.5 * int((subject.duration).total_seconds() / 60),
                text=f"{subject.name[:6]}",
                showarrow=False,
                col=1,
                row=2,
            )
            # add hover info:
            fig.add_trace(
                go.Scatter(
                    x=[subject.x * 100 + 0.5 * day_width * 100],
                    y=[subject.y + 0.5 * int((subject.duration).total_seconds() / 60)],
                    marker=dict(
                        size=int((subject.duration).total_seconds() / 60), opacity=0
                    ),
                    mode="markers",
                    hovertemplate=f"<b>{subject.name}</b> "
                    f"<br> {subject.lecturer}"
                    f"<br> {subject.room}"
                    f"<br> {subject.start_time.time()}"
                    f"<br> {subject.endtime.time()}"
                    f"<extra></extra>",
                    showlegend=False,
                ),
                row=2,
                col=1,
            )

        fig.update_yaxes(
            title_text="Hour",
            range=[max(yticks), min(yticks)],
            tickvals=yticks,
            ticktext=[f"{int(h / 60):02d}:00" for h in yticks],
            row=2,
            col=1,
        )
        fig.update_xaxes(visible=False, col=1, row=2)
        fig.update_xaxes(range=[0, figsize_timetable[0] * 100], row=2, col=1)

        return fig.show()


def choose_layout(type) -> Timetable:
    if type == "static":  # Could be an Enum if it has limited options.
        return StaticTimestable()
    elif type == "dynamic":  # Could be an Enum if it has limited options.
        return DynamicTimetable()
    raise ValueError(f"Unknown timetable type: {type}")


def main(type, filename, themecolor, figsize_timetable, user, auto_generate=True):  # typing
    """Docstring."""
    if not auto_generate:
        user_data = dict_from_user_input()
        csv_path = generate_csv(user_data)
        filename = csv_path

    df = load_course_data(filename)
    df = prepare_df(df)
    courses = []
    colors = list(mcolors.CSS4_COLORS)

    for i, (subject, row) in enumerate(df.iterrows()):
        course = Course(
            subject,  # typing is off "Expected type 'str', got 'Hashable' instead"
            row["credits"],
            row["day"],
            row["start_time"],
            row["duration"],
            row["room"],
            row["lecturer"],
            colors[i + i * 7],
            figsize_timetable,
        )
        courses.append(course)

    timetable = choose_layout(type)
    timetable.decorator(courses, themecolor, figsize_timetable, user)


if __name__ == "__main__":
    main(
        type="dynamic",
        filename="planner_template - chavez_pope.csv",
        themecolor="skyblue",
        figsize_timetable=(8, 6),
        user="Marieke",
        auto_generate=True
    )