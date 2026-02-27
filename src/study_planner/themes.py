from src.study_planner.timetable import Theme
import numpy as np
import matplotlib.pyplot as plt

from src.study_planner.timetable import Theme


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

