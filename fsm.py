from aiogram.dispatcher.filters.state import StatesGroup, State


class BookingRooms(StatesGroup):
    choosing_room_category = State()  # состояние выбора категории номера
    choosing_adults_num = State()  # состояние выбора кол-ва взрослых
    choosing_children_presense = State()  # состояние выбора наличия детей

    choosing_children_num = State()  # состояние выбора кол-ва детей

    lack_suitable_rooms = State()  # отсутствие подходящих номеров

    inputing_1_child_age = State()  # состояние выбора возраста 1го ребенка
    inputing_2_child_age = State()  # состояние выбора возраста 2го ребенка
    inputing_3_child_age = State()  # состояние выбора возраста 3го ребенка

    choosing_date = State()  # состояние выбора даты заселения
    payment = State()  # состояние оплаты
