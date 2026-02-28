from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import matplotlib.patheffects as pe

from src.study_planner.timetable import TimetableLayout, WeekDay
from src.study_planner.timetable import minutes_since_midnight
from src.study_planner.themes import *


class StaticTimestable(TimetableLayout):
    def display_timetable(self) -> Figure:
        """Plotting the timetable with courses."""
        height_ratios = [1, 8]

        fig = plt.figure(figsize=self.figsize_timetable)
        fig.subplots_adjust(left=0.1, right=0.95)
        gs = fig.add_gridspec(2, 1, height_ratios=height_ratios, hspace=0.0)

        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1], sharex=ax1)

        self.display_timetable_header(ax1)
        self.create_timetable_layout(ax2)
        self.display_courses(ax2)

        return fig


    def display_timetable_header(self, ax1: Axes) -> None:
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
        title.set_path_effects([
            pe.withStroke(linewidth=2, foreground=self.theme.fontcolor)
        ])

    def create_timetable_layout(self, ax2: Axes) -> None:
        """Creating timetable layout."""
        y_ticks = self.calc_yrange_for_plotting()
        ax2.set_yticks(y_ticks)
        ax2.set_ylim(y_ticks[0], y_ticks[-1])
        ax2.invert_yaxis()
        ax2.set_yticklabels([f"{int(h / 60 % 24):02d}:00" for h in y_ticks])
        ax2.set_ylabel("Hour")
        ax2.set_xticks([])

    def display_courses(self, ax2: Axes) -> None:
        """Plotting the courses into the timetable layout"""
        day_lines = [i * self.figsize_timetable[0] / len(WeekDay) for i, day in enumerate(WeekDay)]
        for x in day_lines:
            ax2.axvline(x, color=self.theme.fontcolor, alpha=0.5)

        for i_subject, subject in enumerate(self.courses):
            width = self.figsize_timetable[0] / len(WeekDay)  # One day wide
            height = subject.duration_minutes
            day_to_x = {
                day: i * self.figsize_timetable[0] / len(WeekDay) for i, day in enumerate(WeekDay)
            }
            x = day_to_x[subject.week_day]
            y = minutes_since_midnight(subject.start_time)

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