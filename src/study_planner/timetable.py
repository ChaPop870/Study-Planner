# Imports
from abc import ABC, abstractmethod
from datetime import datetime, time, timedelta
from pathlib import Path

import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

WEEK_DAYS: list[str] = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR: Path = BASE_DIR / "data"

BLANK_INPUT_DICT: dict[str, list[str | int| str| str| int| str| str]] = {
    "course_name": [],
    "credits": [],
    "day": [],
    "start_time": [],
    "duration": [],
    "room": [],
    "lecturer": []
}

# %%
def get_user_inputs() -> tuple[str, int, str, str, int, str, str]:
    """Collect one course entry from the user"""

    course = input("Enter course name: ")

    while True:
        try:
            cred = int(input("Enter credits: "))
            break
        except ValueError:
            print("Invalid input; please enter an integer.")

    while True:
        try:
            da = input("Enter day (Monday, Tuesday, etc): ").capitalize()
            if da in WEEK_DAYS:
                break
            else:
                print("Invalid input. Please enter a valid day (Monday, Tuesday, etc).")
        except ValueError:
            print("Invalid input; please enter day (Monday, Tuesday, etc):")

    while True:
        start = input("Enter start time (HH:MM) in 24 hour format: ")
        try:
            valid = datetime.strptime(start, "%H:%M")
            break
        except ValueError:
            print("Invalid time. Please enter time in HH:MM (24-hour format).")

    while True:
        try:
            dur = int(input("Enter duration (in minutes): "))
            if dur <= 1440:
                break
            else:
                print("Invalid input. Please enter a valid duration (in minutes). "
                      "Maximum duration is one day (1440 minutes).")

        except ValueError:
            print("Invalid time. Please enter time in full minutes.")

    r = input("Enter room: ")

    lect = input("Enter lecturer: ")

    return course, cred, da, start, dur, r, lect


def dict_from_user_input() -> dict:
    """Generates a dictionary from repeated user inputs"""

    data = BLANK_INPUT_DICT

    choice = "y"
    while choice.lower() == "y":
        course, cred, da, start, dur, r, lect = get_user_inputs()

        data["course_name"].append(course)
        data["credits"].append(cred)
        data["day"].append(da)
        data["start_time"].append(start)
        data["duration"].append(dur)
        data["room"].append(r)
        data["lecturer"].append(lect)

        choice = input("\nAdd another course? (y/n): ")

    return data


def generate_csv(user_input: dict, name: str = "timetable.csv") -> Path:
    """Generates a csv file from the user's inputs and return its path"""
    df = pd.DataFrame(user_input)

    choice = input("\n Would you like to name the csv file? (y/n): ").lower()
    if choice == "y":
        name = input("Enter name of csv file: ") + ".csv"

    path = DATA_DIR / name
    df.to_csv(path, index=False)

    return path


def load_course_data(file: str) -> pd.DataFrame:
    """Load course data from csv file in a padas dataframe"""
    filepath: Path = DATA_DIR / file
    df = pd.read_csv(filepath).set_index("course_name")
    return df


def prepare_df(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df["start_time"] = pd.to_datetime(df["start_time"], format="%H:%M")
    df["duration"] = pd.to_timedelta(df["duration"], unit="minutes")
    df["end_time"] = df["start_time"] + df["duration"]
    return df


def minutes_since_midnight(date: datetime) -> int:
    """Return the number of minutes since midnight"""
    return date.hour * 60 + date.minute


class Course:
    def __init__(
        self,
        name: str,
        credits: int,
        day: str,
        start_time: datetime,
        duration: timedelta,
        room: str,
        lecturer: str,
        color: str,
        figsize_timetable,
    ) -> None:
        self.name = name
        self.credits = credits
        self.day = day
        self.start_time = start_time
        self.duration = duration
        self.room = room
        self.lecturer = lecturer
        self.color = color

        self.end_time = datetime.combine(datetime.today().date(), datetime.time(start_time)) + duration
        self.y = start_time.hour * 60 + start_time.minute # Any better name that self.y?
        day_to_x = {
            day: i * figsize_timetable[0] / len(WEEK_DAYS)
            for i, day in enumerate(WEEK_DAYS)
        }
        self.x = day_to_x[day]


class Timetable(ABC):
    @abstractmethod
    def decorator(self, courses, themecolor, figsize_timetable, user):
        pass


class StaticTimestable(Timetable):

    def decorator(self, courses, themecolor, figsize_timetable, user):
        earliest_time = datetime(year=1900, month=1, day=2, hour=0, minute=0)
        latest_time = datetime(year=1900, month=1, day=1, hour=0, minute=0)

        for subject in courses:
            start = minutes_since_midnight(subject.start_time)
            end = minutes_since_midnight(subject.end_time)

            # Detect rollover past midnight
            if end < start:
                end += 24 * 60

            start_minutes.append(start)
            end_minutes.append(end)

        earliest_time = min(start_minutes)
        earliest_time -= 120

        latest_time = max(end_minutes)
        latest_time += 120

        yticks = np.arange(earliest_time, latest_time + 1, 60)

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
        ax2.set_yticklabels([f"{(h // 60) % 24:02d}:00" for h in yticks])
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

    def decorator(self, courses, themecolor, figsize_timetable, user):
        earliest_time = datetime(year=1900, month=1, day=2, hour=0, minute=0)
        latest_time = datetime(year=1900, month=1, day=1, hour=0, minute=0)

        for subject in courses:
            start = minutes_since_midnight(subject.start_time)
            end = minutes_since_midnight(subject.end_time)

            # Detect rollover past midnight
            if end < start:
                end += 24 * 60

            start_minutes.append(start)
            end_minutes.append(end)

        earliest_time = min(start_minutes)
        earliest_time -= 120

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

        # create timetable in subplot 2:
        daylines = [
            i * figsize_timetable[0] * 100 / len(WEEK_DAYS)
            for i, _ in enumerate(WEEK_DAYS)
        ]
        for x in daylines:
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
            ticktext=[f"{(h // 60) % 24:02d}:00" for h in yticks],
            row=2,
            col=1,
        )
        fig.update_xaxes(visible=False, col=1, row=2)
        fig.update_xaxes(range=[0, figsize_timetable[0] * 100], row=2, col=1)

        return fig.show()


def choose_layout(type) -> Timetable:
    if type == "static":
        return StaticTimestable()
    elif type == "dynamic":
        return DynamicTimetable()
    raise ValueError(f"Unknown timetable type: {type}")


def main(type, filename, themecolor, figsize_timetable, user, auto_generate=True):
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
            subject,
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