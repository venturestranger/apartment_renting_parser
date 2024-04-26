from telethon import TelegramClient, errors, utils
from telethon.tl.functions.messages import GetHistoryRequest
from config import Config
from time import sleep
from datetime import datetime 
from datetime import timedelta
from backend.backend import API
from backend.config import KWC_Config
import asyncio
import sqlite3
import sys

username = Config.USERNAME
api_id = Config.API_ID
api_hash = Config.API_HASH
limit_per_request = Config.LIMIT_MESSAGES
timeout = Config.TIMEOUT
db_path = Config.DATABASE_PATH
api = API()
chat_titles = []
api.connect(engine_path='./engine_dumps/KWC_NTVRF_0.7.pkl')

api2 = API()
try:
	api2.connect(engine_path='./engine_dumps/secondary.pkl')
except:
	config = KWC_Config()
	config.ADDS = ['/null']
	api2.connect(engine_type='KWC', optional={'KWC_config': config})
	api2.dump_engine('./engine_dumps/secondary.pkl')

async def get_channel_messages(channel_username, limit):
	async with TelegramClient(username, api_id, api_hash) as client:
		try:
			keywords = []
			keywords_fetched = []

			conn = sqlite3.connect('database.sql')
			curr = conn.cursor()
			curr.execute('SELECT keywords FROM keyword_list')
			keywords_raw = curr.fetchall()
			curr.close()
			conn.close()
			i = 0
			for keyword in keywords_raw:
				a = keywords_raw[i][0]
				keywords_fetched.append(a)
				i = i +1
			print(keywords_fetched)
			if set(keywords) != set(keywords_fetched):
				keywords = keywords_fetched.copy()

				print(keywords)
				config = KWC_Config()
				config.ADDS = keywords.copy()
				api2.connect(engine_type='KWC', optional={'KWC_config': config})
				api2.dump_engine('./engine_dumps/secondary.pkl')



			channel = await client.get_entity(channel_username)

			offset_msg = 0
			k = channel.title

			history = await client(GetHistoryRequest(
					peer=channel,
					offset_id=offset_msg,
					offset_date=None,
					add_offset=0,
					limit=limit,
					max_id=0,
					min_id=0,
					hash=0
			))

			conn = sqlite3.connect(db_path)
			cur = conn.cursor()

			try:
				cur.execute('DELETE FROM parsed_list WHERE checked = 1 AND upload_date < ?', (str(datetime.now() - timedelta(days=7)),))
			except:
				pass

			for message in history.messages:
				print(message.message) # Here api2 is similarity model and api is main model
				if (message.message != None and api.query(message.message) == True) or (message.message != None and api2.query(message.message) == True):
					print(message.message)
					try:
						cur.execute('SELECT id FROM parsed_list WHERE chat_name = ? AND user_id = ?', (channel_username, message.id))
						data = cur.fetchall()

						if len(data) == 0:
							cur.execute('INSERT INTO parsed_list(message, user_id, chat_name, chat_title, upload_date, checked) VALUES(?, ?, ?, ?, ?, ?)', (message.message, message.id, channel_username, channel.title , datetime.now(), 0))
					except Exception as e:
						print(e)

			conn.commit()
			conn.close()

		except Exception as e:
			print(e)


if __name__ == "__main__":
	while True:
		conn = sqlite3.connect(db_path)
		cur = conn.cursor()
		cur.execute('SELECT links FROM chat_list')
		links = cur.fetchall()
		conn.close()
		print(f'--- Links fetched:  {links}')

		if len(sys.argv) > 1 and sys.argv[1] == 'auto-start':
			for link in links:
				try:
					asyncio.run(get_channel_messages(link[0], limit_per_request))
					print(f'--- Fetched from  {link[0]}')
					print('--- Went sleeping')
				except:
					pass
			sleep(timeout)
		else:
			for link in links:
				asyncio.run(get_channel_messages(link[0], limit_per_request))
				print(f'--- Fetched from  {link[0]}')
				print('--- Went sleeping')
			sleep(timeout)
		sleep(timeout)
