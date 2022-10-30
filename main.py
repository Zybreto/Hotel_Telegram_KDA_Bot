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
    global start_msg
    start_msg = await message.answer(text='Добро пожаловать в Hotel_Telegram_KDA_Bot!\n' \
                                          'Для продолжения выберите одну из опций на клавиатуре:',
                                     reply_markup=get_start_kb())
    try:
        await message.delete()
    except:
        pass


@dp.message_handler(commands=['start', 'restart'], state=BookingRooms)
async def restart_command(message: types.Message, state: FSMContext):
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
    await message.reply(text=HELP_COMMAND, parse_mode='HTML')  # написать сообщение HELP_COMMAND


@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    await message.answer(text=DESCRIPTION)


@dp.message_handler(Text(equals='Бронь номеров'))
async def booking_rooms(message: types.Message):
    global start_msg
    try:
        await start_msg.delete()
    except:
        pass
    await bot.send_message(chat_id=message.chat.id,
                           text='Выберите категорию номера:',
                           reply_markup=get_room_category_ikb())
    await BookingRooms.choosing_room_category.set()
    try:
        await message.delete()
    except:
        pass


@dp.callback_query_handler(state=BookingRooms.choosing_room_category)
async def choosing_room_category(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    else:
        async with state.proxy() as data:
            match callback.data:
                case 'standard':
                    data['room_type'] = 'standard'
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

        await callback.message.edit_text('Выберите количество взрослых (старше 18 лет):',
                                         reply_markup=get_adult_num_ikb())
        await BookingRooms.next()


@dp.callback_query_handler(state=BookingRooms.choosing_adults_num)
async def choosing_adults_num(callback: types.CallbackQuery, state: FSMContext):
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
                    await callback.message.edit_text('Проверка вместимости',
                                                     reply_markup=get_check_capacity_ikb())
                    await BookingRooms.checking_capacity.set()


@dp.callback_query_handler(state=BookingRooms.choosing_children_num)
async def choosing_children_num(callback: types.CallbackQuery, state: FSMContext):
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
            await callback.message.edit_text('Проверка вместимости',
                                             reply_markup=get_check_capacity_ikb())
            await BookingRooms.checking_capacity.set()


@dp.callback_query_handler(state=BookingRooms.inputing_2_child_age)
async def choosing_2_child_age(callback: types.CallbackQuery, state: FSMContext):
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
            await callback.message.edit_text('Проверка вместимости',
                                             reply_markup=get_check_capacity_ikb())
            await BookingRooms.checking_capacity.set()


@dp.callback_query_handler(state=BookingRooms.inputing_3_child_age)
async def choosing_3_child_age(callback: types.CallbackQuery, state: FSMContext):
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
        await callback.message.edit_text('Проверка вместимости',
                                         reply_markup=get_check_capacity_ikb())
        await BookingRooms.next()


@dp.callback_query_handler(state=BookingRooms.checking_capacity)
async def check_room_capacity(callback: types.CallbackQuery, state: FSMContext):
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
                await callback.message.edit_text('Выберите дату:',
                                                 reply_markup=await SimpleCalendar().start_calendar())
                await BookingRooms.choosing_date.set()
            else:
                await callback.message.edit_text('К сожалению нет номеров с подходящей вместительностью',
                                                 reply_markup=get_main_menu_ikb())
                await BookingRooms.lack_suitable_rooms.set()


@dp.callback_query_handler(state=BookingRooms.lack_suitable_rooms)
async def lack_suitable_rooms(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)


@dp.callback_query_handler(simple_cal_callback.filter(), state=BookingRooms.choosing_date)
async def choosing_date(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
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
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    elif callback.data == 'yes':
        async with state.proxy() as data:
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
            else:
                await BookingRooms.choosing_date.set()
                await callback.answer('Нет свободных номеров')
                await callback.message.edit_text('К сожалению, в выбранную дату нет свободных номеров\n' \
                                                 'Выберите другую дату:',
                                                 reply_markup=await SimpleCalendar().start_calendar())
    elif callback.data == 'no':
        await BookingRooms.choosing_date.set()
        await callback.answer('Выберите другую дату')
        await callback.message.edit_text('Выберите другую дату:',
                                         reply_markup=await SimpleCalendar().start_calendar())
    await callback.message.delete()


@dp.callback_query_handler(state=BookingRooms.choosing_room)
async def choose_room(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)













@dp.message_handler(Text(equals='Ресторан'))
async def restaurant(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo=open('res/images/borsalino_4.jpg', 'rb'))
    await message.answer('Ресторан Borsalino предлагает изысканный современный интерьер, непринужденную атмосферу,' \
                         'внимательное обслуживание и великолепный вид на Исаакиевский собор.',
                         reply_markup=get_start_kb())
    await message.delete()


@dp.message_handler(Text(equals='Об отеле'))
async def about_hotel(message: types.Message):
    await message.answer('В данном разделе вы можете ознакомиться с дополнительными сервисами, предоставляемые отелем',
                         reply_markup=get_info_about_hotel())


@dp.callback_query_handler()
async def about_hotel_cinema(callback: types.CallbackQuery):
    if callback.data == "cinema":
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=open('res/images/cinema_angleter.jpg', 'rb'),
                             caption='Кинотеатр в отеле «KDA hotel» - это культурная площадка в самом центре' \
                                     'Санкт-Петербурга на Исаакиевской площади. Здесь демонстрируется фестивальное и' \
                                     'авторское кино, проходят трансляции балетных и оперных спектаклей, проводятся ' \
                                     'премьерные кинопоказы и творческие встречи с режиссерами и актерами.' \
                                     'Для бронирование мест обратитесь по телефону: +7(812)-996-16-66')
    elif callback.data == "fitness":
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=open('res/images/fitness.jpg', 'rb'),
                             caption='Фитнес-центр предлагает: тренажерный зал,оборудованный высокотехнологичными' \
                                     'тренажерами TechnoGym,две сауны и бассейн.\n' \
                                     'Посещение тренажерного зала,бассейна и сауны предоставляется' \
                                     'бесплатно всем гостям отеля.\n' \
                                     'Время работы: с 7:00-22:00.\n' \
                                     'Для бронирование мест обратитесь по телефону: +7(812)-996-16-66')
    elif callback.data == "main_menu":
        await start_command(callback.message)


@dp.message_handler(Text(equals='Контактная информация'))
async def contact_inf(message: types.Message):
    await message.answer('Отель «KDA Hotel»\nИсаакиевская пл.\nУл. Малая Морская 24\nСанкт-Петербург\n' \
                         '190000 Россия\nTel. +7(812)-996-16-66\nKDA_Hotel.spb@mail.ru',
                         reply_markup=get_start_kb())
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
