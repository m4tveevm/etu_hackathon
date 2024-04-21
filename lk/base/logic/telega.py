import os
import requests
from telebot import TeleBot
import sqlite3
from foreign_lk import ETU_data_with_cookies
from foreign_lk import ETU_data
from bs4 import BeautifulSoup

bot = TeleBot('7065971962:AAHo9a1p8Ee8tINz89IZSOn2MiXyPsGUQyk')



def send_notification():
    temp = ETU_data(login=os.getenv('login'), password=os.getenv('password'))
    temper = ETU_data_with_cookies(temp.get_cookies()).number_of_unread_messages()
    return temper


@bot.message_handler(commands=['start'])
def start_command(message):
    con = sqlite3.connect('coolsite.db')
    cur = con.cursor()
    username = message.from_user.username
    user_id = message.from_user.id
    if cur.execute(f"""select * from users where username = '{username}'""").fetchall():

        bot.send_message(message.chat.id, 'Имя уже в базе данных')
        return 0
    else:

        cur.execute(f"""INSERT INTO users (
                         user_id,
                         username
                     )
                     VALUES ('{user_id}', '{username}');
                         """)
        con.commit()
        con.close()
        bot.send_message(message.chat.id, 'Приветствую! Чем я могу вам помочь?')
        bot.send_message(message.chat.id, username)
        bot.send_message(message.chat.id, user_id)


@bot.message_handler(commands=['check_message'])
def start_command1(message):
    if str(send_notification() == None):
        bot.send_message(message.chat.id, "Новых сообщений нет")
    else:
        bot.send_message(message.chat.id, f"У вас {send_notification()} непрочитанных сообщений")


bot.polling()
