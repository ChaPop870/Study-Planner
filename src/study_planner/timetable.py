# Imports
from abc import ABC, abstractmethod
from datetime import datetime, time, timedelta
from pathlib import Path
import matplotlib.patheffects as pe
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
print("base dir:" , BASE_DIR)

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
        figsize_timetable,
    ) -> None:
        self.name = name
        self.credits = credits
        self.day = day
        self.start_time = start_time
        self.duration = duration
        self.room = room
        self.lecturer = lecturer

        self.endtime = datetime.combine(datetime.today().date(), datetime.time(start_time)) + duration
        self.y = start_time.hour * 60 + start_time.minute # Any better name that self.y?
        day_to_x = {
            day: i * figsize_timetable[0] / len(WEEK_DAYS)
            for i, day in enumerate(WEEK_DAYS)
        }
        self.x = day_to_x[day]


class Theme(ABC):
    @abstractmethod
    def color_list(self, number_of_courses: int) -> list:
        pass


class DarkTheme(Theme):
    def __init__(self):
        self.cmap = plt.get_cmap("bone")
        self.themecolor = "midnightblue"
        self.fontcolor = "white"

    def color_list(self, number_of_courses: int) -> list:
        return [self.cmap(i) for i in np.linspace(0.1, 0.5, number_of_courses)]

class LightTheme(Theme):
    def __init__(self):
        self.cmap = plt.get_cmap("Blues")
        self.themecolor = "powderblue"
        self.fontcolor = "black"

    def color_list(self, number_of_courses: int) -> list:
        return [self.cmap(i) for i in np.linspace(0.2, 0.6, number_of_courses)]

class RainbowTheme(Theme):
    def __init__(self):
        self.cmap = plt.get_cmap("rainbow")
        self.themecolor = "crimson"
        self.fontcolor = "lightgrey"

    def color_list(self, number_of_courses: int) -> list:
        return [self.cmap(i) for i in np.linspace(0, 1, number_of_courses)]

class AutumnTheme(Theme):
    def __init__(self):
        self.cmap = plt.get_cmap("autumn")
        self.themecolor = "maroon"
        self.fontcolor = "white"

    def color_list(self, number_of_courses: int) -> list:
        return [self.cmap(i) for i in np.linspace(0, 0.85, number_of_courses)]

class NeutralTheme(Theme):
    def __init__(self):
        self.cmap = plt.get_cmap("copper")
        self.themecolor = "tan"
        self.fontcolor = "black"

    def color_list(self, number_of_courses: int) -> list:
        return [self.cmap(i) for i in np.linspace(0.25, 1, number_of_courses)]

class NatureTheme(Theme):
    def __init__(self):
        self.cmap = plt.get_cmap("summer")
        self.themecolor = "lightgreen"
        self.fontcolor = "darkslategrey"

    def color_list(self, number_of_courses: int) -> list:
        return [self.cmap(i) for i in np.linspace(0, 1, number_of_courses)]



class Timetable(ABC):
    @abstractmethod
    def decorator(self, courses, theme, figsize_timetable, user):
        pass


class StaticTimestable(Timetable):
    def decorator(self, courses, theme, figsize_timetable, user):
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
                edgecolor=theme.fontcolor,
                facecolor=theme.themecolor,  # theme.color_list(len(courses))[0],
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
        title = ax1.set_title(
            f"{user}'s Study Timetable \n",
            fontsize=16,
            color=theme.themecolor,  # theme.color_list(len(courses))[0],
            fontweight="bold",
        )
        title.set_path_effects(
            [pe.withStroke(linewidth=2, foreground=theme.fontcolor)
             ])

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
            ax2.axvline(x, color=theme.fontcolor, alpha=0.5)

            # plotting the courses:
            for i_subject, subject in enumerate(courses):
                width = figsize_timetable[0] / len(WEEK_DAYS)  # One day wide
                height = (subject.duration).total_seconds() / 60  # Duration in minutes

                period = Rectangle(
                    xy=(subject.x, subject.y),
                    width=width,
                    height=height,
                    facecolor=theme.color_list(len(courses))[i_subject],
                    edgecolor=theme.fontcolor,
                    label=subject.name,
                )
                ax2.add_patch(period)
                ax2.text(
                    subject.x + width * 0.3, subject.y + height * 0.7, subject.name[0:6]
                )

            ax2.legend()

            return fig.show()


class DynamicTimetable(Timetable):
    def decorator(self, courses, theme, figsize_timetable, user):
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
        fig.update_layout(title_font_color = mcolors.to_hex(theme.themecolor),
                          title_font_shadow = "auto")

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
                fillcolor=mcolors.to_hex(theme.themecolor),
                # opacity = 0.5
            )

            fig.add_annotation(
                x=(i * day_width + text_offset[0]) * 100,
                y=text_offset[1],
                text=f"{WEEK_DAYS[i]}",
                showarrow=False,
                col=1,
                row=1,
                font={"color": mcolors.to_hex(theme.fontcolor)},
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
                fillcolor=mcolors.to_hex(theme.fontcolor),
                col=1,
                row=2,
            )

        # plot the courses:
        for i_subject,subject in enumerate(courses):
            fig.add_shape(
                type="rect",
                x0=subject.x * 100,
                x1=subject.x * 100 + day_width * 100,
                y1=subject.y,
                y0=subject.y + int((subject.duration).total_seconds() / 60),
                xref="x2",
                yref="y2",
                fillcolor=mcolors.to_hex(theme.color_list(len(courses))[i_subject]),
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
                font={"color": mcolors.to_hex(theme.fontcolor)},
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
                    hoverlabel=dict(bgcolor=mcolors.to_hex(theme.color_list(len(courses))[i_subject]),
                                    font_color=mcolors.to_hex(theme.fontcolor),
                                    bordercolor=mcolors.to_hex(theme.fontcolor)),
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
    if type == "static":
        return StaticTimestable()
    elif type == "dynamic":
        return DynamicTimetable()
    raise ValueError(f"Unknown timetable type: {type}")

def choose_theme(theme) -> Theme:
    if theme == "dark":
        return DarkTheme()
    elif theme == "light":
        return LightTheme()
    elif theme == "rainbow":
        return RainbowTheme()
    elif theme == "autumn":
        return AutumnTheme()
    elif theme == "neutral":
        return NeutralTheme()
    elif theme == "nature":
        return NatureTheme()
    raise ValueError(f"Unknown theme: {theme}")


def main(type, filename, theme, figsize_timetable, user, auto_generate=True):
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
            figsize_timetable,
        )
        courses.append(course)

    timetable = choose_layout(type)
    timetable.decorator(courses, choose_theme(theme), figsize_timetable, user)


if __name__ == "__main__":
    main(
        type="static",
        filename="planner_template - chavez_pope.csv",
        theme="autumn",
        figsize_timetable=(8, 6),
        user="Marieke",
        auto_generate=True
    )