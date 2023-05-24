import bot
import json
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types, filters
from aiogram.types import ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup

dp = bot.dp

@dp.message_handler(commands=['start']) #Cтарт бота
async def start_work(message: types.Message):

    await message.answer("Добро пожаловать в телеграмм бот ЦОПП Кузбасса!\n\n" +
    "Мы занимаемся:\n\n" +
    "✅ Выявлением наиболее востребованных в регионе профессий;\n\n" +
    "✅ Разработкой единых подходов к образовательным программам для всех категорий граждан;\n\n" +
    "✅ Содействием центрам занятости в поиске соискателей для актуальных вакансий; \n\n" +
    "✅ Информированием работодателей и работников о проектах рынка труда;\n\n"+
    "✅ Защитой интеллектуальной собственности;\n\n"+
    "✅ Организацией и проведением профориентационных работ в регионе;\n\n"+
    "✅ Вопросами международного сотрудничества;\n\n"+
    "✅ Организацией и проведением деловых встреч и мероприятий")
    await get_menu(message)



@dp.message_handler(commands=['menu']) # Менюшка
async def get_menu(message: types.Message):
    menu = types.InlineKeyboardMarkup(inline_keyboard=True)
    menu.add(types.InlineKeyboardButton(text="Записаться на курс 👨‍💻", callback_data='menu_course'))
    menu.add(types.InlineKeyboardButton(text="Наши контакты 🌍", callback_data='menu_contacts'))
    await message.answer("Выберите для продолжения", reply_markup=menu)

@dp.message_handler(commands=['help'])
async def get_help(message: types.Message):
    await message.answer("Список доступных команд: 🙏\n\n"
                         "👉 start - Запуск бота\n"
                         "👉 menu - Главное меню\n"
                         "👉 reg - Запуск процедуры регистрации\n"
                         "👉 course - Список курсов\n"
                         "👉 events - Список мероприятий\n")

@dp.callback_query_handler(filters.Text(startswith="menu_")) #Обработка обратной связи кнопок меню
async def go_to_courses(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    if action == "course":
        await callback.message.answer("Для записи на курс необходимо пройти регистрацию \n\n"
                                      "Зарегистрироваться можно здесь: <b>https://platform.copp42.ru/registration</b>\n\n"
                                      "‼️ <b> Для регистрации в Telegram напишите /reg ‼</b>", parse_mode="html")

    elif action == "contacts":
        menu = types.InlineKeyboardMarkup(inline_keyboard=True)
        menu.add(types.InlineKeyboardButton(text="Вызов меню ⚡", callback_data='return_menu'))
        await callback.message.answer('Контакты: \n\n' +
                                      "📍 650021, г.Кемерово, ул.Павленко, 1а\n\n" +
                                      "📞 +7 (3842) 57-11-20 \n📞 +7 (3842) 57-11-14\n\n" +
                                      "✉  copp42@yandex.ru\n\n" +
                                      "Режим работы:\n\n" +
                                      "Пн-Пт 8:30-17:00\nСб 8:30-14:00\nВс-выходной\n" +
                                      "Социальные сети: \n\n" +
                                      "Вконтакте: \nhttps://vk.com/copp42kuzbass \n\n" +
                                      "Одноклассники: \nhttps://ok.ru/copp42kuzbass \n\n" +
                                      "Telegram канал: \nhttps://t.me/copp42 \n\n" +
                                      "Youtube канал: \n\nhttps://www.youtube.com/channel/UCn2HyuY_HBUy9L75sqx0qcw",
                                      parse_mode='html', reply_markup=menu)
        @dp.callback_query_handler(lambda c: c.data == 'return_menu')
        async def return_to_menu(callback: types.CallbackQuery):
            if callback.data == "return_menu":
                await get_menu(callback.message)

