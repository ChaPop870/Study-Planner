from abc import ABC, abstractmethod
from datetime import datetime, time, timedelta
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import StrEnum
import matplotlib.patheffects as pe
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


_MAX_MINUTES_IN_A_DAY = 1440

class WeekDay(StrEnum):
    """Distinct week days by name."""

    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"

    
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"


@dataclass
class Course:
    """ One university course."""
    course_name: str
    credits_: int
    week_day: WeekDay
    start_time: str
    duration_minutes: int
    room: str
    lecturer: str

@dataclass
class Timetable:
    """ Timetable containing multiple courses over the week. """
    courses: list[Course] = field(default_factory=list)

    def add_course(self, course: Course):
        self.courses.append(course)

    def to_df(self) -> pd.DataFrame:
        """Generate dataframe representation of timetable."""
        courses_dict = asdict(self)
        courses_df = pd.DataFrame(courses_dict["courses"]).set_index("course_name")
        print(courses_df)
        return courses_df

def get_user_inputs() -> Course:
    """Collect one course entry from the user"""

    course_name = input("Enter course name: ")

    while True:
        try:
            credits_ = int(input("Enter credits: "))
            break
        except ValueError:
            print("Invalid input; please enter an integer.")

    while True:
        try:
            week_day = WeekDay(input("Enter day (Monday, Tuesday, etc): "))
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
            if duration <= _MAX_MINUTES_IN_A_DAY:
                break
            else:
                print("Invalid input. Please enter a valid duration (in minutes). "
                      f"Maximum duration is one day ({_MAX_MINUTES_IN_A_DAY} minutes).")

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


