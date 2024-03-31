import telebot
from telebot import types
import sqlite3
from config import Config


# Creation of SQLite DB
conn = sqlite3.connect('database.sql')
curr = conn.cursor()
curr.execute('CREATE TABLE IF NOT EXISTS chat_list('
             'id INTEGER PRIMARY KEY, '
             'links TEXT,'
             'usernames TEXT,'
             'names TEXT,'
             'transfer INTEGER DEFAULT 0,'
             'chat_id INTEGER,'
             'k INTEGER'
             ')'
             )
curr.execute('CREATE TABLE IF NOT EXISTS parsed_list ('
             'id INTEGER PRIMARY KEY,'
             'message TEXT,'
             'user_id TEXT,'
             'upload_date TIMESTAMP,'
             'checked INTEGER DEFAULT 0'
             ')'
             )
conn.commit()
curr.close()
conn.close()



#Creation of dictionary for transfer of variables between functions


bot = telebot.TeleBot(Config.TELEBOT_TOKEN)
botf = telebot.TeleBot(Config.TELEBOTF_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    #Creation of Buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    AddButton = types.KeyboardButton('Добавить Чат')
    ShowButton = types.KeyboardButton('Показать Все Чаты')
    markup.row(AddButton, ShowButton)
    bot.send_message(message.chat.id,f'Привет {message.from_user.first_name}!.'
                                     f' Этот бот способен парсить сообщения каналов которые вы укажите.'
                                    f' Чтобы начать добавьте чаты которые вы хотите пропарсить.', reply_markup=markup)


owner_id = Config.OWNER_ID

def send_parsed(message):
    conn = sqlite3.connect('database.sql')
    curr = conn.cursor()
    curr.execute('SELECT message, user_id, id FROM parsed_list WHERE checked = ?', (0,))
    messages_and_user_ids = curr.fetchall()
    messages = []
    user_ids = []
    ids = []
    for i, message in enumerate(messages_and_user_ids):
        messages.append(messages_and_user_ids[i][0])
        user_ids.append(messages_and_user_ids[i][1])
        ids.append(messages_and_user_ids[i][2])
    for i, message in enumerate(messages):
        botf.send_message(owner_id, f'Пользователь - https://web.telegram.org/k/#{user_ids[i]}\nСообщение - "{message}".')
        curr.execute('UPDATE parsed_list SET checked = ? WHERE id = ?', (0, ids[i]))
    conn.commit()
    curr.close()
    conn.close()



@bot.message_handler(func=lambda message: message.text.lower() == 'показать все чаты')
def button_reply(message):
    username = message.from_user.username
    conn = sqlite3.connect('database.sql')
    curr = conn.cursor()
    curr.execute('SELECT links, names FROM chat_list WHERE usernames = ?', (username,))

    chat_list = curr.fetchall()
    if chat_list:
        chat_id = message.chat.id
        k = 0  # counter used to count id
        for i in chat_list:
            message_id = message.message_id
            date = message.date
            markup = types.InlineKeyboardMarkup()
            delete = types.InlineKeyboardButton('Удалить', callback_data=f'deleteAll_{chat_id}_{k+1}')
            markup.add(delete)
            link = chat_list[k][0]
            name = chat_list[k][1]
            bot.send_message(message.chat.id, f'{k+1}.{name} - {link}\n', reply_markup = markup)
            curr.execute('UPDATE chat_list SET k = ?, chat_id = ?  WHERE links = ? AND names = ?', (k+1, chat_id, link, name,))

            k = k+1
    else:
        bot.send_message(message.chat.id, 'Список чатов пуст. Пожалуйста добавьте чат!')
    conn.commit()
    curr.close()
    conn.close()

@bot.message_handler(func=lambda message: message.text.lower() == 'добавить чат')
def chat_addition_request(message):
    bot.send_message(message.chat.id, 'Отправьте ссылку на чат')
    bot.register_next_step_handler(message, chat_addition_link)

def chat_addition_link(message):
    username = message.from_user.username
    link = message.text
    conn = sqlite3.connect('database.sql')
    curr = conn.cursor()

    if link.startswith("http"):
        curr.execute('INSERT INTO chat_list (links, usernames, transfer) VALUES (?, ?, ?)', (link, username, 1))
        bot.send_message(message.chat.id, 'Напишите название чата под которым он будет сохранен.')
        bot.register_next_step_handler(message, chat_addition_name, link)
    else:
        bot.send_message(message.chat.id,"""
Вы отправили не ссылку.
Процесс добавления чата для парсинга прекращается.
Чтобы начать заново нажмите на кнопку 'добавить чат'""")

    conn.commit()
    curr.close()
    conn.close()

def chat_addition_name(message, link):
    username = message.from_user.username
    name = message.text
    markup = types.InlineKeyboardMarkup()
    delete = types.InlineKeyboardButton('Удалить', callback_data = 'deleteAdd')
    correct = types.InlineKeyboardButton('Подтвердить', callback_data = 'accept')
    markup.row(correct,delete)
    conn = sqlite3.connect('database.sql')
    curr = conn.cursor()
    curr.execute('UPDATE chat_list SET names = ? WHERE links = ? and usernames = ?', (name, link,username,))
    bot.send_message(message.chat.id, f"""
    Ссылка - "{link}"
Название - "{name}"
Если присутствует ошибка, нажмите кнопку "Удалить" и начните заново.
    """, reply_markup = markup)
    conn.commit()
    curr.close()
    conn.close()


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    username = call.from_user.username
    conn = sqlite3.connect('database.sql')
    curr = conn.cursor()
    # deleteAll
    callback_data = call.data.split("_")
    action = callback_data[0]
    if call.data == 'deleteAdd':
        curr.execute('SELECT links, names FROM chat_list WHERE transfer = ? AND usernames = ?', (1, username,))
        transfer = curr.fetchall()
        link = transfer[0][0]
        name = transfer[0][1]
        curr.execute('DELETE FROM chat_list WHERE usernames = ? AND links = ? AND names = ?', (username, link, name,))
        bot.send_message(call.message.chat.id,
                         'Чат не был сохранен. Чтобы начать процесс заново нажмите кнопку "Добавить Чат".')
    elif call.data == 'accept':
        curr.execute('UPDATE chat_list SET transfer = ? WHERE transfer = ?', (0, 1,))
        bot.send_message(call.message.chat.id, 'Чат был успешно добавлен!')
    elif action == 'deleteAll':
        chat_id = callback_data[1]
        counter = callback_data[2]
        curr.execute('DELETE FROM chat_list WHERE chat_id = ? AND k = ?', (chat_id, counter,))
        bot.send_message(call.message.chat.id, 'Чат был успешно удален из списка.')

    # Edit the original message to remove the InlineKeyboardMarkup
    bot.delete_message(call.message.chat.id, call.message.message_id)

    conn.commit()
    curr.close()
    conn.close()
    #Creation of interface buttons to handle the input to user

if __name__=='__main__':
    bot.polling(none_stop = True)
