# Review remarks

## General remarks
- the majority of remarks are in code
- The flow is pretty reasonable to me
  - only question for me is, why you the "in-between-dict" instead of directly using your `Course` class
- it is good practise to break up the code in modules. I would suggest:
  - timetable.py: just the `Timetable(ABC)` and `Course` definition
  - static_timetable.py: just `StaticTimetable(Timetable)` definition
  - dynamic_timetable.py: just `DynamicTimetable(Timetable)` definition
  - main.py: your execution code + settings, constants, helper functions 
- quite a lot of dependencies are in requirements.txt? Do you need all of them explicitly?
  - usually just the once directly in use are defined and not all subdependencies.This helps others to identify which dependencies are important
- remove "development code" (test.py, testing.ipynb, *png's (png))
  - for images, which you want to show in your README.md, put them in a dedicated "images" folder to keep the root folder of the project clean
- please check following (old) slides to ensure you stay in code and projecture structure style

## Grading criteria remarks
- Readme is generally speaking well-structured, but it seems, that is not aligned with the project state.
  - please ensure that an installation and usage guide is in there as well (see installation guide here: https://github.com/Practical-Python-Development/minesweeper)
- I mentioned separation of modules before
- please run mypy and ruff to check if your code adheres to coding style
- no tests yet (be aware of the project structure. The current `test.py` would not be in the correct spot)
- I highlighted where I want to see docstrings. basically in every method, function or class
- comments should exist as little as possible (check coding style)
  - therefore, please remove all my comments before we will grate the project
- The One pattern I saw is nice already, but it is not stated in the README.md
  - in the meetings note there is ann other pattern mentioned... Do you want to implement it? please align :)
- 