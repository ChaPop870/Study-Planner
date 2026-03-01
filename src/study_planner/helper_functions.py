from pathlib import Path
from enum import StrEnum

import pandas as pd

from src.study_planner.static_timetable import StaticTimetable
from src.study_planner.dynamic_timetable import DynamicTimetable
from src.study_planner.themes import *
from src.study_planner.timetable import Theme, TimetableLayout


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