import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import datetime as dt


BASE_DIR = pathlib.Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

file = DATA_DIR / "planner_template - chavez_pope.csv"

df = pd.read_csv(file)

# define times and days
start = dt.datetime(2025,1,1, 8,0)
datetime_vec = [start + i * dt.timedelta(minutes=15) for i in range(0,49)]  # quarter hour steps
time = [t.time() for t in datetime_vec]
print(time)
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

