import bot
import asyncio
import logging

import config

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage #Хранилище состояний

dp = bot.dp

class UserState(StatesGroup):
    name = State()
    surname = State()
    email = State()
    number = State()
    age = State()
    categories = State()



@dp.message_handler(commands=['reg']) #
async def user_register(message: types.Message):
    await message.answer("Введите ваше имя")
    await UserState.name.set()

@dp.message_handler(state=UserState.name)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text) #Запись значения в name
    await message.answer("Введите вашу фамилию.")
    await UserState.surname.set()  # либо же UserState.adress.set()

@dp.message_handler(state=UserState.email)
async def get_email(message: types.Message, state: FSMContext):

    await state.update_data(email=message.text)


@dp.message_handler(state=UserState.surname)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    data = await state.get_data()
    await message.answer(f"Имя: {data['name']}\n"
                         f"Фамилия: {data['surname']}")

    await state.finish()

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
