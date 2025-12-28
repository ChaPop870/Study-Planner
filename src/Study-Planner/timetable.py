# Imports
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import matplotlib.colors as mcolors


# Load File
BASE_DIR: Path = Path(__file__).resolve().parents[2]
DATA_DIR: Path = BASE_DIR / "data"
WEEK_DAYS: list[str] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
#HOURS = np.arange(0, 24)

file = DATA_DIR / "planner_template - chavez_pope.csv"

#user = "Chavez"

df = pd.read_csv(file).set_index("course_name")

# Prepare the data
df["start_time"] = pd.to_datetime(df["start_time"], format="%H:%M")
df["duration"] = pd.to_timedelta(df["duration"], unit="minutes")
df["end_time"] = df["start_time"] + df["duration"]


class Course:
    def __init__(self, name, credits, day, starttime, duration, room, lecturer, color, figsize_timetable):
        self.name = name
        self.credits = credits
        self.day = day
        self.starttime = starttime
        self.duration = duration
        self.room = room
        self.lecturer = lecturer
        self.color = color

        self.endtime = starttime + duration
        self.y = starttime.hour * 60 + starttime.minute
        daylines = [i * figsize_timetable[0] / len(WEEK_DAYS) for i, day in enumerate(WEEK_DAYS)]
        day_to_x = {day: daylines[i] for i, day in enumerate(WEEK_DAYS)}
        self.x = day_to_x[day]



class Display():
    def __init__(self, courses):
        self.courses = courses

    def static(self, themecolor, figsize_timetable, user):
        # prepare dynamic y-axis
        earliest_time = datetime(year = 1900, month = 1, day = 2, hour = 0, minute = 0)
        latest_time = datetime(year = 1900, month = 1, day = 1, hour = 0, minute = 0)

        for subject in self.courses:
            if subject.starttime < earliest_time:
                earliest_time = subject.starttime
            if subject.endtime > latest_time:
                latest_time = subject.endtime

        y_bounds = [(earliest_time - timedelta(hours = 2)).hour, (latest_time + timedelta(hours = 2)).hour]
        yticks = np.arange(y_bounds[0]*60, y_bounds[1]*60 +1, 60)

        height_ratios = [1,8]
        day_width = figsize_timetable[0] / len(WEEK_DAYS)
        text_offset = [day_width /2, height_ratios[0] / 2]

        fig = plt.figure(figsize = figsize_timetable)
        fig.subplots_adjust(left=0.1, right=0.95)
        gs = fig.add_gridspec(2, 1, height_ratios = height_ratios, hspace=0.0)

        # ax1 for days
        ax1 = fig.add_subplot(gs[0])
        for i in range(len(WEEK_DAYS)):
            rec = Rectangle( (i * day_width, 0), day_width, 1, edgecolor="black", facecolor=themecolor)
            ax1.add_patch(rec)

            ax1.text(i * day_width + text_offset[0], text_offset[1], f"{WEEK_DAYS[i]}", ha="center", va="center", fontsize=12)

        ax1.set_xlim(0, figsize_timetable[0])
        ax1.set_ylim(0,1)
        ax1.axis("off")
        ax1.set_title(f"{user}'s Study Timetable \n", fontsize = 16, color = themecolor, fontweight = "bold")

        # ax2 for actual timetable
        ax2 = fig.add_subplot(gs[1], sharex = ax1)
        ax2.set_yticks(yticks)
        ax2.set_ylim(yticks[0], yticks[-1])
        ax2.invert_yaxis()
        ax2.set_yticklabels([f"{int(h/60):02d}:00" for h in yticks])
        ax2.set_ylabel("Hour")
        ax2.set_xticks([])
        daylines = [i * figsize_timetable[0] / len(WEEK_DAYS) for i,day in enumerate(WEEK_DAYS)]
        for x in daylines:
            ax2.axvline(x, color = "black", alpha = 0.5)

        # plotting the courses:
        for subject in self.courses:
            width = figsize_timetable[0] / len(WEEK_DAYS)  # One day wide
            height = (subject.duration).total_seconds() / 60  # Duration in minutes

            period = Rectangle(
                xy=(subject.x, subject.y),
                width=width,
                height=height,
                facecolor=subject.color,
                edgecolor="black",
                label = subject.name
            )
            ax2.add_patch(period)
            ax2.text(subject.x + width*0.3, subject.y + height*0.7, subject.name[0:6])

        ax2.legend()

    def show(self):
        plt.show()


courses = []
colors = list(mcolors.CSS4_COLORS)
figsize_timetable = [8,6]
for i, (subject, row) in enumerate(df.iterrows()):
    course = Course(subject, row["credits"], row["day"], row["start_time"], row["duration"], row["room"], row["lecturer"], colors[i+i*7], figsize_timetable)
    courses.append(course)

plot = Display(courses)
plot.static("skyblue", figsize_timetable, "Marieke")
plot.show()


