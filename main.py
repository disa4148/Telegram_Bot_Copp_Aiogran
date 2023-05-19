import bot
import asyncio
import re
import xlsxwriter
import logging
import navigation
import CreateExcelTable
import EmailSender


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
    user_status = State()

@dp.message_handler(commands=['reg']) #Процедура регистрации
async def user_register(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше имя")
    await UserState.name.set()

@dp.message_handler(state=UserState.name)
async def get_name(message: types.Message, state: FSMContext): #Получение
    if (len(message.text)) >= 2:
        if (len(message.text)) < 20:
            if any(char.isdigit() for char in message.text):
                await message.answer("Имя не должно содержат цифр\n\n Попробуйте ввести ещё раз")
            else:
                await state.update_data(name=message.text)  # Запись значения в name
                await message.answer("Введите вашу фамилию")
                await UserState.surname.set()  # либо же UserState.adress.set()
        else:
            await message.answer("Имя слишком длинное\n\n Попробуйте ввести ещё раз")
    else:
        await message.answer("Имя слишком короткое\n\n Попробуйте ввести ещё раз")

@dp.message_handler(state=UserState.surname)
async def get_surname(message: types.Message, state: FSMContext): #Ф-ция фамилии
    if (len(message.text)) >= 2:
        if (len(message.text)) < 60:
            if any(char.isdigit() for char in message.text):
                await message.answer('Фамилия не должна содержать цифр, попробуйте ввести ещё раз')
            else:
                await state.update_data(surname=message.text) # Запись значения surname
                await message.answer("Введите адрес эл. почты")
                await UserState.email.set()

        else:
            await message.answer("Фамилия слишком длинная\n\n Попробуйте ввести ещё раз")
    else:
        await message.answer('Фамилия слишком короткая, попробуйте ввести ещё раз')

@dp.message_handler(state=UserState.email)
async def get_number(message: types.Message, state: FSMContext):
    email_validate_pattern = r"^\S+@\S+\.\S+$"
    if bool(re.match(email_validate_pattern, message.text)) == True:
        await state.update_data(email=message.text) #Запись значения email
        await message.answer("Введите номер телефона:")
        await UserState.category.set()
    else:
        await message.answer("Введите корректные данные")

@dp.message_handler(state=UserState.category)
async def get_category(message: types.Message, state: FSMContext):
    pattern = re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', message.text)

    if (bool(pattern)) == True:
        await state.update_data(number=message.text) #Запись значения в number
        keyboard_cat = types.InlineKeyboardMarkup(row_width=1)
        categories = {
            'Студенты': '1',
            'Учащиеся общеобразоветельных учреждений 6-7 классы': '2',
            'Учащиеся общеобразоветельных учреждений 8-11 классы': '3',
            'Предпенсионеры': '4',
            'Взрослое население/Работающий': '5',
            'Работодатель': '6',
            'Все': '7'
        }
        for category, data in categories.items():
            keyboard_cat.add(types.InlineKeyboardButton(text=category, callback_data=data))
        await message.answer("Выберите целевую аудиторию:", reply_markup=keyboard_cat)
    else:
        await message.answer("Введите корректные данные")
    #await message.answer("Выберите целевую аудиторию гражданина:")


@dp.callback_query_handler(lambda c: c.data in ['1', '2', '3', '4', '5', '6', '7'], state=UserState.category)
async def process_category(callback_query: types.CallbackQuery, state: FSMContext):
    category = callback_query.data
    categories = {
        '1': 'Студенты',
        '2': 'Учащиеся общеобразоветельных учреждение 6-7 классы',
        '3': 'Учащиеся общеобразоветельных учреждение 8-11 классы',
        '4': 'Предпенсионеры',
        '5': 'Взрослое население/Работающий',
        '6': 'Работодатель',
        '7': 'Все'
    }

    await state.update_data(category=categories[callback_query.data]) #Запись значения в category
    await callback_query.answer(f"Вы выбрали целевую аудиторию: {category}")
    await UserState.age.set()
    # вызов следующего шага после выбора категории
    await callback_query.message.answer("Введите ваш возраст:")

@dp.message_handler(state=UserState.age)
async def get_age(message: types.Message, state: FSMContext):
    builder = types.InlineKeyboardMarkup(inline_keyboard=True, row_width=2)
    builder.add(types.InlineKeyboardButton(text="Да ✅", callback_data='reg_confirm'))
    builder.add(types.InlineKeyboardButton(text="Нет ❌", callback_data='reg_deviation'))

    await state.update_data(age=message.text) #Запись значения в age
    data = await state.get_data()
    await message.answer(f"Проверьте, корректно ли заполнены поля?  💬\n\n"
                         f"Имя: <b>{data['name']}</b>\n"
                         f"Фамилия: <b>{data['surname']}</b>\n"
                         f"Эл. почта: <b>{data['email']}</b>\n"
                         f"Номер телефона: <b>{data['number']}</b>\n"
                         f"Возраст: <b>{data['age']}</b>\n"
                         f"Категория: <b>{data['category']}</b>",
                         parse_mode='html',
                         reply_markup=builder
                         )
    #await state.finish
    await UserState.user_status.set()

@dp.callback_query_handler(lambda c: c.data == 'reg_confirm' or c.data == 'reg_deviation', state=UserState.user_status)
async def process_callback_reg_confirm(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'reg_confirm':
        us = UserState()
        await state.update_data(user_status='authorized')
        await callback_query.message.answer('Все успешно заполнено 👏 \n\nВы можете ознакомиться с курсами с помощью команды <b> /course </b>', parse_mode='html')
        data = await state.get_data()
        CreateExcelTable.InsertTable(data)
        await state.finish()

    elif callback_query.data == 'reg_deviation':
            await state.update_data(user_status='unauthorized')
            data = await state.get_data()
            await callback_query.message.answer('Нажми кнопку <b>"/reg"</b> для возврата назад', parse_mode='html')
            await state.finish()
# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)
try:
    if __name__ == "__main__":
        print('Bot is working!!!')
        asyncio.run(main())
except:
    print('Не работает...')
