import requests

def get_updates(token):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url)
    updates = response.json()
    return updates

print(get_updates('YOUR_BOT_TOKEN'))
