from datetime import time
from index import is_open, is_meal


def test_is_open():
    time_now = time(22, 30)
    day = 1
    h_open = time(8, 30)
    m_th_close = time(23, 00)
    f_close = time(16, 00)
    possible_hours = [h_open, m_th_close, f_close]

    assert(is_open(time_now, day, possible_hours) == True)

    day = 6
    assert(is_open(time_now, day, possible_hours) == False)

    time_now = time(23, 01)
    assert(is_open(time_now, day, possible_hours) == False)


def test_is_meal():
    time_now = time(22, 30)
    day = 1
    h_open = time(8, 30)
    m_th_close = time(23, 00)
    f_close = time(16, 00)
    me_close = time(16, 00)
    possible_hours = [h_open, m_th_close, f_close, me_close]

    assert(is_meal(time_now, day, possible_hours) == False)

    time_now = time(13, 00)
    assert(is_meal(time_now, day, possible_hours) == True)

    day = 5
    assert(is_meal(time_now, day, possible_hours) == False)
