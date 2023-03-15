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

@dp.message_handler(commands=['reg'])
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
    await UserState.category.set()
@dp.message_handler(state=UserState.category)
async def get_category(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text) #Запись значения в email
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

@dp.callback_query_handler(lambda c: c.data in ['one', 'two', 'three', 'four', 'five', 'six', 'seven'], state=UserState.category)
async def process_category(callback_query: types.CallbackQuery, state: FSMContext):
    category = callback_query.data
    categories = {
        'one': 'Студенты',
        'two': 'Учащиеся общеобразоветельных учреждение 6-7 классы',
        'three': 'Учащиеся общеобразоветельных учреждение 8-11 классы',
        'four': 'Предпенсионеры',
        'five': 'Взрослое население/Работающий',
        'six': 'Работодатель',
        'seven': 'Все'
    }
    await state.update_data(category=categories[callback_query.data])
    await callback_query.answer(f"Вы выбрали целевую аудиторию: {category}")
    await UserState.age.set()
    # вызов следующего шага после выбора категории
    await callback_query.message.answer("Введите ваш возраст:")
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
