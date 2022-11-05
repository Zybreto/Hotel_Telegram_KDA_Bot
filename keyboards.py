from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from database import get_room_name


def get_start_kb():
    kb = ReplyKeyboardMarkup([[KeyboardButton('Бронь номеров'), KeyboardButton('Дополнительные услуги')],
                              [KeyboardButton('Об отеле'), KeyboardButton('Контактная информация')]],
                             resize_keyboard=True,
                             one_time_keyboard=True)
    return kb


def get_room_category_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('Standard', callback_data='standard'), InlineKeyboardButton('Studio', callback_data='studio'))
    ikb.add(InlineKeyboardButton('Suite', callback_data='suite'), InlineKeyboardButton('Delux', callback_data='deluxe'))
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


def get_check_capacity_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('Проверить на вместимость\n' \
                                 '*тык*',
                                 callback_data='check'))
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb


def get_main_menu_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb


def get_choosing_date_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('Верно', callback_data='yes'), InlineKeyboardButton('Исправить', callback_data='no'))
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb


def get_choosing_room_ikb(rooms_id: list):
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    if len(rooms_id) >= 2 and len(rooms_id) % 2 == 0:
        for i in range(0, len(rooms_id)-1, 2):
            ikb.add(InlineKeyboardButton(f'{get_room_name(rooms_id[i])}', callback_data=rooms_id[i]),
                    InlineKeyboardButton(f'{get_room_name(rooms_id[i+1])}', callback_data=rooms_id[i+1]))
    elif len(rooms_id) > 2 and len(rooms_id) % 2 != 0:
        for i in range(0, len(rooms_id)-2, 2):
            ikb.add(InlineKeyboardButton(f'{get_room_name(rooms_id[i])}', callback_data=rooms_id[i]),
                    InlineKeyboardButton(f'{get_room_name(rooms_id[i+1])}', callback_data=rooms_id[i+1]))
        ikb.add(InlineKeyboardButton(f'{get_room_name(rooms_id[len(rooms_id)-1])}', callback_data=rooms_id[len(rooms_id)-1]))
    elif len(rooms_id) == 1:
        ikb.add(InlineKeyboardButton(f'{get_room_name(rooms_id[0])}', callback_data=rooms_id[0]))

    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb


def get_confirm_room_selection_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('Оставить этот номер', callback_data='this'))
    ikb.add(InlineKeyboardButton('Выбрать другой номер', callback_data='yes'))  # 'yes' нужен для корректного возврата к выбору номера
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb


def get_authorization_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('Перейти к авторизации', callback_data='auth'))
    ikb.add(InlineKeyboardButton('Выбрать другой номер', callback_data='yes'))
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb


def get_card_check_ikb():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('Верно', callback_data='true'))
    ikb.add(InlineKeyboardButton('Ввести заново', callback_data='false'))
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb


def get_additional_services():
    ikb = InlineKeyboardMarkup(resize_keyboard=True)
    ikb.add(InlineKeyboardButton('Кинотеатр', callback_data='cinema'))
    ikb.add(InlineKeyboardButton('Фитнес', callback_data='fitness'))
    ikb.add(InlineKeyboardButton('Ресторан', callback_data='restaurant'))
    ikb.add(InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))
    return ikb
