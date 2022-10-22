from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from time import time, ctime

from keyboards import *
from database import *

bot = Bot(TOKEN)
dp = Dispatcher(bot)  # Dispatcher осуществляет анализ и обработку входящих обновлений бота


@dp.message_handler(commands=['start', 'restart'])
async def start_command(message: types.Message):
    await message.answer(text='Добро пожаловать в Hotel_Telegram_KDA_Bot!\n'\
                              'Для продолжения выберите одну из опций на клавиатуре:',
                         reply_markup=get_start_kb())
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND, parse_mode='HTML')  # написать сообщение HELP_COMMAND


@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    await message.answer(text=DESCRIPTION)


@dp.message_handler(Text(equals='Бронь номеров'))
async def booking_rooms(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='бронь',
                           reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals='Ресторан'))
async def restaurant(message: types.Message):
    await message.answer('ресторан',
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals='Об отеле'))
async def about_hotel(message: types.Message):
    await message.answer('об отеле',
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals='Контактная информация'))
async def contact_inf(message: types.Message):
    await message.answer('контакты',
                         reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
