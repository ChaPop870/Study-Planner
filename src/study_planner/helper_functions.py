from pathlib import Path
from enum import StrEnum

import pandas as pd

from src.study_planner.static_timetable import StaticTimetable
from src.study_planner.dynamic_timetable import DynamicTimetable
from src.study_planner.themes import *
from src.study_planner.timetable import WeekDay, Course, Timetable, TimetableLayout, Theme


_MAX_MINUTES_IN_A_DAY: int = 1440

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"


class LayoutType(StrEnum):
    """Distinct Layout Type Options by name."""
    STATIC = "static"
    DYNAMIC = "dynamic"


class TimetableTheme(StrEnum):
    """Distinct Timetable Theme Options by name."""
    DARK = "dark"
    LIGHT = "light"
    RAINBOW = "rainbow"
    AUTUMN = "autumn"
    NEUTRAL = "neutral"
    NATURE = "nature"


def load_course_data(file: str) -> pd.DataFrame:
    """Load course data from csv file in a pandas dataframe"""
    filepath = DATA_DIR / file
    df = pd.read_csv(filepath)
    df = df.set_index("course_name")
    return df


def choose_layout(layout_type, courses, theme, figsize_timetable, user) -> TimetableLayout:
    """Choose a layout type by name."""
    if layout_type == LayoutType.STATIC:
        return StaticTimetable(courses, theme, figsize_timetable, user)

    elif layout_type == LayoutType.DYNAMIC:
        return DynamicTimetable(courses, theme, figsize_timetable, user)

    raise ValueError(f"Unknown timetable type: {layout_type}")


def choose_theme(theme: TimetableTheme) -> Theme:
    theme_dict: dict[TimetableTheme, Theme] = {
        TimetableTheme.DARK: DarkTheme(),
        TimetableTheme.LIGHT: LightTheme(),
        TimetableTheme.RAINBOW: RainbowTheme(),
        TimetableTheme.AUTUMN: AutumnTheme(),
        TimetableTheme.NEUTRAL: NeutralTheme(),
        TimetableTheme.NATURE: NatureTheme(),
    }

    try:
        return theme_dict[theme]

    except KeyError:
        raise ValueError(f"Unknown theme: {theme}")

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
