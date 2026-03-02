import pytest

from src.study_planner.timetable import WeekDay, Course, Timetable, TimetableLayout
from src.study_planner.cli_generation import available_timetable_list ,get_user_inputs


def test_get_user_inputs_valid(monkeypatch):
    inputs = iter([
        "Math",
        6,
        WeekDay.MONDAY,
        "10:00",
        90,
        "A1",
        "Dr. Euler"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert get_user_inputs() == Course("Math", 6, WeekDay.MONDAY, "10:00", 90, "A1", "Dr. Euler")


def test_invalid_credits(monkeypatch):
    inputs = iter([
        "Math",
        -3, "ten", 6,
        WeekDay.MONDAY,
        "10:00",
        90,
        "A1",
        "Dr. Euler"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_user_inputs()

    assert result.credits == 6


def test_invalid_weekday(monkeypatch):
    inputs = iter([
        "Math",
        6,
        "Tomorrow", "sunday",
        "10:00",
        90,
        "A1",
        "Dr. Euler"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_user_inputs()

    assert result.week_day == WeekDay.SUNDAY


def test_invalid_start_time(monkeypatch):
    inputs = iter([
        "Math",
        6,
        "Tomorrow", "sunday",
        "soon", "24:53", "10:00",
        90,
        "A1",
        "Dr. Euler"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_user_inputs()

    assert result.start_time == "10:00"


def test_invalid_duration(monkeypatch):
    inputs = iter([
        "Math",
        6,
        WeekDay.MONDAY,
        "10:00",
        15_000, 20_000, -4, "Cake", 90,
        "A1",
        "Dr. Euler"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_user_inputs()

    assert result.duration_minutes == 90


def test_filter_csv_files(tmp_path):

    (tmp_path / "file1.csv").touch()
    (tmp_path / "file2.csv").touch()
    (tmp_path / "notes.txt").touch()
    (tmp_path / "to-do-list.pdf").touch()

    result = available_timetable_list(tmp_path)

    assert sorted(result) == ["file1.csv", "file2.csv"]