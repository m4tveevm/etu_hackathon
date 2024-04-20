import requests
from telebot import TeleBot
import sqlite3
bot = TeleBot('7065971962:AAHo9a1p8Ee8tINz89IZSOn2MiXyPsGUQyk')

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Приветствую! Чем я могу вам помочь?')

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.chat.id, message.text)
conn = sqlite3.connect('bot_data.db')

bot.polling()