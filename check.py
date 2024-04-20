import requests
import json
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
# print(temp.get_user_info(1))
