import requests


def get_events_around(
    lat="59.971374", lng=30.324618, radius="5", categories="", tags="", is_free=True
):
    base_url = "https://spb-afisha.gate.petersburg.ru/kg/external/afisha/events"
    base_url = "https://kudago.com/public-api/1.4/events/"
    params = {
        "q": "event",
        "lat": lat,
        "lon": lng,
        "radius": 5,
        # 'categories': categories,
        # 'fields': 'place,tags,categories,is_free,title',
        # 'expand': 'place,images,dates',
        # 'page': 1,
        # 'count': 10,
        # 'is_free': is_free,
    }
    response = requests.get(base_url, params=params)
    response = requests.get(base_url, params=params)
    print(response.url)
    print(response.text)
    if response.status_code == 200:
        data = response.json()
        events = []
        for event in data.get("data", []):
            event_info = {
                "categories": event["categories"],
                "title": event["title"],
                "place": event["place"]["title"]
                if event.get("place")
                else "Не указано",
                "image_url": event["images"][0]["image"]
                if event.get("images")
                else "Изображение отсутствует",
                "time": event["dates"]["start_date"]
                if event.get("dates")
                else "Время не указано",
                "price": event["price"] if event.get("price") else "Цена не указана",
                "tags": event["tags"][:3] if event.get("tags") else "без тегов",
                "site": event["place"]["site_url"] if event.get("place") else None,
                "images": event["images"]["image"]
                if event.get("images")
                else "https://w.forfun.com/fetch/5d/5d572d697e41c82ac511549420ebcf44.jpeg",
            }
            events.append(event_info)
        return events
    else:
        return f"Ошибка запроса: {response.status_code}"


# print(get_events_around())
