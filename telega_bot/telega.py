import requests
from telebot import TeleBot
import sqlite3
from threading import local

# Create thread-local storage for database objects
db_tls = local()
bot = TeleBot('7065971962:AAHo9a1p8Ee8tINz89IZSOn2MiXyPsGUQyk')
def get_db_connection():
    if not hasattr(db_tls, 'connection'):
        db_tls.connection = sqlite3.connect('coolsite.db')
    return db_tls.connection

def get_cursor():
    connection = get_db_connection()
    return connection.cursor()

def close_connection():
    if hasattr(db_tls, 'connection'):
        db_tls.connection.close()
def add_user(id, username):
    # Prepare SQL INSERT statement
    sql_insert = f"""INSERT INTO user (
                     id,
                     username
                 )
                 VALUES 
                     {id},
                     {username}
                 """
    print(sql_insert)

    # Create cursor object
    cursor = get_cursor()

    # Execute the INSERT statement with user ID and username
    cursor.execute(sql_insert)

    # Commit changes to the database
    get_db_connection().commit()

@bot.message_handler(commands=['start'])
def start_command(message):
    username = message.chat.username
    user_id = message.chat.id
    # Add user to the database using the function
    add_user(user_id, username)

    # Send a welcome message to the user
    bot.send_message(message.chat.id, f'Приветствую, {username}! Вы успешно зарегистрированы.')
    close_connection()

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.chat.id, message.text)


bot.polling()
