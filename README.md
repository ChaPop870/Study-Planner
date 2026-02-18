# Study-Planner

## Project Description
This project aims to create study planner for students. It will allow students to plan their schedules and later view it in an intuitive graphical user interface.  There are also plans to scrape websites with classes to automatically populate the planner using web scraping. Also, we can create a room timetable as well for the Geomatikum.

## Project Scope and Goals
1. Parse a user-created csv file and use the data to create a structured timetable.
2. Create the schedule from user-generated input.
3. Scrape UHH website to create the timetable automatically.
4. Create a timetable for specific classrooms to determine their availability for students who wish to use them for studying.

## 1. Using the CSV format
In this case, the user will populate a csv file with the information for their courses. This csv file will then be used to create a timetable.

## 2. Using a link from STiNE
In this case, the user will provide a link to the page which contains their courses. The get to this page, students must log into STiNE, navigate to Studying and click on Courses. This hyperlink will then be the input for the study planner. A screenshot of this page is provided below.
![img.png](img.png)
In the future, we can likely automate the fetching of this link.

### CSV Structure
Each row in the CSV file represents one scheduled course session. The required columns

| Column              | Description                                  |
| ------------------- |----------------------------------------------|
| **course_name**     | The name/title of the course                 |
| **credits**         | Number of credit hours                       |
| **day**             | Start day (Sunday, Monday, ... , Saturday)   |
| **start_time**      | Start time in 24 hour format (e.g., `18:00`) |
| **duration**        | Duration (TimeDelta)                         |
| **room**            | Room or lecture hall                         |
| **lecturer**        | Instructor of the course                     |

### Timetable Display

We plan to support:

1. Static Timetable (Matplotlib)
   - Clean weekly timetable image
   - Minimal details for clarity
   - Good for exporting or printing

2. Interactive Timetable (Plotly)
   - Hover tooltips with additional course information
   - Potential zooming or filtering (e.g., by day, room, or teacher)

### Ideas
- [ ] Create a timetable class which can be used to retrieve specific information and do specific things.
- [ ] Add a table to enclose the days on the timetable for aesthetics.
- [ ] Add another column in the CSV template called "label" which will be used for the labels on the rectangles.
- [ ] Allow a user to manually enter information into the planner.  They should be able to add, remove, and edit entries.
- [ ] Will need to handle rectangles overlapping gracefully.

# 26-01-26 Meeting
## Adapter Design Pattern
## Factory Method
## Builder method
Might be useful to say to use this input with that output.
- Input adapters can return a list of courses
- Ensure typing in main functions and other functions. Use MyPy to check code for typing options. It helps with handling of types. https://github.com/python/mypy

# 13-02-26
- Start time + Duration should be less than a full day. OR... if longer, print until the end of the day and no longer beyond with an associated warning.
- In the creation of the plot, we have a 2 hour buffer. We should account for times beginning just after midnight and before midnight. If start time is less than buffer time, set start time to midnight, or end time to midnight. (Or rather, have the axis roll back into the previous day.)
- Can we implement a decorator pattern? Is the adapter decorator pattern possible? Factory pattern.
- Implement themes (about 5): Dark Mode, Light mode (Modern look) Lightwork, Warm Colors (Caribbean color theme), Cool colors, Nature (Green).
- Interactivity with the interface. We can possibly add another parameter to main (bool) which takes the user through a routine OR generates a timetable immediately from the set parameters.
- Testing.