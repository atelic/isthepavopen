import os
import json
from datetime import datetime, time
from flask import Flask, render_template

from settings import debug
app = Flask(__name__)


@app.route('/')
def index():
    i_am_bad_at_names = {}

    with open(os.path.join(os.getcwd(), 'hours.json')) as fp:
        locations = json.loads(fp.read())
        for location, info in locations.items():
            OPEN = time(info['open'][0], info['open'][1])
            M_TH_CLOSE = time(info['m_th_close'][0], info['m_th_close'][1])
            F_CLOSE = time(info['f_close'][0], info['f_close'][1])
            ME_CLOSE = time(info['me_close'][0], info['me_close'][1])

            time_now = datetime.now().time()
            day = datetime.today().weekday()
            closing = False
            if day in range(0, 4):
                closing = M_TH_CLOSE
            if day == 4:
                closing = F_CLOSE

            hour_open = is_open(time_now, day, [OPEN, M_TH_CLOSE, F_CLOSE])
            meal = is_meal(time_now, day, [OPEN, M_TH_CLOSE, F_CLOSE, ME_CLOSE])
            print([OPEN, M_TH_CLOSE, F_CLOSE])
            i_am_bad_at_names[location] = {
                'open': hour_open,
                'meal': meal,
                'close': closing
            }

            print(i_am_bad_at_names)

        return render_template('index.html', location_dict=i_am_bad_at_names)


def is_open(time_now, day, possible_hours):
    """ Hours are stored in ./hours.json and can be found at
    http://www.virginia.edu/newcomb/building-hours/
    There is currently no way to programmatically find these
    """
    hours = {
        'open': possible_hours[0],
        'close': time(00, 00)
    }
    if day in range(5):  # Monday - Thursday
        hours['close'] = possible_hours[1]

    if day == 5:  # Friday hours
        hours['close'] = possible_hours[2]

    ret = False
    if time_now >= hours['open'] and time_now <= hours['close']:
        ret = True

    return ret


def is_meal(time_now, day, possible_hours):
    """ Monday - Thursday 4:00pm - 8:00pm"""
    hours = {
        'open': possible_hours[0],
        'close': possible_hours[3]
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
