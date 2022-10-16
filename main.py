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


@dp.message_handler(commands=['tasks'])
async def tasks_command(message: types.Message):
    await message.answer(text=f"<b>Задачи Hotel_Telegram_KDA_Bot</b>\n\n" \
                              f"<b>Общие: </b> <em>{get_dev_task('joint')[1]}</em>\n\n" \
                              f"<b>Дима: </b> <em>{get_dev_task('dima')[1]}</em>\n\n" \
                              f"<b>Андрей: </b> <em>{get_dev_task('andrey')[1]}</em>\n\n" \
                              f"<b>Кирилл: </b> <em>{get_dev_task('kirill')[1]}</em>",
                         parse_mode="HTML")


@dp.message_handler(commands=['edit_task'])
async def edit_task(message: types.Message):
    dev = message.text.split()[1]
    new_task = message.text.split()
    del new_task[:2]
    new_task = ' '.join(new_task)
    set_dev_task(dev, new_task)

    await message.answer(text=f'Задача {dev} изменена на "{new_task}"')


@dp.message_handler(commands=['report'])
async def report_command(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo=open('res/images/report_content.jpg', 'rb'))


if __name__ == '__main__':
    executor.start_polling(dp)
