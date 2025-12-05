# Imports
import datetime as dt
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

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title(f"{user}'s Study Timetable")
ax.xaxis.tick_top()
ax.set_xlabel("Week Day")
ax.set_xticks(ticks=np.arange(0, len(WEEK_DAYS)), labels=WEEK_DAYS)
ax.invert_yaxis()
ax.set_ylabel("Hour")
ax.set_yticks(HOURS)

plt.show()

# define times and days
# start = dt.datetime(2025,1,1, 8,0)
# datetime_vec = [start + i * dt.timedelta(minutes=15) for i in range(0,49)]  # quarter hour steps
# time = [t.time() for t in datetime_vec]
# print(time)
# days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# print(df)

