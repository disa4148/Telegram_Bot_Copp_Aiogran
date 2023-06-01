import aiogram.types
import bot
import json
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types, filters
from aiogram.dispatcher.filters.state import StatesGroup, State

dp = bot.dp




@dp.callback_query_handler(text_contains='confirm_on_event')
async def confirm_on_event_func(callback: types.CallbackQuery):
    await callback.message.answer("Вы записаны!")
@dp.message_handler(commands=['events'])
async def get_course(message: types.Message, state: FSMContext):
    try:
        status = await state.get_data()
        with open('events.json', encoding='utf-8') as f:
            data = f.read()
            categories = json.loads(data)
            cat = 0
            for i in categories['content']:
                if i['begin']:
                    cat = 1 + cat

        i = categories['content']
        count = cat
        page = 0
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Записаться', callback_data='unseen'))
        markup.add(types.InlineKeyboardButton(text=f'{page + 1}/{count}', callback_data=f' '),
                   types.InlineKeyboardButton(text=f'Вперёд --->',
                                              callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                  page + 1) + ",\"CountPage\":" + str(count) + "}"))
        await message.answer_photo(open(i[page]['image']['src'], 'rb'),caption=f"{i[page]['name']}\n" +
                             f"Целевая аудитория: {i[page]['targetGroup']['name']}\n" +
                             f"Тип курса: {i[page]['type']['name']}\n" +
                             f"Почта: {i[page]['speakerEmail']}\n" +
                             f"Телефон для связи: {i[page]['speakerPhone']}\n" +
                             f"Начало: {i[page]['begin'][3]}:{i[page]['begin'][4]}  Дата:{i[page]['begin'][2]}.{i[page]['begin'][1]}.{i[page]['begin'][0]}",
                                   reply_markup=markup, parse_mode='html')
    except Exception as e:
        print(f"An error occurred in get_course: {str(e)}")



@dp.callback_query_handler(lambda call: True)
async def pagination_func(callback: types.CallbackQuery, n=-1):
   # try:
        with open('events.json', encoding='utf-8') as f:
            data = f.read()
            categories = json.loads(data)
            cat = 0
            for i in categories['content']:
                if i['begin']:
                    cat = 1 + cat


        i = categories['content']

        req = callback.data.split('_')

        # Обработка кнопки - скрыть
        if req[0] == 'unseen':

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Записаться', callback_data='confirm_on_event'))
            # await callback.message.edit_media(
            #     media=aiogram.types.InputMedia(type='photo', media=open(i[page]['image']['src'], 'rb'),
            #     caption=f"Вы хотите записаться на:\n{i[page]['name']}\n\n" +
            #    f"Целевая аудитория: {i[page]['targetGroup']['name']}\n\n" +
            #    f"Тип курса: {i[page]['type']['name']}\n\n" +
            #    f"Почта: {i[page]['speakerEmail']}\n\n" +
            #    f"Телефон для связи: {i[page]['speakerPhone']}\n\n" +
            #    f"Начало: {i[page]['begin'][3]}:{i[page]['begin'][4]}  Дата:{i[page]['begin'][2]}.{i[page]['begin'][1]}.{i[page]['begin'][0]}"+
            #    f"\n‼️Внимание, при записи на курс, вы даёте согласие на обработку персональных данных, которые были записаны при регистрации",
            # ), reply_markup=markup)
            await callback.message.answer("Вы точно хотите записаться?", reply_markup=markup)
            print(req[0])

    # Обработка кнопок - вперед и назад
        elif 'pagination' in req[0]:

            # Расспарсим полученный JSON
            json_string = json.loads(req[0])
            count = json_string['CountPage']
            page = json_string['NumberPage']


            # Пересоздаем markup
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Записаться', callback_data='unseen'))
            # markup для первой страницы

            #photo = open('C:/Users/12/PycharmProjects/Telegram_Bot_Copp_Aiogran/photos/ej.jpg', 'rb')
            if page == 0:
                markup.add(types.InlineKeyboardButton(text=f'{page + 1}/{count}', callback_data=f' '),
                           types.InlineKeyboardButton(text=f'Вперёд --->',
                                                callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                    page + 1) + ",\"CountPage\":" + str(count) +"}"))
                await callback.message.edit_media(media=aiogram.types.InputMedia(type='photo', media=open(i[page]['image']['src'], 'rb'),
                                                 caption=f"{i[page]['name']}\n\n" +
                                                 f"Целевая аудитория: {i[page]['targetGroup']['name']}\n\n" +
                                                 f"Тип курса: {i[page]['type']['name']}\n\n" +
                                                 f"Почта: {i[page]['speakerEmail']}\n\n" +
                                                 f"Телефон для связи: {i[page]['speakerPhone']}\n\n" +
                                                 f"Начало: {i[page]['begin'][3]}:{i[page]['begin'][4]}  Дата:{i[page]['begin'][2]}.{i[page]['begin'][1]}.{i[page]['begin'][0]}",
                                                 ), reply_markup=markup)
            # markup для второй страницы
            elif page+1 == count:
                markup.add(types.InlineKeyboardButton(text=f'<--- Назад',
                                                callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                    page - 1) + ",\"CountPage\":" + str(count) + "}"),
                           types.InlineKeyboardButton(text=f'{page+1}/{count}', callback_data=f' '))
                await callback.message.edit_media(media=aiogram.types.InputMedia(type='photo', media=open(i[page]['image']['src'], 'rb'),
                                                 caption=f"{i[page]['name']}\n\n" +
                                                 f"Целевая аудитория: {i[page]['targetGroup']['name']}\n\n" +
                                                 f"Тип курса: {i[page]['type']['name']}\n\n" +
                                                 f"Почта: {i[page]['speakerEmail']}\n\n" +
                                                 f"Телефон для связи: {i[page]['speakerPhone']}\n\n" +
                                                 f"Начало: {i[page]['begin'][3]}:{i[page]['begin'][4]}  Дата:{i[page]['begin'][2]}.{i[page]['begin'][1]}.{i[page]['begin'][0]}",
                                                 ), reply_markup=markup)
            # markup для остальных страниц
            else:
                markup.add(types.InlineKeyboardButton(text=f'<--- Назад',
                                                      callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                          page - 1) + ",\"CountPage\":" + str(count) + "}"),
                           types.InlineKeyboardButton(text=f'{page+1}/{count}', callback_data=f' '),
                           types.InlineKeyboardButton(text=f'Вперёд --->',
                                                      callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                          page + 1) + ",\"CountPage\":" + str(count) + "}"))

                await callback.message.edit_media(media=aiogram.types.InputMedia(type='photo', media=open(i[page]['image']['src'], 'rb'),
                                                                                 caption = f"{i[page]['name']}\n\n"+
                                                 f"Целевая аудитория: {i[page]['targetGroup']['name']}\n\n"+
                                                 f"Тип курса: {i[page]['type']['name']}\n\n"+
                                                 f"Почта: {i[page]['speakerEmail']}\n\n"+
                                                 f"Телефон для связи: {i[page]['speakerPhone']}\n\n"+
                                                 f"Начало: {i[page]['begin'][3]}:{i[page]['begin'][4]}  Дата:{i[page]['begin'][2]}.{i[page]['begin'][1]}.{i[page]['begin'][0]}",
                                                  )
                                                  ,reply_markup=markup)
    # except Exception as e:
    #     print(e)




# Сделай обработку ошибок и исключений try-except для каждой функции и условия

