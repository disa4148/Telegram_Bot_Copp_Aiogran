import bot
import asyncio
import re
import logging

import config

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types, filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage #Хранилище состояний

dp = bot.dp

class UserState(StatesGroup):
    name = State()
    surname = State()
    email = State()
    number = State()
    age = State()
    category = State()



@dp.message_handler(commands=['reg']) #
async def user_register(message: types.Message):
    await message.answer("Введите ваше имя")
    await UserState.name.set()

@dp.message_handler(state=UserState.name)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text) #Запись значения в surname
    await message.answer("Введите вашу фамилию.")
    #await UserState.next()
    await UserState.surname.set()

@dp.message_handler(state=UserState.surname)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Введите email адрес.")
    await UserState.email.set()


@dp.message_handler(state=UserState.email)
async def get_result(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text) #Запись значения в email
    await message.answer("Введите свой номер телефона:")
    #await UserState.next()
    await UserState.number.set()

@dp.message_handler(state=UserState.number)
async def get_result(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text) #Запись значения в email
    await message.answer("Введите свой возраст")
    await UserState.category.set()

@dp.message_handler(state=UserState.category)
async def get_category(message: types.Message):
    keyboard_cat = types.InlineKeyboardMarkup(row_width=1)
    categories = {
        'Студенты': 'one',
        'Учащиеся общеобразоветельных учреждений 6-7 классы': 'two',
        'Учащиеся общеобразоветельных учреждений 8-11 классы': 'three',
        'Предпенсионеры': 'four',
        'Взрослое население/Работающий': 'five',
        'Работодатель': 'six',
        'Все': 'seven'
    }
    for category, data in categories.items():
        keyboard_cat.add(types.InlineKeyboardButton(text=category, callback_data=data))
    await message.answer("Выберите целевую аудиторию:", reply_markup=keyboard_cat)



@dp.callback_query_handler(filters.Text(startswith="cat_"))
async def callback_reply(callback: types.CallbackQuery, state: FSMContext):
    if callback:
        categories = {
            'one': 'Студенты',
            'two': 'Учащиеся общеобразоветельных учреждение 6-7 классы',
            'three': 'Учащиеся общеобразоветельных учреждение 8-11 классы',
            'four': 'Предпенсионеры',
            'five': 'Взрослое население/Работающий',
            'six': 'Работодатель',
            'seven': 'Все'
        }
        if callback in categories:
            state.update_data(category=categories[callback])  # Запись значения в email
            await UserState.age.set()



@dp.message_handler(state=UserState.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text) #Запись значения в email
    data = await state.get_data()
    await message.answer(f"Проверьте, корректно ли заполнены поля?\n\n"
                         f"Имя: {data['name']}\n"
                         f"Фамилия: {data['surname']}\n"
                         f"Эл. почта: {data['email']}\n"
                         f"Номер телефона: {data['number']}\n"
                         f"Возраст: {data['age']}\n"
                         f"Категория: {data['category']}"
                         )
    await state.finish()


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
