# Imports
import datetime as dt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

from soupsieve.css_match import DAYS_IN_WEEK

# Load File
BASE_DIR: Path = Path(__file__).resolve().parents[2]
DATA_DIR: Path = BASE_DIR / "data"
WEEK_DAYS: list[str] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
HOURS = np.arange(0, 24)

file = DATA_DIR / "planner_template - chavez_pope.csv"

user = "Chavez"

df = pd.read_csv(file).set_index("course_name")

# Prepare the data
df["start_time"] = pd.to_datetime(df["start_time"], format="%H:%M")
df["duration"] = pd.to_timedelta(df["duration"], unit="minutes")
df["end_time"] = df["start_time"] + df["duration"]

# Period to create timetable display
# period = Rectangle(
#     xy=(df["day"], df["start_time"]),
#     width=df["day"],
#     height=df["duration"]
# )


# Plot
fig, ax = plt.subplots(figsize=(8, 6))
# for subject, row in df.iterrows():
#     x = row["day"]
#     y = row["start_time"]
#     width = row["day"]
#     height = row["duration"]
#
#     period = Rectangle(
#         xy=(x, y),
#         width=width,
#         height=height
#     )
#     ax.add_patch(period)
ax.set_title(f"{user}'s Study Timetable")
ax.xaxis.tick_top()
ax.set_xticks(ticks=np.arange(0, len(WEEK_DAYS)), labels=WEEK_DAYS)
ax.set_xlim(- 0.5, len(WEEK_DAYS) - 0.5)
ax.set_xticklabels(WEEK_DAYS)
ax.set_xlabel("Week Day")
ax.invert_yaxis()
ax.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.yaxis.set_major_locator(mdates.HourLocator(byhour=np.arange(1, 24, 2)))
ax.yaxis.set_minor_locator(mdates.MinuteLocator(interval=30))
ax.set_ylabel("Hour")
# ax.set_yticks(HOURS)

plt.show()

# define times and days
# start = dt.datetime(2025,1,1, 8,0)
# datetime_vec = [start + i * dt.timedelta(minutes=15) for i in range(0,49)]  # quarter hour steps
# time = [t.time() for t in datetime_vec]
# print(time)
# days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# print(df)

