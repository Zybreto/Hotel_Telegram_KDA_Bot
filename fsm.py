from aiogram.dispatcher.filters.state import StatesGroup, State


class BookingRooms(StatesGroup):
    choosing_room_category = State()  # состояние выбора категории номера
    choosing_adults_num = State()  # состояние выбора кол-ва взрослых
    choosing_children_presense = State()  # состояние выбора наличия детей

    choosing_children_num = State()  # состояние выбора кол-ва детей
    inputing_children_age = State()  # состояние выбора возраста детей

    choosing_dates = State()  # состояние выбора даты заселения
    payment = State()  # состояние оплаты
