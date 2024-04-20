import requests
import json
import time
from bs4 import BeautifulSoup

import os
from dotenv import load_dotenv

load_dotenv()


class ETU_data():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.session = requests.Session()

    def number_of_unread_messages(self):
        try:
            response = self.session.get('https://lk.etu.ru/api/profile/menu_counters', headers=self.headers)
            response_json = json.loads(response.text)
            messages_to_count = response_json['messages_to']['count']
            if messages_to_count > 0:
                return str(messages_to_count)
            else:
                return None
        except Exception as e:
            print(f"Error retrieving notification: {e}")
            return 0  # Return 0 if an error occurs

    def get_timetable_session(self):
        url = "https://digital.etu.ru/attendance/"
        response = self.session.get(url, headers=self.headers)
        response = self.session.get("https://digital.etu.ru/attendance/api/auth", headers=self.headers,
                                    allow_redirects=False)
        time.sleep(10)
        response = self.session.get(response.headers["Location"], headers=self.headers, allow_redirects=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        login_data = {
            '_token': soup.find('input', {'name': '_token'})['value'],
            'state': '',
            'client_id': soup.find('input', {'name': 'client_id'})['value'],
            'auth_token': soup.find('input', {'name': 'auth_token'})['value'],
        }

        print(login_data)
        # _token: bqdLIWOvP6B4xyJcAV2jxgY7huZSAgDKbCSIV6XJ
        # state:
        # client_id: 29
        # auth_token: PoMRcX5W1FMWyjL
        # print(response.status_code, response.text)
        # todo: ОБРАТИТЬ ВНИМАНИКЕ перед asinc
        response = self.session.post("https://lk.etu.ru/oauth/authorize", headers=self.headers, params=login_data)
        # print(response.status_code, response.text)
        return self.session.cookies

    def get_session(self):
        response = self.session.get('https://lk.etu.ru/login', headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        login_data = {
            'email': os.getenv('login'),
            'password': os.getenv('password'),
            '_token': soup.find('input', {'name': '_token'})['value'],
        }
        response = self.session.post('https://lk.etu.ru/login', data=login_data,
                                     headers=self.headers)
        oauth_callback = f'https://api.id.etu.ru/portal/oauth{response.url[17:]}'
        login_data = {
            'email': os.getenv('login'),
            'password': os.getenv('password'),
            '_token': self.session.get('https://api.id.etu.ru/initialize').json()['token'],
        }
        self.session.post("https://api.id.etu.ru/auth/login", data=login_data,
                          headers=self.headers)
        response = self.session.get(oauth_callback, headers=self.headers)
        self.session.get(response.json()['redirect'], headers=self.headers)

    def get_news(self):
        news_link = f'https://lk.etu.ru/api/news?lang=ru'
        request = (self.session.get(news_link))
        print(f'TASK: {request.status_code} \n\n {request.json()}')
        return request.json()

    def get_user_info(self, user) -> str:
        link = f"https://lk.etu.ru/api/contact-list/contact-info/{user}"
        request = self.session.get(link, headers=self.headers)
        return f"{request.status_code} {request.text}"


temp = ETU_data()
bruh_test = temp.get_session()
# print(temp.get_timetable())
print(temp.get_timetable_session())
# print(temp.number_of_unread_messages())
