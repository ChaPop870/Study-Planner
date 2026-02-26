from src.study_planner.timetable import TimetableLayout, WeekDay
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.study_planner.timetable import TimetableLayout, WeekDay


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