import datetime

from aiogram import executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram_calendar import SimpleCalendar, simple_cal_callback
from time import time, ctime

from keyboards import *
from database import *
from fsm import BookingRooms
from tools import *


@dp.message_handler(commands=['start', 'restart'])
async def start_command(message: types.Message):
    """функция-обработчик команды /start и /restart вне любых состояний машины конечных состояний"""
    global start_msg

    # отправка сообщения в чат пользователя
    # await позволяет выполнять команды асинхронно
    # reply_markup содержит клавиатуру, которая будет появляться сместе с этим сообщением
    start_msg = await message.answer(text='Добро пожаловать в Hotel_Telegram_KDA_Bot!\n' \
                                          'Для продолжения выберите одну из опций на клавиатуре:',
                                     reply_markup=get_start_kb())
    try:
        # удаление сообщения message
        await message.delete()
    except:
        pass


@dp.message_handler(commands=['start', 'restart'], state=BookingRooms)
async def restart_command(message: types.Message, state: FSMContext):
    """функция-обработчик команды /start и /restart в любых состояниях машины конечных состояний BookingRooms"""
    await state.reset_state()
    global start_msg
    start_msg = await message.answer(text='Регистрация в Hotel_Telegram_KDA_Bot прервана!\n' \
                                          'Для продолжения выберите одну из опций на клавиатуре:',
                                     reply_markup=get_start_kb())
    try:
        await message.delete()
    except:
        pass


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """функция-обработчик команды /help"""
    await message.reply(text=HELP_COMMAND, parse_mode='HTML')


@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    """Функция-обработчик команды /description"""
    await message.answer(text=DESCRIPTION)


@dp.message_handler(Text(equals='Бронь номеров'))
async def booking_rooms(message: types.Message):
    """
        Функция-обработчик текстовой команды "Бронь номеров".
        Эта функция является началом цепочки состояний машины конечных состояний BookingRooms,
        нужной для последовательного выполнения определенных команд для бронирования номеров
        и не позволяющей выполнять сторонние команды, не входящие в процесс бронирования номеров.
    """
    global start_msg
    try:
        await start_msg.delete()
    except:
        pass
    await bot.send_message(chat_id=message.chat.id,
                           text='Выберите категорию номера:',
                           reply_markup=get_room_category_ikb())

    # установка состояния choosing_room_category машины конечных состояний BookingRooms
    await BookingRooms.choosing_room_category.set()
    try:
        await message.delete()
    except:
        pass


