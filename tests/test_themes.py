import pytest

from src.study_planner.themes import (
    DarkTheme,
    LightTheme,
    RainbowTheme,
    AutumnTheme,
    NeutralTheme,
    NatureTheme,
)
from src.study_planner.timetable import Theme


# Helper
THEME_CLASSES = [
    DarkTheme,
    LightTheme,
    RainbowTheme,
    AutumnTheme,
    NeutralTheme,
    NatureTheme,
]


# Basic Structural Tests
@pytest.mark.parametrize("ThemeClass", THEME_CLASSES)
def test_theme_is_subclass(ThemeClass):
    theme = ThemeClass()
    assert isinstance(theme, Theme)


@pytest.mark.parametrize("ThemeClass", THEME_CLASSES)
def test_theme_has_required_attributes(ThemeClass):
    theme = ThemeClass()

    assert hasattr(theme, "themecolor")
    assert hasattr(theme, "fontcolor")
    assert isinstance(theme.themecolor, str)
    assert isinstance(theme.fontcolor, str)


# color_list Behavior
@pytest.mark.parametrize("ThemeClass", THEME_CLASSES)
def test_color_list_length(ThemeClass):
    theme = ThemeClass()

    colors = theme.color_list(5)

    assert isinstance(colors, list)
    assert len(colors) == 5


@pytest.mark.parametrize("ThemeClass", THEME_CLASSES)
def test_color_list_zero(ThemeClass):
    theme = ThemeClass()

    colors = theme.color_list(0)

    assert colors == []


@pytest.mark.parametrize("ThemeClass", THEME_CLASSES)
def test_color_list_returns_rgba(ThemeClass):
    theme = ThemeClass()

    colors = theme.color_list(3)

    for color in colors:
        assert isinstance(color, tuple)
        assert len(color) == 4  # RGBA
        assert all(0 <= c <= 1 for c in color)