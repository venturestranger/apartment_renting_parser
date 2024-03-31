from telethon import TelegramClient, errors, utils
from telethon.tl.functions.messages import GetHistoryRequest
from config import Config
from time import sleep
from datetime import datetime 
import asyncio
import sqlite3
import sys

username = Config.USERNAME
api_id = Config.API_ID
api_hash = Config.API_HASH
limit_per_request = Config.LIMIT_MESSAGES
timeout = Config.TIMEOUT
db_path = Config.DATABASE_PATH


async def get_channel_messages(channel_username, limit):
	async with TelegramClient(username, api_id, api_hash) as client:
		try:
			channel = await client.get_entity(channel_username)

			offset_msg = 0
			all_messages = []

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
			for message in history.messages:
				cur.execute('DELETE FROM parsed_list WHERE checked = 1')
				cur.execute('INSERT INTO parsed_list(message, user_id, upload_date, checked) VALUES(?, ?, ?, ?)', (message.message, message.from_id.user_id, datetime.now(), 0))
			conn.commit()
			conn.close()

		except Exception as e:
			print(e)


if __name__ == "__main__":
	print('--- Working with {sys.argv[1]}')

	while True:
		conn = sqlite3.connect(db_path)
		cur = conn.cursor()
		cur.execute('SELECT links FROM chat_list')
		links = cur.fetchall()
		conn.close()
		print(f'--- Links fetched:  {links}')

		if sys.argv[1] == 'auto-start':
			for link in links:
				try:
					asyncio.run(get_channel_messages(link[0], limit_per_request))
					print(f'--- Fetched from  {link[0]}')
					print('--- Went sleeping')
					sleep(timeout)
				except:
					pass
		else:
			for link in links:
				asyncio.run(get_channel_messages(link[0], limit_per_request))
				print(f'--- Fetched from  {link[0]}')
				print('--- Went sleeping')
				sleep(timeout)
