from aiogram.dispatcher.filters.state import StatesGroup, State


class BookingRooms(StatesGroup):
    choosing_room_category = State()  # состояние выбора категории номера
    choosing_adults_num = State()  # состояние выбора кол-ва взрослых
    choosing_children_presense = State()  # состояние выбора наличия детей

    choosing_children_num = State()  # состояние выбора кол-ва детей
    inputing_1_child_age = State()  # состояние выбора возраста 1го ребенка
    inputing_2_child_age = State()  # состояние выбора возраста 2го ребенка
    inputing_3_child_age = State()  # состояние выбора возраста 3го ребенка

    checking_capacity = State()  # проверка вместимости

    lack_suitable_rooms = State()  # отсутствие подходящих номеров

    choosing_date = State()  # состояние выбора даты заселения
    checking_rooms = State()  # проверка номеров
    choosing_room = State()  # выбор номера
    confirm_room_selection = State()  # подтверждение выбора номера
    authorization = State()  # авторизация пользователя
    user_data = State()  # данные пользователя
    card_num = State()  # номер банковской карты
    card_date = State()  # срок действия банковской карты
    card_holders_name = State()  # имя держателя банковской карты
    card_cvv = State()  # cvv банковской карты
    card_check = State()  # проверка данных банковской карты

    payment = State()  # состояние оплаты
