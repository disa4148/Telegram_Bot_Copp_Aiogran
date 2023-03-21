import bot
import json
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types, filters
from aiogram.dispatcher.filters.state import StatesGroup, State

dp = bot.dp
@dp.callback_query_handler(lambda call: True)
async def pagination_func(callback: types.CallbackQuery, n=-1):
    with open('Events.json', encoding='utf-8') as f:
        data = f.read()
        categories = json.loads(data)
        cat = 0
        for i in categories['content']:
            if i['begin']:
                cat = 1 + cat

    req = callback.data.split('_')
    # Обработка кнопки - скрыть
    if req[0] == 'unseen':
         await callback.message.delete()
# Обработка кнопок - вперед и назад
    elif 'pagination' in req[0]:
        i = categories['content']

        # Расспарсим полученный JSON
        json_string = json.loads(req[0])
        count = json_string['CountPage']
        page = json_string['NumberPage']
        # Пересоздаем markup
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        # markup для первой страницы
        if page == 1:
            markup.add(types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       types.InlineKeyboardButton(text=f'Вперёд --->',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page + 1) + ",\"CountPage\":" + str(count) +"}"))
        # markup для второй страницы
        elif page == count:
            markup.add(types.InlineKeyboardButton(text=f'<--- Назад',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page - 1) + ",\"CountPage\":" + str(count) + "}"),
                       types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))
        # markup для остальных страниц
        else:
            markup.add(types.InlineKeyboardButton(text=f'<--- Назад',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page - 1) + ",\"CountPage\":" + str(count) + "}"),
                       types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       #types.InlineKeyboardButton(text=f'Вперёд --->',
                       #                     callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                       #                         page + 1) + ",\"CountPage\":" + str(count) + "}"))
                        types.InlineKeyboardButton(text=f'Вперёд --->',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page + 1) + ",\"CountPage\":" + str(count) + "}"))

            await callback.message.edit_text(f"{i[page]['image']['name']}\n"+
                                             f"{i[page]['name']}\n"+
                                             f"Целевая аудитория: {i[page]['targetGroup']['name']}\n"+
                                             f"Тип курса: {i[page]['type']['name']}\n"+
                                             f"Почта: {i[page]['speakerEmail']}\n"+
                                             f"Телефон для связи: {i[page]['speakerPhone']}\n"+
                                             f"Начало: {i[page]['begin'][3]}:{i[page]['begin'][4]}  Дата:{i[page]['begin'][2]}.{i[page]['begin'][1]}.{i[page]['begin'][0]}", reply_markup=markup, parse_mode='html')
        #await callback.message.edit_text("Наши мероприятия:\n" + " ", reply_markup=markup)
#Для пагнинации


