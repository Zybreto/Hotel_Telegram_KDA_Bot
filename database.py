import sqlite3

from config import *

"""
users table:
___________________________________________________________________
|   tg_id   |      surname    |     name     |        email       |
|-----------|-----------------|--------------|--------------------|
| 123456789 | example_surname | example_name |    example_email   |
|   ....    |       ...       |      ...     |        ...         |
-------------------------------------------------------------------


bank_cards table:
___________________________________________________________________________________________________________
|   tg_id   |  card_holders_name   |    card_number   |  holders_name  |   validity_month   | validity_year | cvv |
|-----------|--------------|------------------|----------------|--------------------|---------------------|
| 123456789 | example_name | 1234123412341234 | example_h_name |   example_month    | example_year  | 123 |
|    ...    |     ...      |       ...        |      ...       |        ...         |      ...      | ... |
-----------------------------------------------------------------------------------------------------------


occupied_rooms table:
____________________________________________________________
| room_id |        day       |    month   |      year      |
|---------|------------------|------------|----------------|
|   123   |         1        |      12    |      2022      |
|   ...   |        ...       |     ...    |      ...       |
------------------------------------------------------------


room_characteristics table:
_______________________________________________________________________________________________
| room_id | room_type | room_cost | single_beds_num | double_beds_num | sofas_num | additions |
|---------|-----------|-----------|-----------------|-----------------|-----------------------|
|   123   | standard  |    1234   |        2        |         0       |     0     | some_text |
|   ...   |    ...    |    ...    |       ...       |        ...      |    ...    |    ...    |
-----------------------------------------------------------------------------------------------
"""


db = sqlite3.connect(database_path)
cursor = db.cursor()


# функции общего назначения
def create_table(name: str, columns: str):
    """создает таблицу с названием name и столбцами columns, если ее нет в БД"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name}({columns})""")


def _commit():
    """сохраняет изменения в БД"""
    db.commit()


def close():
    """закрывает БД"""
    db.close()


# работа с таблицей users
def _get_all_tg_id():
    """возвращает кортеж со всеми tg_id из таблицы users"""
    cursor.execute("""SELECT tg_id FROM users""")
    return cursor.fetchall()


def _get_all_card_numbers():
    """возвращает кортеж со всеми card_number из таблицы bank_cards"""
    cursor.execute("""SELECT card_number FROM bank_cards""")
    return cursor.fetchall()


def create_user(tg_id: int, surname: str, name: str, patronymic: str):
    """производит проверку на наличие tg_id, в случае его отсутствия создает пользователя с таким tg_id,
       иначе ничего не происходит"""
    if (tg_id,) in _get_all_tg_id():
        return
    cursor.execute("""INSERT INTO users (tg_id, surname, name, patronymic) VALUES(?, ?, ?, ?)""",
                   (tg_id, surname, name, patronymic))
    _commit()
    return 1


def del_user(tg_id: int):
    """удаляет данные пользователя из таблиц users и данные его карты из bank_cards"""
    cursor.execute("""DELETE FROM users WHERE tg_id == ?""", (tg_id, ))
    cursor.execute("""DELETE FROM bank_cards WHERE tg_id == ?""", (tg_id, ))
    _commit()


def user_in_db(tg_id: int):
    return 1 if (tg_id,) in _get_all_tg_id() else 0


# работа с таблицей bank_cards
def add_bank_card(tg_id: int, card_number: int, holders_name: str, validity_month: int, validity_year: int, cvv: int):
    """производит проверку на наличие card_number, в случае его отсутствия создает карту с таким card_number,
       иначе ничего не происходит"""
    if (card_number, ) in _get_all_card_numbers():
        return
    cursor.execute("""INSERT INTO bank_cards (tg_id, card_number, holders_name, validity_month, validity_year, cvv) VALUES(?, ?, ?, ?, ?, ?)""",
                   (tg_id, card_number, holders_name, validity_month, validity_year, cvv))
    _commit()
    return 1


def get_user_cards(tg_id):
    """возвращает кортежи вида (card_holders_name, card_number) по tg_id"""
    cursor.execute("""SELECT card_holders_name, card_number FROM bank_cards WHERE tg_id == ?""", (tg_id, ))
    return cursor.fetchall()


def del_bank_card(card_name):
    """удаляет данные карты по card_holders_name"""
    cursor.execute("""DELETE FROM bank_cards WHERE card_holders_name == ?""", (card_name, ))
    _commit()


# работа с room_condition
def add_occupied_room(room_id: int, day: int, month: int, year: int):
    """добавляет данные по состоянию номера"""
    cursor.execute("""INSERT INTO occupied_rooms (room_id, day, month, year) VALUES(?, ?, ?, ?)""",
                   (room_id, day, month, year))
    _commit()


def get_all_occupied_room():
    """возвращает данные по состоянию всех номеров"""
    cursor.execute("""SELECT * FROM occupied_rooms""")
    return cursor.fetchall()


def get_occupied_rooms(room_id):
    cursor.execute("""SELECT * FROM occupied_rooms WHERE room_id == ?""",
                   (room_id, ))
    return cursor.fetchall()


# работа с room_characteristics
def add_room_characteristics(room_id: int, room_name: str, room_type: str, capacity: int, room_cost: int, single_beds_num: int, double_beds_num: int, sofas_num: int, additions: str):
    """добавляет характеристики номеров"""
    cursor.execute("""INSERT INTO room_characteristics (room_id, room_name, room_type, capacity, room_cost, single_beds_num, double_beds_num, sofas_num, additions) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (room_id, room_name, room_type, capacity, room_cost, single_beds_num, double_beds_num, sofas_num, additions))
    _commit()


def get_room_characteristics(room_id: int):
    """возвращает характеристики номера по room_id"""
    cursor.execute("""SELECT * FROM room_characteristics WHERE room_id == ?""",
                   (room_id, ))
    return cursor.fetchone()


def get_room_name(room_id):
    cursor.execute("""SELECT room_name FROM room_characteristics WHERE room_id == ?""",
                   (room_id,))
    return cursor.fetchone()[0]


def get_rooms_id():
    cursor.execute("""SELECT room_id FROM room_characteristics""")
    return cursor.fetchall()


def get_rooms_id_by_type(room_type: str):
    cursor.execute("""SELECT room_id FROM room_characteristics WHERE room_type == ?""",
                   (room_type, ))
    return cursor.fetchall()


def get_room_id_by_capacity(room_type: str, capacity: int):
    cursor.execute("""SELECT room_id FROM room_characteristics WHERE room_type == ? AND capacity >= ?""",
                   (room_type, capacity))
    return cursor.fetchall()


def get_room_cost_by_id(room_id: int):
    cursor.execute("""SELECT room_cost FROM room_characteristics WHERE room_id == ?""",
                   (room_id, ))
    return cursor.fetchone()


def get_hotel_specs(hotel_id: int):
    cursor.execute("""SELECT address, phone_num, email FROM hotel_specs WHERE hotel_id == ?""", (hotel_id, ))
    return cursor.fetchone()


def get_hotels_num():
    hotels = cursor.execute("""SELECT hotel_id FROM hotel_specs""").fetchall()
    return len(hotels)
