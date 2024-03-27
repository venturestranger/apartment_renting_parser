import telebot
from telebot import types
import sqlite3


bot = telebot.TeleBot('7138063286:AAFgtX4Bbjz5w5ltoUmaV2P2asSPbRhg6zo')

@bot.message_handler(commands=['start'])
def start_message(message):
    #Creation of Buttons
    markup = types.ReplyKeyboardMarkup()
    AddButton = types.KeyboardButton('Добавить Чат')
    ShowButton = types.KeyboardButton('Показать Все Чаты')
    markup.row(AddButton, ShowButton)
    bot.send_message(message.chat.id,f'Привет {message.from_user.first_name}!. Этот бот способен парсить сообщения каналов которые вы укажите. Чтобы начать добавьте чаты которые вы хотите пропарсить.', reply_markup=markup)






 #Creation of SQLite DB
conn = sqlite3.connect('database.sql')
curr = conn.cursor()
curr.execute('CREATE TABLE IF NOT EXISTS chats (id int autoincrement primary key, link varchar(100))')
conn.commit()
curr.close()
conn.close()


@bot.message_handler()
def button_reply(message):
        if message.text == 'Добавить Чат':
            bot.send_message(message.chat.id, '')













bot.polling(none_stop = True)
