from aiogram import Bot, Dispatcher, executor, types
from time import time, ctime

from database import *


bot = Bot(TOKEN)
dp = Dispatcher(bot)  # Dispatcher осуществляет анализ и обработку входящих обновлений бота


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text='Добро пожаловать в Hotel_Telegram_KDA_Bot')
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND, parse_mode='HTML')  # написать сообщение HELP_COMMAND


@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    await message.answer(text=DESCRIPTION)


if __name__ == '__main__':
    executor.start_polling(dp)
