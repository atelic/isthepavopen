from datetime import datetime, time
from flask import Flask, render_template

from settings import debug
app = Flask(__name__)



OPEN = time(10, 30)
M_TH_CLOSE = time(20, 00)
F_CLOSE = time(18, 30)
ME_CLOSE = time(16, 00)


@app.route('/')
def index():
    time_now = datetime.now().time()
    day = datetime.today().weekday()
    closing = False
    if day in range(0, 4):
        closing = M_TH_CLOSE
    if day == 4:
        closing = F_CLOSE

    open = is_open(time_now, day)
    meal = is_meal(time_now, day)

    return render_template('index.html', open=open, meal=meal, close=closing)


def is_open(time_now, day):
    """ As of 09-12-2015, the hours for Pavilion XI (The Pav) are:
    Monday - Thursday  Friday            Saturday    Sunday
    10:30am - 8:00pm   10:30am - 6:00pm  Closed      Closed
    Per: http://www.virginia.edu/newcomb/building-hours/
    There is currently no way to programmatically find these
    """
    hours = {
        'open': OPEN,
        'close': time(00, 00)
    }
    if day in range(5):  # Monday - Thursday
        hours['close'] = M_TH_CLOSE

    if day == 5:  # Friday hours
        hours['close'] = F_CLOSE

    ret = False
    if time_now >= hours['open'] and time_now <= hours['close']:
        ret = True

    return ret


def is_meal(time_now, day):
    """ Monday - Thursday 4:00pm - 8:00pm"""
    hours = {
        'open': ME_CLOSE,
        'close': M_TH_CLOSE
    }
    meal = False
    weekday = day not in range(4, 7)

    if time_now >= hours['open'] and time_now <= hours['close'] and weekday:
        meal = True

    return meal

@app.route('/hours')
def hours():
    return render_template('hours.html')

if __name__ == '__main__':
    app.run(debug=debug)
