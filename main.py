import telebot
from telebot import types
import sqlite3
from config import Config
import threading
from time import sleep



# Creation of SQLite db
conn = sqlite3.connect('database.sql')
curr = conn.cursor()
curr.execute('CREATE TABLE IF NOT EXISTS chat_list('
			 'id INTEGER PRIMARY KEY, '
			 'links TEXT,'
			 'usernames TEXT,'
			 'names TEXT,'
			 'transfer INTEGER DEFAULT 0,'
			 'chat_id INTEGER,'
			 'k INTEGER,'
			 'keywords TEXT'
			 ')'
			 )
curr.execute('CREATE TABLE IF NOT EXISTS keyword_list ('
			 'id INTEGER PRIMARY KEY,'
			 'keywords TEXT DEFAULT "empty",'
			 'words TEXT,'
			 'usernames TEXT,'
			 'k INTEGER'
			 ')'
			 )
curr.execute('CREATE TABLE IF NOT EXISTS parsed_list ('
			 'id INTEGER PRIMARY KEY,'
			 'message TEXT,'
			 'user_id TEXT,'
			 'chat_name TEXT,'
			 'chat_title TEXT,'
			 'upload_date TIMESTAMP,'
			 'checked INTEGER DEFAULT 0'
			 ')'
			 )
conn.commit()
curr.close()
conn.close()

bot = telebot.TeleBot(Config.TELEBOT_TOKEN)
botf = telebot.TeleBot(Config.TELEBOTF_TOKEN)

def onstart():
	while True:
		try:
			send_parsed()
			print(e, 'IN ons TARGET')
		except Exception as e:
			sleep(Config.TIMEOUT)

@bot.message_handler(commands=['start'])
def start_message(message):
	#Creation of Buttons
	user_id = message.chat.id
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	AddButton = types.KeyboardButton('Добавить Чат')
	ShowButton = types.KeyboardButton('Показать Все Чаты')
	AddWord = types.KeyboardButton('Добавить Слово для Поиска')
	ShowWords = types.KeyboardButton('Показать Все Слова')
	markup.row(AddButton, ShowButton)
	markup.row(AddWord, ShowWords)
	bot.send_message(message.chat.id,f'Привет {message.from_user.first_name}!.'
									 f' Этот бот способен парсить сообщения каналов которые вы укажите.'
									 f'Также была добавлена новая функция поиска сообщений по ключевым словам.'
									f' Чтобы начать добавьте чаты которые вы хотите пропарсить.', reply_markup=markup)

def send_parsed():
	conn = sqlite3.connect('database.sql')

	curr = conn.cursor()
	curr.execute('SELECT message, user_id, id, chat_name, chat_title FROM parsed_list WHERE checked = ?', (0,))
	messages_and_user_ids = curr.fetchall()
	messages = []
	user_ids = []
	ids = []
	chat_name = []
	chat_title = []
	for i, message in enumerate(messages_and_user_ids):
		messages.append(messages_and_user_ids[i][0])
		user_ids.append(messages_and_user_ids[i][1])
		ids.append(messages_and_user_ids[i][2])
		chat_name.append(messages_and_user_ids[i][3])
		chat_title.append(messages_and_user_ids[i][4])

	#Reversing arrays to print them in ascending order with respect to time
	messages.reverse()
	user_ids.reverse()
	ids.reverse()
	chat_name.reverse()
	chat_title.reverse()

	for i, message in enumerate(messages):

		botf.send_message(Config.OWNER_ID, f'Пользователь - t.me/{chat_name[i][13:]}/{user_ids[i]}\nСообщение: \n"{message}".\nОткуда - {chat_title[i]}')
		curr.execute('UPDATE parsed_list SET checked = ? WHERE id = ?', (1, ids[i]))
	conn.commit()
	curr.close()
	conn.close()


@bot.message_handler(func=lambda message: message.text.lower() == 'показать все чаты')
def button_reply(message):
	conn = sqlite3.connect('database.sql')
	

	username = message.from_user.username
	curr = conn.cursor()
	curr.execute('SELECT links, names FROM chat_list WHERE usernames = ?', (username,))
	chat_list = curr.fetchall()
	if chat_list:
		chat_id = message.chat.id
		k = 0  # counter used to count id
		for i in chat_list:
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
	conn = sqlite3.connect('database.sql')

	username = message.from_user.username
	link = message.text
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
	conn = sqlite3.connect('database.sql')

	username = message.from_user.username
	name = message.text
	markup = types.InlineKeyboardMarkup()
	delete = types.InlineKeyboardButton('Удалить', callback_data = 'deleteAdd')
	correct = types.InlineKeyboardButton('Подтвердить', callback_data = 'accept')
	markup.row(correct,delete)
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

