import requests
from telebot import TeleBot
import sqlite3
bot = TeleBot('7065971962:AAHo9a1p8Ee8tINz89IZSOn2MiXyPsGUQyk')

@bot.message_handler(commands=['start'])
def start_command(message):
    con = sqlite3.connect('coolsite.db')
    cur = con.cursor()
    username = message.from_user.username
    user_id = message.from_user.id
    if cur.execute(f"""select * from user where username = '{username}'""").fetchall():
        print("Имя уже в базе данных")
        bot.send_message(message.chat.id, 'Имя уже в базе данных')
        return 0
    else:

        cur.execute(f"""INSERT INTO user (
                         user_id,
                         username
                     )
                     VALUES ('{user_id}', '{username}');
                         """)
        con.commit()
        con.close()
        bot.send_message(message.chat.id, 'Приветствую! Чем я могу вам помочь?')
        bot.send_message(message.chat.id,  username)
        bot.send_message(message.chat.id,  user_id)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.chat.id, message.text)


bot.polling()