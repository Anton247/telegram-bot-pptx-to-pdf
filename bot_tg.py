import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import datetime
from datetime import timedelta
import uuid
import os
from settings import TOKEN
from sqlite3.dbapi2 import Cursor
from PPTX_GENERATOR import PPTX_GENERATOR 
import sqlite3
API_TOKEN = TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

mess = {}       #Тут будем считать сообщения через словарь
mess_time = datetime.date.today()   #Храним сегодняшнюю дату

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Хочу сертификат"]
keyboard.add(*buttons)
last_time = datetime.datetime.now()
@dp.message_handler(commands=['start', 'help', 'сертификат'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет, "+ message.from_user.first_name + "!\n👋🏼😀\nЯ Квантоша, бот, созданный для отправки сертификата о посещении дня\
		открытых дверей\nНапиши мне своё имя и я отправлю тебе твой сертификат", reply_markup=keyboard)

@dp.message_handler(Text(equals="Хочу сертификат"))
async def certificate(message: types.Message):
	await message.answer("Напиши мне свои ФИО", reply_markup=keyboard)

@dp.message_handler()
async def echo(message: types.Message):
	global mess
	global mess_time
	if mess_time != datetime.date.today(): #Если дата не сегодня, сбрасываем все сообщения
		mess = {}
		mess_time = datetime.date.today()   #Храним сегодняшнюю дату
	check = 1
	if message.from_user.id not in mess: #Если пользователь не писал сообщения, то добавляем его ID в словарь и присваиваем время
		mess[message.from_user.id] = datetime.datetime.now()
	elif (datetime.datetime.now() - mess[message.from_user.id]).total_seconds() < 10: #Ставим ограничения на кол-во сообщений
		await message.answer('Мне можно писать не чаще чем раз в 10 секунд\nТебе придётся подождать')
		check = 0
	if check:
		mess[message.from_user.id] = datetime.datetime.now()
		await message.answer("Твой сертификат создаётся, подожди немного")
		now = str(datetime.date.today().day)
		now += "-" + str(datetime.date.today().month)
		now += "-" + str(datetime.date.today().year)
		UID = uuid.uuid4().hex #уникальный идентификатор
		file = PPTX_GENERATOR(message.text, UID, now)
		file = file.replace(" ", "©")
		command = "python PPTX_to_PDF.py " + file + " " + now
		res = os.system(command)  # открываем скрипт для форматирования	
		file = file.replace("©", " ")
		doc = open('./GENERATED_PDF/' + now + '/' + file + ".pdf", 'rb')
		await message.reply_document(doc)

		connect = sqlite3.connect('users.db')
		cursor = connect.cursor()
		cursor.execute("""CREATE TABLE IF NOT EXISTS users(
				user_id TEXT PRIMARY KEY,
				user_name TEXT,
				date TEXT,
				time TEXT,
				source TEXT,
				uname_source TEXT,
				uid_source TEXT
				)
				""")	
		now_time = datetime.datetime.now()
		users_list = [UID, message.text, now, now_time.strftime("%H:%M:%S"), "Telegram", message.from_user.username, message.from_user.id]
		cursor.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?);", users_list)
		connect.commit()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)