@dp.callback_query_handler(state=BookingRooms.choosing_room_category)
async def choosing_room_category(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса полученного в результате нажатия на кнопку
        клавиатуры, созданной get_room_category_ikb()
    """
    # callback содержит множество данных
    # данные, отправляемые на сервер клавиатурой содержатся в data
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    else:
        # state.proxy() является памятью машины конечных состояний
        # здесь хранятся данные для каждого пользователя отдельно
        # разделение данных пользователей происходит автоматически
        async with state.proxy() as data:
            match callback.data:
                case 'standard':
                    # данные в state.proxy() хранятся в виде словаря python
                    data['room_type'] = 'standard'

                    # callback.answer вызывает временное всплывающее окно с введенным текстом
                    await callback.answer('Выбрана категория Standard')
                case 'studio':
                    data['room_type'] = 'studio'
                    await callback.answer('Выбрана категория Studio')
                case 'suite':
                    data['room_type'] = 'suite'
                    await callback.answer('Выбрана категория Suite')
                case 'deluxe':
                    data['room_type'] = 'deluxe'
                    await callback.answer('Выбрана категория Delux')

        # edit_text позволяет отредактировать сообщение
        await callback.message.edit_text('Выберите количество взрослых (старше 18 лет):',
                                         reply_markup=get_adult_num_ikb())

        # переход в следующее состояние BookingRooms
        await BookingRooms.next()


@dp.callback_query_handler(state=BookingRooms.choosing_adults_num)
async def choosing_adults_num(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии choosing_adults_num полученного
        в результате нажатия на кнопку клавиатуры, созданной get_room_category_ikb()
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    else:
        async with state.proxy() as data:
            match callback.data:
                case '1':
                    data['adults_num'] = 1
                    await callback.answer('1 взрослый')
                case '2':
                    data['adults_num'] = 2
                    await callback.answer('2 взрослых')
                case '3':
                    data['adults_num'] = 3
                    await callback.answer('3 взрослых')
                case '4':
                    data['adults_num'] = 4
                    await callback.answer('4 взрослых')

        await callback.message.edit_text('С вами будут дети (младше 18 лет)?',
                                         reply_markup=get_children_presense_ikb())
        await BookingRooms.next()


@dp.callback_query_handler(state=BookingRooms.choosing_children_presense)
async def choosing_children_presense(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии choosing_children_presense полученного
        в результате нажатия на кнопку клавиатуры, созданной get_children_presense_ikb()
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    else:
        async with state.proxy() as data:
            match callback.data:
                case 'да':
                    data['children_num'] = 0
                    data['children_presense'] = 'да'
                    await callback.answer('С детьми')
                    await callback.message.edit_text('Выберите количество детей:',
                                                     reply_markup=get_children_num_ikb())
                    await BookingRooms.next()
                case 'нет':
                    data['children_presense'] = 'нет'
                    data['children_num'] = 0
                    await callback.answer('Без детей')
                    await callback.message.edit_text('Чтобы проверить на вместимость, нажмите на кнопку',
                                                     reply_markup=get_check_capacity_ikb())
                    await BookingRooms.checking_capacity.set()


@dp.callback_query_handler(state=BookingRooms.choosing_children_num)
async def choosing_children_num(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии choosing_children_num полученного
        в результате нажатия на кнопку клавиатуры, созданной get_children_num_ikb()
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    else:
        async with state.proxy() as data:
            match callback.data:
                case '1':
                    data['children_num'] = 1
                    await callback.answer('1 ребенок')
                case '2':
                    data['children_num'] = 2
                    await callback.answer('2 ребенка')
                case '3':
                    data['children_num'] = 3
                    await callback.answer('3 ребенка')

            await callback.message.edit_text('Выберите возраст 1-го ребенка:\n',
                                             reply_markup=get_children_age_ikb())
            await BookingRooms.inputing_1_child_age.set()


@dp.callback_query_handler(state=BookingRooms.inputing_1_child_age)
async def choosing_1_child_age(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии inputing_1_child_age полученного
        в результате нажатия на кнопку клавиатуры, созданной get_children_age_ikb()
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    else:
        async with state.proxy() as data:
            match callback.data:
                case '0':
                    data[f'1_child'] = 0
                case '1':
                    data[f'1_child'] = 1
                case '2':
                    data[f'1_child'] = 2

        await callback.answer('возраст 1-го ребенка введен')
        if data['children_num'] > 1:
            await callback.message.edit_text('Выберите возраст 2-го ребенка:\n',
                                             reply_markup=get_children_age_ikb())
            await BookingRooms.next()
        else:
            await callback.message.edit_text('Чтобы проверить на вместимость, нажмите на кнопку',
                                             reply_markup=get_check_capacity_ikb())
            await BookingRooms.checking_capacity.set()


@dp.callback_query_handler(state=BookingRooms.inputing_2_child_age)
async def choosing_2_child_age(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии inputing_2_child_age полученного
        в результате нажатия на кнопку клавиатуры, созданной get_children_age_ikb()
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    else:
        async with state.proxy() as data:
            match callback.data:
                case '0':
                    data[f'2_child'] = 0
                case '1':
                    data[f'2_child'] = 1
                case '2':
                    data[f'2_child'] = 2

        await callback.answer('возраст 2-го ребенка введен')
        if data['children_num'] > 2:
            await callback.message.edit_text('Выберите возраст 3-го ребенка:\n',
                                             reply_markup=get_children_age_ikb())
            await BookingRooms.next()
        else:
            await callback.message.edit_text('Чтобы проверить на вместимость, нажмите на кнопку',
                                             reply_markup=get_check_capacity_ikb())
            await BookingRooms.checking_capacity.set()


@dp.callback_query_handler(state=BookingRooms.inputing_3_child_age)
async def choosing_3_child_age(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии inputing_3_child_age полученного
        в результате нажатия на кнопку клавиатуры, созданной get_children_age_ikb()
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    else:
        async with state.proxy() as data:
            match callback.data:
                case '0':
                    data[f'3_child'] = 0
                case '1':
                    data[f'3_child'] = 1
                case '2':
                    data[f'3_child'] = 2

        await callback.answer('Возраст 3-го ребенка введен')
        await callback.message.edit_text('Чтобы проверить на вместимость, нажмите на кнопку',
                                         reply_markup=get_check_capacity_ikb())
        await BookingRooms.next()


@dp.callback_query_handler(state=BookingRooms.checking_capacity)
async def check_room_capacity(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии checking_capacity полученного
        в результате нажатия на кнопку клавиатуры, созданной get_check_capacity_ikb()
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    else:
        async with state.proxy() as data:
            count = 0
            async with state.proxy() as data:
                for child in range(data['children_num']):
                    if data[f'{child + 1}_child'] != 0:
                        count += 1
                data['total_people'] = data['adults_num'] + count

            if check_capacity(data['room_type'], data['total_people']):
                await callback.message.edit_text('Номера с подхходящей вместительностью есть\nВыберите дату:',
                                                 reply_markup=await SimpleCalendar().start_calendar())
                await BookingRooms.choosing_date.set()
            else:
                await callback.message.edit_text('К сожалению нет номеров с подходящей вместительностью',
                                                 reply_markup=get_main_menu_ikb())
                await BookingRooms.lack_suitable_rooms.set()


@dp.callback_query_handler(state=BookingRooms.lack_suitable_rooms)
async def lack_suitable_rooms(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии lack_suitable_rooms
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)


@dp.callback_query_handler(simple_cal_callback.filter(), state=BookingRooms.choosing_date)
async def choosing_date(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии choosing_date полученного
        в результате нажатия на кнопку клавиатуры, созданной SimpleCalendar().start_calendar()
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    else:
        selected, date = await SimpleCalendar().process_selection(callback, callback_data)
        if selected:
            async with state.proxy() as data:
                data['day'] = int(date.strftime("%d"))
                data['month'] = int(date.strftime("%m"))
                data['year'] = int(date.strftime("%Y"))
                await callback.answer(f"Выбрана следующая дата: {data['day']}.{data['month']}.{data['year']}")

            await callback.message.edit_text(f"Выбрана следующая дата: {data['day']}.{data['month']}.{data['year']}",
                                             reply_markup=get_choosing_date_ikb())
            await BookingRooms.next()


@dp.callback_query_handler(state=BookingRooms.checking_rooms)
async def check_room(callback: types.CallbackQuery, state:FSMContext):
    """
        Функция-обработчик callback запроса в состоянии checking_rooms полученного
        в результате нажатия на кнопку клавиатуры, созданной get_choosing_date_ikb()
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    elif callback.data == 'yes':
        async with state.proxy() as data:
            if data['year'] >= int(datetime.datetime.now().year) \
                    and data['month'] >= int(datetime.datetime.now().month) \
                    and data['day'] >= int(datetime.datetime.now().day):
                data['all_occupied_rooms_id_in_date'] = []

                for room in get_all_occupied_room():
                    if room[1] == data['day'] and room[2] == data['month'] and room[3] == data['year']:
                        data['all_occupied_rooms_id_in_date'].append(room[0])

                data['free_rooms_id_by_type'] = get_free_rooms(data['all_occupied_rooms_id_in_date'], data['room_type'])

                if len(data['free_rooms_id_by_type']):
                    await callback.answer('Переходим к выбору номера')
                    await bot.send_photo(chat_id=callback.message.chat.id,
                                         photo=open('res/images/hotel_plan.png', 'rb'),
                                         caption='Выберите номер:',
                                         reply_markup=get_choosing_room_ikb(data['free_rooms_id_by_type']))
                    await BookingRooms.next()
                    await callback.message.delete()
                else:
                    await BookingRooms.choosing_date.set()
                    await callback.answer('Нет свободных номеров')
                    await callback.message.edit_text('К сожалению, в выбранную дату нет свободных номеров\n' \
                                                     'Выберите другую дату:',
                                                     reply_markup=await SimpleCalendar().start_calendar())
                return

    # if callback.data == 'no' or old date
    await BookingRooms.choosing_date.set()
    await callback.answer('Выберите другую дату')
    await callback.message.edit_text('Выберите другую дату:',
                                     reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(state=BookingRooms.choosing_room)
async def choose_room(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии choosing_room полученного
        в результате нажатия на кнопку клавиатуры, созданной get_choosing_room_ikb(data['free_rooms_id_by_type'])
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    else:
        await callback.message.delete()
        ph = await bot.send_photo(chat_id=callback.message.chat.id,
                                  photo=open(f'res/images/room_{callback.data}.png', 'rb'))
        await bot.send_message(chat_id=callback.message.chat.id,
                               text='Подтвердите выбор номера',
                               reply_markup=get_confirm_room_selection_ikb())
        await BookingRooms.next()
        async with state.proxy() as date:
            date['room_id'] = callback.data
            date['ph'] = ph.message_id


@dp.callback_query_handler(state=BookingRooms.confirm_room_selection)
async def confirm_room_selection(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии confirm_room_selection полученного
        в результате нажатия на кнопку клавиатуры, созданной get_confirm_room_selection_ikb()
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    elif callback.data == 'yes':
        await BookingRooms.checking_rooms.set()
        async with state.proxy() as data:
            await bot.delete_message(callback.message.chat.id, data['ph'])
            await check_room(callback, state)
    elif callback.data == 'this':
        async with state.proxy() as data:
            await bot.delete_message(callback.message.chat.id, data['ph'])
            await callback.message.edit_text(f'Стоимость проживания в этом номере составляет {get_room_cost_by_id(data["room_id"])[0]}₽\n' \
                                             'Продолжить?',
                                             reply_markup=get_authorization_ikb())
        await BookingRooms.next()


@dp.callback_query_handler(state=BookingRooms.authorization)
async def authorization(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии authorization полученного
        в результате нажатия на кнопку клавиатуры, созданной get_authorization_ikb()
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    elif callback.data == 'yes':
        await BookingRooms.checking_rooms.set()
        async with state.proxy() as data:
            await bot.delete_message(callback.message.chat.id, data['ph'])
            await check_room(callback, state)
    elif callback.data == 'auth':
        if user_in_db(callback.from_user.id):
            # сообщение для подтверждения оплаты
            #
            BookingRooms.payment.set()
        else:
            await callback.message.edit_text('Введите свою фамилию, имя и email через пробел:',
                                             reply_markup=get_main_menu_ikb())
            await BookingRooms.next()


@dp.message_handler(state=BookingRooms.user_data)
async def user_data(message: types.Message, state: FSMContext):
    """Функция-обработчик текстового сообщения, содержащего данные пользователя"""
    async with state.proxy() as data:
        data['surname'], data['name'], data['email'] = message.text.split()
        await bot.send_message(message.chat.id,
                               'Введите номер банковской карты (без пробелов):',
                               reply_markup=get_main_menu_ikb())
    await BookingRooms.next()


@dp.message_handler(state=BookingRooms.card_num)
async def card_num(message: types.Message, state: FSMContext):
    """Функция-обработчик текстового сообщения, содержащего номер карты"""
    async with state.proxy() as data:
        data['card_num'] = message.text
        await bot.send_message(message.chat.id,
                               'Введите срок действия банковской карты:',
                                reply_markup=get_main_menu_ikb())
    await BookingRooms.next()


@dp.message_handler(state=BookingRooms.card_date)
async def card_date(message: types.Message, state: FSMContext):
    """Функция-обработчик текстового сообщения, содержащего время действия карты"""
    async with state.proxy() as data:
        data['card_date'] = message.text
        await bot.send_message(message.chat.id,
                               'Введите имя держателя банковской карты:',
                                reply_markup=get_main_menu_ikb())
    await BookingRooms.next()


@dp.message_handler(state=BookingRooms.card_holders_name)
async def card_holders_name(message: types.CallbackQuery, state: FSMContext):
    """Функция-обработчик текстового сообщения, содержащего имя держателя карты"""
    async with state.proxy() as data:
        data['card_holders_name'] = message.text
        await bot.send_message(message.chat.id,
                               'Введите CVV-код банковской карты:',
                                reply_markup=get_main_menu_ikb())
    await BookingRooms.next()


@dp.message_handler(state=BookingRooms.card_cvv)
async def card_cvv(message: types.Message, state: FSMContext):
    """Функция-обработчик текстового сообщения, содержащего cvv"""
    async with state.proxy() as data:
        data['cvv'] = message.text
        await bot.send_message(message.chat.id,
                               'Проверьте данные банковской карты:\n'\
                                 f'{data["card_num"]}\n'\
                                 f'{data["card_date"]}\n'\
                                 f'{data["card_holders_name"]}\n'\
                                 f'{data["cvv"]}',
                                 reply_markup=get_card_check_ikb())
    await BookingRooms.next()


@dp.callback_query_handler(state=BookingRooms.card_check)
async def card_check(callback: types.CallbackQuery, state: FSMContext):
    """
        Функция-обработчик callback запроса в состоянии card_check полученного
        в результате нажатия на кнопку клавиатуры, созданной get_card_check_ikb()
    """
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    elif callback.data == 'false':
        await BookingRooms.card_num.set()
        await callback.message.edit_text('Введите номер банковской карты (без пробелов):',
                                         reply_markup=get_main_menu_ikb())
    elif callback.data == 'true':
        async with state.proxy() as data:
            DATA = [
                ["Date", "Name", "Volume", "Price (Rs.)"],
                [f"{data['day']}.{data['month']}.{data['year']}",
                 f"KDA Hotel {get_room_name(data['room_id'])} (room #{data['room_id']})",
                 "1 day",
                 f"{get_room_cost_by_id(data['room_id'])[0]}Rub"
                 ],
                ["Discount", "", "", "- 0"],
                ["Total", "", "", f"{get_room_cost_by_id(data['room_id'])[0]}Rub"]
            ]
            path = f"res/pdf/receipt_{str(data['day'])+str(data['month'])+str(data['year'])}_{data['room_id']}.pdf"
            pdf = SimpleDocTemplate(path, pagesize=A4)
            table = Table(DATA, style=style)
            pdf.build([title, table])

            await callback.message.delete()
            await bot.send_document(callback.message.chat.id,
                                    document=open(path, 'rb'),
                                    caption='Чек об оплате')


@dp.message_handler(Text(equals='Об отеле'))
async def about_hotel(message: types.Message):
    """Функция-обработчик текстовой команды "Об отеле" """
    # создание MediaGroup для отправки нескольких фотографий одним сообщением
    media = types.MediaGroup()
    media.attach_photo(types.InputFile('res/images/galery_2.jpeg'), 'Фасад здания отеля')
    media.attach_photo(types.InputFile('res/images/galery_4.jpeg'), 'Бассейн в фитнес зале')
    media.attach_photo(types.InputFile('res/images/galery_5.jpeg'), 'Кинотеатр')
    media.attach_photo(types.InputFile('res/images/galery_6.jpeg'), 'Холл')
    media.attach_photo(types.InputFile('res/images/galery_7.jpeg'), 'Вход в отель')
    media.attach_photo(types.InputFile('res/images/galery_8.jpeg'), 'Номер Standart')
    media.attach_photo(types.InputFile('res/images/galery_10.jpeg'), 'Номер Standart')
    media.attach_photo(types.InputFile('res/images/galery_12.jpeg'), 'Холл')
    media.attach_photo(types.InputFile('res/images/galery_13.jpeg'), 'Ресторан Borsalino')
    media.attach_photo(types.InputFile('res/images/galery_14.jpeg'), 'Холл')
    await bot.send_media_group(message.chat.id, media=media)
    await bot.send_message(message.chat.id, 'История «KDA-Hotel» насчитывает уже более полутора столетий. Находясь в самом сердце Санкт-Петербурга, отель был и остаётся свидетелем и участником исторических событий не только города, но и страны.'
                            '\n''Гостиница была основана на этом месте в 1840 году Наполеоном Бокиным и была известна под именем «Наполеон». Это было трехэтажное здание. В 1845-1846 архитектор Адриан Робен (1804-1872) реконструировал здание, которое стало четырехэтажным «Домом Поггенпола» с арендой квартир. В 1876 дом опять перестроили, и открылся отель «Шмидт-Англия», принадлежащий Терезе Шмидт (1800-1883) В 1911 и 1912 он был перестроен еще два раза. В 1911 году название отеля официально потеряло приставку «Шмидт» и в официальных документах значился как «владение наследников семьи Медем, хотя все еще принадлежал семье Шмидт. С 1911 по 1914 год отелем владела семья Шотте, благодаря которым, до наших дней дошли фотографии и документы тех лет. К 1917 году в отеле насчитывалось 75 номеров, и в городском путеводителе он значился как один из самых роскошных.',
                             reply_markup=get_main_menu_ikb())
    await message.delete()


@dp.message_handler(Text(equals='Дополнительные услуги'))
async def additional_services(message: types.Message):
    """Функция-обработчик текстовой команды "Дополнительные услуги" """
    await message.answer('В данном разделе вы можете ознакомиться с дополнительными сервисами, предоставляемые отелем',
                         reply_markup=get_additional_services())
    await message.delete()


@dp.callback_query_handler()
async def additional_services(callback: types.CallbackQuery):
    """
        Функция-обработчик callback запроса полученного
        в результате нажатия на кнопку клавиатуры, созданной get_additional_services()
    """
    if callback.data == "cinema":
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=open('res/images/cinema_angleter.jpg', 'rb'),
                             caption='Кинотеатр в отеле «KDA hotel» - это культурная площадка в самом центре' \
                                     'Санкт-Петербурга на Исаакиевской площади. Здесь демонстрируется фестивальное и' \
                                     'авторское кино, проходят трансляции балетных и оперных спектаклей, проводятся ' \
                                     'премьерные кинопоказы и творческие встречи с режиссерами и актерами.' \
                                     'Для бронирование мест обратитесь по телефону: +7(812)-996-16-66',
                             reply_markup=get_main_menu_ikb())
    elif callback.data == "fitness":
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=open('res/images/fitness.jpg', 'rb'),
                             caption='Фитнес-центр предлагает: тренажерный зал,оборудованный высокотехнологичными' \
                                     'тренажерами TechnoGym,две сауны и бассейн.\n' \
                                     'Посещение тренажерного зала,бассейна и сауны предоставляется' \
                                     'бесплатно всем гостям отеля.\n' \
                                     'Время работы: с 7:00-22:00.\n' \
                                     'Для бронирование мест обратитесь по телефону: +7(812)-996-16-66',
                             reply_markup=get_main_menu_ikb())
    elif callback.data == "restaurant":
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=open('res/images/borsalino_4.jpg', 'rb'),
                             caption='Ресторан Borsalino предлагает изысканный современный интерьер, непринужденную атмосферу,' \
                                     'внимательное обслуживание и великолепный вид на Исаакиевский собор.',
                             reply_markup=get_main_menu_ikb())
    elif callback.data == "main_menu":
        await start_command(callback.message)


@dp.message_handler(Text(equals='Контактная информация'))
async def contact_inf(message: types.Message):
    """Функция-обработчик текстовой команды "Контактная информацияи" """
    await message.answer('Отель «KDA Hotel»\nИсаакиевская пл.\nУл. Малая Морская 24\nСанкт-Петербург\n' \
                         '190000 Россия\nTel. +7(812)-996-16-66\nKDA_Hotel.spb@mail.ru',
                         reply_markup=get_main_menu_ikb())
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
