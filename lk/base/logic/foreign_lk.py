import requests
import json
import time
from http.cookies import SimpleCookie
import datetime
from bs4 import BeautifulSoup

import os
from dotenv import load_dotenv

load_dotenv()


class ETUData:
    def __init__(self, login, password):
        self.login, self.password = login, password
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
            "537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        self.session = requests.Session()

    def number_of_unread_messages(self):
        try:
            response = self.session.get(
                "https://lk.etu.ru/api/profile/" "menu_counters", headers=self.headers
            )
            response_json = json.loads(response.text)
            messages_to_count = response_json["messages_to"]["count"]
            if messages_to_count > 0:
                return str(messages_to_count)
            else:
                return None
        except Exception as e:
            print(f"Error retrieving notification: {e}")
            return 0

    def get_timetable_session(self):
        url = "https://digital.etu.ru/attendance/"
        self.session.get(url, headers=self.headers)
        response = self.session.get(
            "https://digital.etu.ru/attendance/api/auth", allow_redirects=False
        )
        # todo: ОБРАТИТЬ ВНИМАНИЕ перед asinc \/
        time.sleep(5)
        response = self.session.get(
            response.headers["Location"], headers=self.headers, allow_redirects=False
        )
        soup = BeautifulSoup(response.text, "html.parser")
        login_data = {
            "_token": soup.find("input", {"name": "_token"})["value"],
            "state": "",
            "client_id": soup.find("input", {"name": "client_id"})["value"],
            "auth_token": soup.find("input", {"name": "auth_token"})["value"],
        }
        self.session.post("https://lk.etu.ru/oauth/authorize", params=login_data)

    def get_cookies(self):
        response = self.session.get("https://lk.etu.ru/login")
        soup = BeautifulSoup(response.text, "html.parser")
        login_data = {
            "email": self.login,
            "password": self.password,
            "_token": soup.find("input", {"name": "_token"})["value"],
        }
        response = self.session.post("https://lk.etu.ru/login", data=login_data)
        oauth_callback = f"https://api.id.etu.ru/portal/oauth{response.url[17:]}"
        login_data = {
            "email": self.login,
            "password": self.password,
            "_token": self.session.get("https://api.id.etu.ru/initialize").json()[
                "token"
            ],
        }
        self.session.post("https://api.id.etu.ru/auth/login", data=login_data)
        response = self.session.get(oauth_callback, headers=self.headers)
        self.session.get(response.json()["redirect"], headers=self.headers)
        self.get_timetable_session()
        cookie_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        return json.dumps(cookie_dict)

    def load_cookies_from_json(self, json_cookies):
        """Loads cookies from a JSON string into the session's cookies"""
        cookie_obj = SimpleCookie()
        cookie_dict = json.loads(json_cookies)
        for key, value in cookie_dict.items():
            cookie_obj[key] = value
        for morsel in cookie_obj.values():
            self.session.cookies.set(morsel.key, morsel.value, domain=morsel["domain"])

    def get_news(self):
        news_link = "https://lk.etu.ru/api/news?lang=ru"
        request = self.session.get(news_link)
        print(f"TASK: {request.status_code} \n\n {request.json()}")
        return request.json()

    def get_user_info(self, user) -> str:
        link = f"https://lk.etu.ru/api/contact-list/contact-info/{user}"
        request = self.session.get(link)
        return f"{request.status_code} {request.text}"


class ETUDataWithCookies:
    def __init__(self, cookies):
        self.session = requests.Session()
        if cookies:
            self.headers = {"cookies": self.load_cookies_from_json(cookies)}
        else:
            self.headers = {}

    def load_cookies_from_json(self, cookies):
        cookie_obj = SimpleCookie()
        cookie_dict = json.loads(cookies)
        for key, value in cookie_dict.items():
            cookie_obj[key] = value
        for morsel in cookie_obj.values():
            self.session.cookies.set(morsel.key, morsel.value, domain=morsel["domain"])

    def number_of_unread_messages(self):
        try:
            response = self.session.get(
                "https://lk.etu.ru/api/profile/menu_counters", headers=self.headers
            )
            response_json = json.loads(response.text)
            messages_to_count = response_json["messages_to"]["count"]
            if messages_to_count > 0:
                return str(messages_to_count)
            else:
                return None
        except Exception as e:
            print(f"Error retrieving notification: {e}")
            return 52

    def timetable_checkin(self):
        try:
            response = self.session.get(
                "https://digital.etu.ru/attendance/api/schedule/check-in",
                headers=self.headers,
            )
            events = json.loads(response.text)
            today_date = (datetime.datetime.now()).strftime("%Y-%m-%d")

            today_events = []
            for event in events:
                event_date = event["start"][:10]
                if event_date == today_date:
                    today_events.append(event)
            return today_events

        except Exception as e:
            print(f": {e}")
            return 52


# temp = ETUData(login=os.getenv('login'), password=os.getenv('password'))
# print(temp.get_cookies())
# temper = ETU_data_with_cookies(temp.get_cookies())
