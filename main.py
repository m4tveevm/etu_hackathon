import requests

lat, lng = "59.971374", "30.324618"
params = {
    'lat': lat,
    'lng': lng,
    'radius': 5,
    'categories': '',
    'fields': '',
    'expand': '',
}
r = requests.get(
    f'https://spb-afisha.gate.petersburg.ru/kg/external/afisha/events',
    auth=('user', 'pass'), params=params)
print(r.text)
