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


def get_adult_num_ikb():
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


def get_children_num_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('1', callback_data='1'), InlineKeyboardButton('2', callback_data='2'))
    ikb.add(InlineKeyboardButton('3', callback_data='3'))
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb


def get_children_age_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('младше 6 лет', callback_data='0'))
    ikb.add(InlineKeyboardButton('6 - 12 лет', callback_data='1'))
    ikb.add(InlineKeyboardButton('12 - 18 лет', callback_data='2'))
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb


def main_menu_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb

