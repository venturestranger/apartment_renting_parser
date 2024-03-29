import telebot
from telebot import types
import sqlite3




The code structure

 import of necessary modules + telethon + engine api
 addition of tokens for both bot and botf
 /start message
 the creation of sqlite3 db that consists of 2 tables. 1: id, username, links, name; 2: id, username, message, boolean, inserted_time.
 creation of keyboard buttons
 creation of inline keyboard buttons related to input
 lambda functions that handle pure text without slash /
 callback_handling


    the use of telethon parser bot + api + botf to forward messages
        make a condition to check the date of records in parsed_lsot table to delete records older than 30 days.

    Have a confusion related to OOP and the way different objects work in different files.


# Creation of SQLite DB
    conn = sqlite3.connect('database.sql')
    curr = conn.cursor()
    curr.execute('CREATE TABLE IF NOT EXISTS chat_list,('
                 'id INTEGER PRIMARY KEY, '
                 'link varchar(100)'
                 'username varchar(50)'
                 ')'
                 )
    curr.execute('CREATE TABLE IF NOT EXISTS parsed_list, ('
                 'id INTEGER PRIMARY KEY'
                 'username varchar(50)'
                 'text'
                 'boolean'
                 )
    conn.commit()
    curr.close()
    conn.close()






bot = telebot.TeleBot('7138063286:AAFgtX4Bbjz5w5ltoUmaV2P2asSPbRhg6zo')
botf = telebot.TeleBot('6922598981:AAEr6uhM_gog7V6kmn6pvToiZ5GgAz_mmjs')
@bot.message_handler(commands=['start'])
def start_message(message):
    #Creation of Buttons
    markup = types.ReplyKeyboardMarkup()
    AddButton = types.KeyboardButton('Добавить Чат')
    ShowButton = types.KeyboardButton('Показать Все Чаты')
    markup.row(AddButton, ShowButton)
    bot.send_message(message.chat.id,f'Привет {message.from_user.first_name}!.'
                                     f' Этот бот способен парсить сообщения каналов  которые вы укажите.'
                                    f'Чтобы начать добавьте чаты которые вы хотите пропарсить.', reply_markup=markup)







@bot.message_handler(func=lambda message: message.text.lower() == 'добавить чат')
def button_reply(message):
    bot.register_next_step_handler(message, chat_addition)

def chat_addition(message):
#Saving user input and username
    link = message.text
    username = message.from_user.username

#Creation of interface buttons to handle the input to user
    markup = types.InlineKeyboardMarkup
    edit = types.InlineKeyboardButton('Изменить ответ', callback_data='edit')















bot.polling(none_stop = True)
