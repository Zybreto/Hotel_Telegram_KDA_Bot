from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


def get_start_kb():
    kb = ReplyKeyboardMarkup([[KeyboardButton('Бронь номеров'), KeyboardButton('Ресторан')],
                              [KeyboardButton('Об отеле'), KeyboardButton('Контактная информация')]],
                             resize_keyboard=True,
                             one_time_keyboard=True)
    return kb


def get_room_category_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('Standard', callback_data='standard'), InlineKeyboardButton('Studio', callback_data='studio'))
    ikb.add(InlineKeyboardButton('Suite', callback_data='suite'), InlineKeyboardButton('Delux', callback_data='delux'))
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb


def get_people_num_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('1', callback_data='1'), InlineKeyboardButton('2', callback_data='2'))
    ikb.add(InlineKeyboardButton('3', callback_data='3'), InlineKeyboardButton('4', callback_data='4'))
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb


def get_children_presense_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('Да', callback_data='да'), InlineKeyboardButton('Нет', callback_data='нет'))
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb


def get_choosing_dates_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)

    return ikb
