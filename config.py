from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


TOKEN = r'5765828718:AAG3tElzqDgFiObtA5pEZhkQrdtyc83Ffk0'  # авторизационный токен для взаимодействия с API Telegram

storage = MemoryStorage()  # память для хранения состояний пользователей
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)  # Dispatcher осуществляет анализ и обработку входящих обновлений бота
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


# payment receipt
# creating a Base Document Template of page size A4
# pdf = SimpleDocTemplate("res/pdf/receipt.pdf", pagesize=A4)

# standard stylesheet defined within reportlab itself
styles = getSampleStyleSheet()

# fetching the style of Top level heading (Heading1)
title_style = styles["Heading1"]

# 0: left, 1: center, 2: right
title_style.alignment = 1

# creating the paragraph with
# the heading text and passing the styles of it
title = Paragraph("KDA_Hotel", title_style)

# creates a Table Style object and in it,
# defines the styles row wise
# the tuples which look like coordinates
# are nothing but rows and columns
style = TableStyle(
    [
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("GRID", (0, 0), (4, 4), 1, colors.black),
        ("BACKGROUND", (0, 0), (3, 0), colors.gray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ]
)
