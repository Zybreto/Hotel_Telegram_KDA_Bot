from aiogram import Bot, Dispatcher, executor, types
from time import time, ctime

from database import *


bot = Bot(TOKEN)
dp = Dispatcher(bot)  # Dispatcher осуществляет анализ и обработку входящих обновлений бота


if __name__ == '__main__':
    executor.start_polling(dp)
