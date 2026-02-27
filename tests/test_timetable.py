
def test_is_course():
    assert type(dynamics) == Course
    assert type(math) == Course


# Tests for Timetable Class
def test_add_course():
    timetable = Timetable()
    timetable.add_course(dynamics)
    timetable.add_course(math)

    assert len(timetable) == 2

def test_is_timetable():
    assert type(Timetable([dynamics, math])) == Timetable