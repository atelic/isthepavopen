import os
import json
from pprint import pprint as pp

with open(
        os.path.join(
            os.getcwd(), 'hours.json'
        )
) as fp:
    locations = json.loads(fp.read())
    for location, info in locations.items():
        print('{loc} opens at {open}'.format(loc=location, open=info['open']))
        pp(location)
        pp(info)
