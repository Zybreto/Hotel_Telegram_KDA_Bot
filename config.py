from aiogram import  Bot, Dispatcher


TOKEN = r'5765828718:AAG3tElzqDgFiObtA5pEZhkQrdtyc83Ffk0'  # авторизационный токен для взаимодействия с API Telegram

bot = Bot(TOKEN)
dp = Dispatcher(bot)  # Dispatcher осуществляет анализ и обработку входящих обновлений бота
database_path = 'res/DB/database.db'

HELP_COMMAND = """
<b>/start</b> - <em>начать работу с ботом</em>
<b>/help</b> - <em>список команд</em>
<b>/description</b> - <em>описание возможностей бота</em>
<b>/report</b> - <em>содержание отчета</em>
<b>/tasks</b> - <em>список задач разработчиков бота</em>
<b>/edit_task dev task</b> - <em>изменение задачи разработчика</em>"""

DESCRIPTION = """
описание возможностей бота
ля ля ля
ля ля
ля"""

