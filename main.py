from aiogram import executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from time import time, ctime

from keyboards import *
from database import *
from fsm import BookingRooms


@dp.message_handler(commands=['start', 'restart'])
async def start_command(message: types.Message):
    await message.answer(text='Добро пожаловать в Hotel_Telegram_KDA_Bot!\n'\
                              'Для продолжения выберите одну из опций на клавиатуре:',
                         reply_markup=get_start_kb())
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND, parse_mode='HTML')  # написать сообщение HELP_COMMAND


@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    await message.answer(text=DESCRIPTION)


@dp.message_handler(Text(equals='Бронь номеров'))
async def booking_rooms(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Выберите категорию номера:',
                           reply_markup=get_room_category_ikb())
    await BookingRooms.choosing_room_category.set()
    await message.delete()


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
                    data['room_category'] = 'standard'
                    await callback.answer('Выбрана категория Standard')
                case 'studio':
                    data['room_category'] = 'studio'
                    await callback.answer('Выбрана категория Studio')
                case 'suite':
                    data['room_category'] = 'suite'
                    await callback.answer('Выбрана категория Suite')
                case 'delux':
                    data['room_category'] = 'delux'
                    await callback.answer('Выбрана категория Delux')

        await callback.message.edit_text('Выберите количество взрослых:', reply_markup=get_people_num_ikb())
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
                    data['adults_num'] = '1'
                    await callback.answer('1 взрослый')
                case '2':
                    data['adults_num'] = '2'
                    await callback.answer('2 взрослых')
                case '3':
                    data['adults_num'] = '3'
                    await callback.answer('3 взрослых')
                case '4':
                    data['adults_num'] = '4'
                    await callback.answer('4 взрослых')

    await callback.message.edit_text('С вами будут дети?', reply_markup=get_children_presense_ikb())
    await BookingRooms.next()


@dp.callback_query_handler(state=BookingRooms.choosing_children_presense)
async def choosing_adults_num(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'main_menu':
        await callback.answer('Возвращаемся в главное меню')
        await state.finish()
        await start_command(callback.message)
    else:
        async with state.proxy() as data:
            match callback.data:
                case 'да':
                    data['children_presense'] = 'да'
                    await callback.answer('С детьми')

                    await callback.message.edit_text('Выберите количество детей:',
                                                     reply_markup=get_people_num_ikb())
                    await BookingRooms.next()
                case 'нет':
                    data['children_presense'] = 'нет'
                    await callback.answer('Без детей')

                    await callback.message.edit_text('Далее следует выбор даты бронирования номера.\n'\
                                                     'Сначала нужно выбрать год, затем месяц и число.\n'\
                                                     'Выберите год:',
                                                     reply_markup=get_choosing_dates_ikb())
                    await BookingRooms.choosing_dates.set()


@dp.message_handler(Text(equals='Ресторан'))
async def restaurant(message: types.Message):
    await message.answer('ресторан',
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals='Об отеле'))
async def about_hotel(message: types.Message):
    await message.answer('об отеле',
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals='Контактная информация'))
async def contact_inf(message: types.Message):
    await message.answer('контакты',
                         reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
