import os

import requests

from dotenv import load_dotenv

load_dotenv()

MAPS_API_KEY = os.environ.get("YANDEX_API")



def get_events_around(lat='59.971374', lng=30.324618, radius='5', categories=''):
    params = {
        'lat': lat,
        'lng': lng,
        'radius': 5,
        'categories': categories,
        'fields': '',
        'expand': '',
    }
    r = requests.get(
        f'https://spb-afisha.gate.petersburg.ru/kg/external/afisha/events',
        auth=('user', 'pass'), params=params)
    return r.json()['data']


print(get_events_around())
