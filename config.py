TOKEN = r'5765828718:AAG3tElzqDgFiObtA5pEZhkQrdtyc83Ffk0'  # авторизационный токен для взаимодействия с API Telegram

database_path = 'res/DB/database.db'

users_columns = 'tg_id INTEGER,' \
                'surname TEXT,' \
                'name TEXT,' \
                'patronymic TEXT'

bank_cards_columns = 'tg_id INTEGER,' \
                     'card_number INTEGER,' \
                     'holders_name TEXT,' \
                     'validity_month INTEGER,' \
                     'validity_year INTEGER,' \
                     'cvv INTEGER'

room_condition_columns = 'room_id INTEGER,' \
                          'occupancy_status INTEGER,' \
                          'entry_date timestamp,' \
                          'departure_date timestamp'

room_characteristics_columns = 'room_id INTEGER,' \
                               'room_type TEXT,' \
                               'room_cost INTEGER,' \
                               'single_beds_num INTEGER,' \
                               'double_beds_num INTEGER,' \
                               'sofas_num INTEGER,' \
                               'additions TEXT'