@bot.message_handler(func=lambda message: message.text.lower() == 'показать все слова')
def show_words(message):
	conn = sqlite3.connect('database.sql')
	curr = conn.cursor()
	username = message.from_user.username
	curr.execute('SELECT words FROM keyword_list WHERE usernames = ?', (username,))
	word_list = curr.fetchall()
	k = 0

	if word_list:
		for word in word_list:
			markup = types.InlineKeyboardMarkup()
			delete = types.InlineKeyboardButton('Удалить', callback_data=f'deleteShowAllWords_{k + 1}')
			markup.add(delete)
			Word = word_list[k][0]
			bot.send_message(message.chat.id, f"{k+1}. {Word}.\n", reply_markup = markup)
			curr.execute('UPDATE keyword_list SET k = ? WHERE words = ?',	 (k + 1, Word,))
			k = k+1
	else:
		bot.send_message(message.chat.id, "Список слов для поиска пуст. Добавьте слово чтобы начать его поиск.")

	conn.commit()
	curr.close()
	conn.close()
@bot.message_handler(func=lambda message: message.text.lower() == 'добавить слово для поиска')
def word_addition_request(message):
	bot.send_message(message.chat.id, "Пожалуйста напишите слово по которому вы хотите искать сообщения:")
	bot.register_next_step_handler(message, word_addition_into_table)

def word_addition_into_table(message):
	conn = sqlite3.connect('database.sql')
	curr = conn.cursor()
	word = message.text
	username = message.from_user.username
	if len(message.text) < 5:
		keyword = message.text
	elif len(message.text) == 5:
		 keyword = message.text[1:4]
	elif len(message.text) == 6:
		keyword = message.text[1:5]
	elif len(message.text) == 7:
		keyword = message.text[1:5]
	elif len(message.text) == 8:
		keyword = message.text[2:7]
	elif len(message.text) > 8:
		keyword = message.text[2:8]

	markup = types.InlineKeyboardMarkup()
	delete = types.InlineKeyboardButton('Удалить', callback_data=f'deleteWord_{keyword}')
	correct = types.InlineKeyboardButton('Подтвердить', callback_data='acceptWord')
	markup.row(correct, delete)

	curr.execute('INSERT INTO keyword_list (keywords, words, usernames) VALUES(?, ?, ?)', (keyword, word,  username, ))
	bot.send_message(message.chat.id, f'Добавленное слово - {message.text}\nЕсли присутствует ошибка, нажмите кнопку "Удалить" и начните заново.', reply_markup = markup)
	conn.commit()
	curr.close()
	conn.close()






@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
	conn = sqlite3.connect('database.sql')


	username = call.from_user.username
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
		bot.send_message(call.message.chat.id, 'Чат был успешно добавлен!')
		curr.execute('UPDATE chat_list SET transfer = ? WHERE transfer = ?', (0, 1,))
	elif action == 'deleteAll':
		chat_id = callback_data[1]
		counter = callback_data[2]
		curr.execute('DELETE FROM chat_list WHERE chat_id = ? AND k = ?', (chat_id, counter,))
		bot.send_message(call.message.chat.id, 'Чат был успешно удален из списка.')
	elif action == 'deleteWord':
		keyword = callback_data[1]
		curr.execute('DELETE FROM keyword_list WHERE keywords = ?', (keyword,))
		bot.send_message(call.message.chat.id, "Слово не было сохранено. Чтобы добавить слово для поиска начните процесс заново.")
	elif call.data == 'acceptWord':
		bot.send_message(call.message.chat.id, "Слово было успешно сохранено.")
	elif action == 'deleteShowAllWords':
		counter = callback_data[1]
		curr.execute('DELETE FROM keyword_list WHERE k = ?', (counter,))
		bot.send_message(call.message.chat.id, 'Слово было успешно удалено из списка!')
	# Edit the original message to remove the InlineKeyboardMarkup
	bot.delete_message(call.message.chat.id, call.message.message_id)

	conn.commit()
	curr.close()
	conn.close()
	#Creation of interface buttons to handle the input to user


if __name__=='__main__':
	bot1 = threading.Thread(target=lambda: bot.polling(none_stop=True))
	bot2 = threading.Thread(target=lambda: botf.polling(none_stop=True))
	ons = threading.Thread(target=lambda: onstart())

	try:
		bot1.start()
		bot2.start()
		ons.start()
	finally:
		bot1.join()
		bot2.join()
		ons.join()
