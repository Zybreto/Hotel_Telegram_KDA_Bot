import sqlite3

from config import *

"""
users table:
___________________________________________________________________
|   tg_id   |      surname    |     name     |     patronymic     |
|-----------|-----------------|--------------|--------------------|
| 123456789 | example_surname | example_name | example_patronymic |
|   ....    |       ...       |      ...     |        ...         |
-------------------------------------------------------------------


bank_cards table:
___________________________________________________________________________________________________________
|   tg_id   |  card_name   |    card_number   |  holders_name  |   validity_month   | validity_year | cvv |
|-----------|--------------|------------------|----------------|--------------------|---------------------|
| 123456789 | example_name | 1234123412341234 | example_h_name |   example_month    | example_year  | 123 |
|    ...    |     ...      |       ...        |      ...       |        ...         |      ...      | ... |
-----------------------------------------------------------------------------------------------------------


room_condition table:
____________________________________________________________
| room_id | occupancy_status | entry_date | departure_date |
|---------|------------------|------------|----------------|
|   123   |         1        | 12.01.2022 |   15.01.2022   |
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


def create_table(name: str, columns: str):
    """создает таблицу с названием name и столбцами columns, если ее нет в БД"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name}({columns})""")


def _commit():
    """сохраняет изменения в БД"""
    db.commit()


def close():
    """закрывает БД"""
    db.close()


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


def add_new_bank_card(tg_id: int, card_number: int, holders_name: str, validity_month: int, validity_year: int, cvv: int):
    """производит проверку на наличие card_number, в случае его отсутствия создает карту с таким card_number,
       иначе ничего не происходит"""
    if (card_number, ) in _get_all_card_numbers():
        return
    cursor.execute("""INSERT INTO bank_cards (tg_id, card_number, holders_name, validity_month, validity_year, cvv) VALUES(?, ?, ?, ?, ?, ?)""",
                   (tg_id, card_number, holders_name, validity_month, validity_year, cvv))
    _commit()
    return 1


def get_user_cards(tg_id):
    """возвращает кортежи вида (card_name, card_number) по tg_id"""
    cursor.execute("""SELECT card_name, card_number FROM bank_cards WHERE tg_id == ?""", (tg_id, ))
    return cursor.fetchall()


def del_bank_card(card_name):
    """удаляет данные карты по card_name"""
    cursor.execute("""DELETE FROM bank_cards WHERE card_name == ?""", (card_name, ))
    _commit()
