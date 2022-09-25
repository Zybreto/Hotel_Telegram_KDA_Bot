import sqlite3

from config import database_path


class Database:
    def __init__(self):
        self.db = sqlite3.connect(database_path)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.close()

    def create_table(self, table_name, table_columns):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}({table_columns})""")

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()


class Users(Database):
    """
    ___________________________________________________________________
    |   tg_id   |      surname    |     name     |     patronymic     |
    |-----------|-----------------|--------------|--------------------|
    | 123456789 | example_surname | example_name | example_patronymic |
    |   ....    |       ...       |      ...     |        ...         |
    -------------------------------------------------------------------
    """

    def __init__(self):
        super().__init__()

        self.table_name = 'users'
        self.table_columns = 'tg_id INTEGER,' \
                             'surname TEXT,' \
                             'name TEXT,' \
                             'patronymic TEXT'

        self.create_table(self.table_name, self.table_columns)

    def create_user(self):
        ...


class BankCards(Database):
    """
    ____________________________________________________________________________________________
    |   tg_id   |    card_number   |  holders_name  |   validity_month   | validity_year | cvv |
    |-----------|------------------|----------------|--------------------|---------------------|
    | 123456789 | 1234123412341234 | example_h_name |   example_month    | example_year  | 123 |
    |    ...    |       ...        |      ...       |        ...         |      ...      | ... |
    --------------------------------------------------------------------------------------------
    """

    def __init__(self):
        super().__init__()

        self.table_name = 'bank_cards'
        self.table_columns = 'tg_id INTEGER,' \
                             'card_number INTEGER,' \
                             'holders_name TEXT,' \
                             'validity_month INTEGER,' \
                             'validity_year INTEGER,' \
                             'cvv INTEGER'

        self.create_table(self.table_name, self.table_columns)


class RoomCondition(Database):
    """
    ____________________________________________________________
    | room_id | occupancy_status | entry_date | departure_date |
    |---------|------------------|------------|----------------|
    |   123   |         1        | 12.01.2022 |   15.01.2022   |
    |   ...   |        ...       |     ...    |      ...       |
    ------------------------------------------------------------
    """

    def __init__(self):
        super().__init__()

        self.table_name = 'room_condition'
        self.table_columns = 'room_id INTEGER,' \
                             'occupancy_status INTEGER,' \
                             'entry_date timestamp,' \
                             'departure_date timestamp'

        self.create_table(self.table_name, self.table_columns)


class RoomCharacteristics(Database):
    """
    _______________________________________________________________________________________________
    | room_id | room_type | room_cost | single_beds_num | double_beds_num | sofas_num | additions |
    |---------|-----------|-----------|-----------------|-----------------|-----------------------|
    |   123   | standard  |    1234   |        2        |         0       |     0     | some_text |
    |   ...   |    ...    |    ...    |       ...       |        ...      |    ...    |    ...    |
    -----------------------------------------------------------------------------------------------
    """

    def __init__(self):
        super().__init__()

        self.table_name = 'room_characteristics'
        self.table_columns = 'room_id INTEGER,' \
                             'room_type TEXT,' \
                             'room_cost INTEGER,' \
                             'single_beds_num INTEGER,' \
                             'double_beds_num INTEGER,' \
                             'sofas_num INTEGER,' \
                             'additions TEXT'

        self.create_table(self.table_name, self.table_columns)