def prepare_df(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare a dataframe for plotting"""
    df = data.copy()
    df["start_time"] = pd.to_datetime(df["start_time"], format="%H:%M")
    df["duration_minutes"] = pd.to_timedelta(df["duration_minutes"], unit="minutes")
    df["end_time"] = df["start_time"] + df["duration_minutes"]
    return df



class Theme(ABC):
    """Abstract base class for themes"""
    @abstractmethod
    def color_list(self, number_of_courses: int) -> list:
        """Creates a list of n colors where n is the number of courses"""
        pass


class DarkTheme(Theme):
    """Dark theme for the timetable"""
    def __init__(self):
        self.cmap = plt.get_cmap("bone")
        self.themecolor = "midnightblue"
        self.fontcolor = "white"

    def color_list(self, number_of_courses: int) -> list:
        """List of colors for the dark theme"""
        return [self.cmap(i) for i in np.linspace(0.1, 0.5, number_of_courses)]

class LightTheme(Theme):
    """Light theme for the timetable"""
    def __init__(self):
        self.cmap = plt.get_cmap("Blues")
        self.themecolor = "powderblue"
        self.fontcolor = "black"

    def color_list(self, number_of_courses: int) -> list:
        """List of colors for the light theme"""
        return [self.cmap(i) for i in np.linspace(0.2, 0.6, number_of_courses)]

class RainbowTheme(Theme):
    """Rainbow theme for the timetable"""
    def __init__(self):
        self.cmap = plt.get_cmap("rainbow")
        self.themecolor = "crimson"
        self.fontcolor = "lightgrey"

    def color_list(self, number_of_courses: int) -> list:
        """List of colors for the rainbow theme"""
        return [self.cmap(i) for i in np.linspace(0, 1, number_of_courses)]

class AutumnTheme(Theme):
    """Autumn theme for the timetable"""
    def __init__(self):
        self.cmap = plt.get_cmap("autumn")
        self.themecolor = "maroon"
        self.fontcolor = "white"

    def color_list(self, number_of_courses: int) -> list:
        """List of colors for the autumn theme"""
        return [self.cmap(i) for i in np.linspace(0, 0.85, number_of_courses)]

class NeutralTheme(Theme):
    """Neutral theme for the timetable"""
    def __init__(self):
        self.cmap = plt.get_cmap("copper")
        self.themecolor = "tan"
        self.fontcolor = "black"

    def color_list(self, number_of_courses: int) -> list:
        """List of colors for the neutral theme"""
        return [self.cmap(i) for i in np.linspace(0.25, 1, number_of_courses)]

class NatureTheme(Theme):
    """Nature theme for the timetable"""
    def __init__(self):
        self.cmap = plt.get_cmap("summer")
        self.themecolor = "lightgreen"
        self.fontcolor = "darkslategrey"

    def color_list(self, number_of_courses: int) -> list:
        """List of colors for the nature theme"""
        return [self.cmap(i) for i in np.linspace(0, 1, number_of_courses)]



class TimetableLayout(ABC):
    """Abstract base class for timetable layouts"""
    def __init__(self, courses, theme, figsize_timetable, user):
        self.courses = courses
        self.theme = theme
        self.figsize_timetable = figsize_timetable
        self.user = user

    def calc_yrange_for_plotting(self):
        """Calculate the time range on the y-axis for plotting."""
        earliest_time = datetime(year=1900, month=1, day=2, hour=0, minute=0)
        latest_time = datetime(year=1900, month=1, day=1, hour=0, minute=0)

        for subject in self.courses:
            endtime = datetime.combine(datetime.today().date(),
                                       datetime.time(subject.start_time)) + subject.duration_minutes
            y = subject.start_time.hour * 60 + subject.start_time.minute  # Any better name that self.y?

            if subject.start_time < earliest_time:
                earliest_time = subject.start_time
            if endtime > latest_time:
                latest_time = endtime

        y_bounds = [
            (earliest_time - timedelta(hours=2)).hour,
            (latest_time + timedelta(hours=2)).hour,
        ]
        y_ticks = np.arange(y_bounds[0] * 60, y_bounds[1] * 60 + 1, 60)

        return y_bounds, y_ticks

    @abstractmethod
    def display_timetable(self):
        """Plotting the timetable with courses."""
        pass

    def create_timetable_header(self, ax):
        """Create the timetable header with week days."""
        pass

    def create_timetable_layout(self, ax):
        """Creating timetable layout"""
        pass

    def display_courses(self, ax):
        """Plotting the courses into the timetable layout"""
        pass


class StaticTimestable(TimetableLayout):
    def display_timetable(self):
        """ Plotting the timetable with courses."""
        height_ratios = [1, 8]

        fig = plt.figure(figsize=self.figsize_timetable)
        fig.subplots_adjust(left=0.1, right=0.95)
        gs = fig.add_gridspec(2, 1, height_ratios=height_ratios, hspace=0.0)

        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1], sharex=ax1)

        self.display_timetable_header(ax1)
        self.create_timetable_layout(ax2)
        self.display_courses(ax2)

        return fig.show()


    def display_timetable_header(self, ax1):
        """Creating timetable header"""
        day_width = self.figsize_timetable[0] / len(WeekDay)
        text_offset = [day_width / 2, 1/2]

        for i, day in enumerate(WeekDay):
            rec = Rectangle(
                (i * day_width, 0),
                day_width,
                1,
                edgecolor=self.theme.fontcolor,
                facecolor=self.theme.themecolor,  # theme.color_list(len(courses))[0],
            )
            ax1.add_patch(rec)

            ax1.text(
                i * day_width + text_offset[0],
                text_offset[1],
                f"{day}",
                ha="center",
                va="center",
                fontsize=12,
            )

        ax1.set_xlim(0, self.figsize_timetable[0])
        ax1.set_ylim(0, 1)
        ax1.axis("off")
        title = ax1.set_title(
            f"{self.user}'s Study Timetable \n",
            fontsize=16,
            color=self.theme.themecolor,
            fontweight="bold",
        )
        title.set_path_effects(
            [pe.withStroke(linewidth=2, foreground=self.theme.fontcolor)
             ])

    def create_timetable_layout(self, ax2):
        """Creating timetable layout."""
        y_bounds, y_ticks = self.calc_yrange_for_plotting()
        ax2.set_yticks(y_ticks)
        ax2.set_ylim(y_ticks[0], y_ticks[-1])
        ax2.invert_yaxis()
        ax2.set_yticklabels([f"{int(h / 60):02d}:00" for h in y_ticks])
        ax2.set_ylabel("Hour")
        ax2.set_xticks([])

    def display_courses(self, ax2):
        """Plotting the courses into the timetable layout"""
        daylines = [i * self.figsize_timetable[0] / len(WeekDay) for i, day in enumerate(WeekDay)]
        for x in daylines:
            ax2.axvline(x, color=self.theme.fontcolor, alpha=0.5)

        for i_subject, subject in enumerate(self.courses):
            width = self.figsize_timetable[0] / len(WeekDay)  # One day wide
            height = subject.duration_minutes.total_seconds() / 60  # Duration in minutes
            day_to_x = {
                day: i * self.figsize_timetable[0] / len(WeekDay) for i, day in enumerate(WeekDay)
            }
            x = day_to_x[subject.week_day]
            y = subject.start_time.hour * 60 + subject.start_time.minute  # Any better name that self.y?

            period = Rectangle(
                xy=(x, y),
                width=width,
                height=height,
                facecolor=self.theme.color_list(len(self.courses))[i_subject],
                edgecolor=self.theme.fontcolor,
                label=subject.course_name,
            )
            ax2.add_patch(period)
            ax2.text(
                x + width * 0.3, y + height * 0.7, subject.course_name[0:6]
            )

        ax2.legend()


class DynamicTimetable(TimetableLayout):
    """Dynamic Timetable Layout"""
    def display_timetable(self):
        """Plotting the timetable with courses."""
        height_ratios = [1, 8]

        fig = make_subplots(
            2, 1, shared_xaxes=True, vertical_spacing=0, row_heights=height_ratios
        )
        fig.update_layout(title=f"{self.user}'s Study Timetable")
        fig.update_layout(title_font_color=mcolors.to_hex(self.theme.themecolor),
                          title_font_shadow="auto")
        fig.update_xaxes(visible=False, col=1, row=2)
        fig.update_xaxes(range=[0, self.figsize_timetable[0] * 100], row=2, col=1)

        self.create_timetable_header(fig)
        self.create_timetable_layout(fig)
        self.display_courses(fig)

        return fig.show()

    def create_timetable_header(self, fig):
        """Creating timetable header with week days."""

        day_width = self.figsize_timetable[0] / len(WeekDay)
        text_offset = [day_width / 2, 1 / 2]
        # create the days as a header in subplot 1:
        for i, day in enumerate(WeekDay):
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
                fillcolor=mcolors.to_hex(self.theme.themecolor)
            )

            fig.add_annotation(
                x=(i * day_width + text_offset[0]) * 100,
                y=text_offset[1],
                text=f"{day}",
                showarrow=False,
                col=1,
                row=1,
                font={"color": mcolors.to_hex(self.theme.fontcolor)},
            )
        fig.update_yaxes(range=[0, 1], visible=False, col=1, row=1)

    def create_timetable_layout(self, fig):
        """Creating timetable layout"""

        y_bounds, y_ticks = self.calc_yrange_for_plotting()
        daylines = [
            i * self.figsize_timetable[0] * 100 / len(WeekDay)
            for i, _ in enumerate(WeekDay)
        ]
        for x in daylines:
            fig.add_shape(
                type="line",
                x0=x,
                x1=x,
                y0=y_ticks[0],
                y1=y_ticks[-1],
                xref="x2",
                yref="y2",
                opacity=0.5,
                fillcolor=mcolors.to_hex(self.theme.fontcolor),
                col=1,
                row=2,
            )
        fig.update_yaxes(
            title_text="Hour",
            range=[max(y_ticks), min(y_ticks)],
            tickvals=y_ticks,
            ticktext=[f"{int(h / 60):02d}:00" for h in y_ticks],
            row=2,
            col=1,
        )


    def display_courses(self, fig):
        """Plotting the courses into the timetable layout."""

        day_width = self.figsize_timetable[0] / len(WeekDay)

        for i_subject, subject in enumerate(self.courses):
            day_to_x = {
                day: i * self.figsize_timetable[0] / len(WeekDay) for i, day in enumerate(WeekDay)
            }
            x = day_to_x[subject.week_day]
            endtime = datetime.combine(datetime.today().date(),
                                       datetime.time(subject.start_time)) + subject.duration_minutes
            y = subject.start_time.hour * 60 + subject.start_time.minute  # Any better name that self.y?

            fig.add_shape(
                type="rect",
                x0=x * 100,
                x1=x * 100 + day_width * 100,
                y1=y,
                y0=y + int(subject.duration_minutes.total_seconds() / 60),
                xref="x2",
                yref="y2",
                fillcolor=mcolors.to_hex(self.theme.color_list(len(self.courses))[i_subject]),
                col=1,
                row=2,
            )
            fig.add_annotation(
                x=(x * 100 + 0.5 * day_width * 100),
                y=y + 0.5 * int(subject.duration_minutes.total_seconds() / 60),
                text=f"{subject.course_name[:6]}",
                showarrow=False,
                col=1,
                row=2,
                font={"color": mcolors.to_hex(self.theme.fontcolor)},
            )
            # add hover info:
            fig.add_trace(
                go.Scatter(
                    x=[x * 100 + 0.5 * day_width * 100],
                    y=[y + 0.5 * int(subject.duration_minutes.total_seconds() / 60)],
                    marker=dict(
                        size=int(subject.duration_minutes.total_seconds() / 60), opacity=0
                    ),
                    mode="markers",
                    hovertemplate=f"<b>{subject.course_name}</b> "
                                  f"<br> {subject.lecturer}"
                                  f"<br> {subject.room}"
                                  f"<br> {subject.start_time.time()}"
                                  f"<br> {endtime.time()}"
                                  f"<extra></extra>",
                    hoverlabel=dict(bgcolor=mcolors.to_hex(self.theme.color_list(len(self.courses))[i_subject]),
                                    font_color=mcolors.to_hex(self.theme.fontcolor),
                                    bordercolor=mcolors.to_hex(self.theme.fontcolor)),
                    showlegend=False,
                ),
                row=2,
                col=1,
            )

class LayoutType(StrEnum):
    """Distinct Layout Type Options by name."""
    STATIC = "static"
    DYNAMIC = "dynamic"

def choose_layout(layout_type, courses, theme, figsize_timetable, user) -> TimetableLayout:
    """Choose a layout type by name."""
    if layout_type == LayoutType.STATIC:
        return StaticTimestable(courses, theme, figsize_timetable, user)
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

def choose_theme(theme) -> Theme:
    """Choose a theme by name."""
    if theme == TimetableTheme.DARK:
        return DarkTheme()
    elif theme == TimetableTheme.LIGHT:
        return LightTheme()
    elif theme == TimetableTheme.RAINBOW:
        return RainbowTheme()
    elif theme == TimetableTheme.AUTUMN:
        return AutumnTheme()
    elif theme == TimetableTheme.NEUTRAL:
        return NeutralTheme()
    elif theme == TimetableTheme.NATURE:
        return NatureTheme()
    raise ValueError(f"Unknown theme: {theme}")


def main(layout_type, filename, theme, figsize_timetable, user, auto_generate=True):
    if not auto_generate:
        all_users_courses = Timetable()
        while True:
            users_course = get_user_inputs()
            all_users_courses.add_course(users_course)

            choice = input("\nAdd another course? (y/n): ")
            if choice != "y":
                break

        df = all_users_courses.to_df()
        df = prepare_df(df)
    else:
        df = load_course_data(filename)
        df = prepare_df(df)

    courses = []

    for i, (subject, row) in enumerate(df.iterrows()):
        course = Course(
            subject,
            row["_credits"],
            row["week_day"],
            row["start_time"],
            row["duration_minutes"],
            row["room"],
            row["lecturer"]
        )
        courses.append(course)

    timetable = choose_layout(layout_type, courses, choose_theme(theme), figsize_timetable, user)
    timetable.display_timetable()



if __name__ == "__main__":
    main(
        layout_type="static",
        filename="planner_template - chavez_pope.csv",
        theme="autumn",
        figsize_timetable=(8, 6),
        user="Marieke",
        auto_generate=True
    )