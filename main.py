import os

import requests

from dotenv import load_dotenv

load_dotenv()

MAPS_API_KEY = os.environ.get("YANDEX_API")


def get_events_around_new(lat='59.971374', lng=30.324618, radius='5', categories='', tags='', actual_since='',
                          is_free=True):
    base_url = "https://spb-afisha.gate.petersburg.ru/kg/external/afisha/events"
    params = {
        'lat': lat,
        'lng': lng,
        'radius': 5,
        'categories': '',
        'fields': 'place,tags,categories,is_free,',
        'expand': 'place,images,dates',
        'page': 1,
        'count': 10,
        'tags': tags,
        'actual_since': actual_since,
        'is_free': is_free,
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        events = []
        for event in data.get('data', []):
            event_info = {
                'title': event['title'],
                'place': event['place']['title'] if event.get('place') else "Не указано",
                'image_url': event['images'][0]['image'] if event.get(
                    'images') else "Изображение отсутствует",
                'dates': event['dates'][0]['start'] if event.get('dates') else "Время не указано"
            }
            events.append(event_info)
        return events
    else:
        return f"Ошибка запроса: {response.status_code}"


print(get_events_around_new())
