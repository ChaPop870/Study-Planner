# Study-Planner

In this project, a study planner for students is created. Different options for data input and the displaying can be chosen.

## Installation
```
git clone https://github.com/ChaPop870/Study-Planner.git
cd Study-Planner
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
The user can choose between the creation of a timetable based on an existing csv-file 
or based on terminal inputs. In the case of using an existing csv file, the file must
be stored in the data folder. 
```
cp path/to/csv-file/name.csv path/to/projects/Study-Planner/data/
```
A planner template can be found in the data folder. See [CSV Structure](README.md#csv-structure) 
for more information to the file structure.

Afterwards, the main script can be executed.
```
cd path/to/projects/Study-Planner
python src/main.py
```
When running the script the user is guided through the creation by prompts in the terminal.

The user is able to choose between the creation based on an existing csv file or 
based on inputs in the terminal.
Two displaying options are offered: a static version and a dynamic version. 
See [displaying options](README.md#timetable-display) for more details.
Moreover, the user can choose between 5 different 
color options for the timetable. 

### CSV Structure
Each row in the CSV file represents one scheduled course session. The required columns

| Column               | Description                                  |
|----------------------|----------------------------------------------|
| **course_name**      | The name/title of the course                 |
| **credits_**         | Number of credit hours                       |
| **week_day**         | Start day (Sunday, Monday, ... , Saturday)   |
| **start_time**       | Start time in 24 hour format (e.g., `18:00`) |
| **duration_minutes** | Duration (TimeDelta)                         |
| **room**             | Room or lecture hall                         |
| **lecturer**         | Instructor of the course                     |

### Timetable Display

We support:

1. Static Timetable (Matplotlib)
   - Clean weekly timetable image
   - Minimal details for clarity
   - Good for exporting or printing

2. Interactive Timetable (Plotly)
   - Hover tooltips with additional course information

## Further Project Goals
1. Will need to handle rectangles overlapping gracefully.
2. Scrape UHH website to create the timetable automatically.
3. Create a timetable for specific classrooms to determine their availability for students who wish to use them for studying.


### 2. Using a link from STiNE
In this case, the user will provide a link to the page which contains their courses. The get to this page, students must log into STiNE, navigate to Studying and click on Courses. This hyperlink will then be the input for the study planner. A screenshot of this page is provided below.
![images/img.png](images/img.png)
In the future, we can likely automate the fetching of this link.

## Meeting Notes
### 26-01-26 Meeting
Might be useful to say to use this input with that output.
- Input adapters can return a list of courses
- Ensure typing in main functions and other functions. Use MyPy to check code for typing options. It helps with handling of types. https://github.com/python/mypy

### 13-02-26
- Start time + Duration should be less than a full day. OR... if longer, print until the end of the day and no longer beyond with an associated warning.
- In the creation of the plot, we have a 2 hour buffer. We should account for times beginning just after midnight and before midnight. If start time is less than buffer time, set start time to midnight, or end time to midnight. (Or rather, have the axis roll back into the previous day.)
- Can we implement a decorator pattern? Is the adapter decorator pattern possible? Factory pattern.
- Implement themes (about 5): Dark Mode, Light mode (Modern look) Lightwork, Warm Colors (Caribbean color theme), Cool colors, Nature (Green).
- Interactivity with the interface. We can possibly add another parameter to main (bool) which takes the user through a routine OR generates a timetable immediately from the set parameters.
- Testing.

- Adapter Design Pattern
- Factory Method
- Builder method