from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


def get_start_kb():
    kb = ReplyKeyboardMarkup([[KeyboardButton('Бронь номеров'), KeyboardButton('Ресторан')],
                              [KeyboardButton('Об отеле'), KeyboardButton('Контактная информация')]],
                             resize_keyboard=True)
    return kb
