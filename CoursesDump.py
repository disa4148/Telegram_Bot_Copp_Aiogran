import json
import bot
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

dp = bot.dp

# Загружаем данные из файла JSON
def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['content']

# Получаем имя курса по его идентификатору
def get_course_name_by_id(course_id, content):
    for item in content:
        if str(item['id']) == course_id:
            return item['name']
    return None

# Обработчик команды /course
@dp.message_handler(commands=['course'])
async def start_work(message: types.Message):
    await message.answer("Выберите интересующий вас курс:")

    content = load_data_from_json('courses.json')

    current_page = 1
    index = current_page - 1

    if index >= len(content):
        await message.answer("Страница не существует.")
        return

    item = content[index]
    id = item['id']
    name = item['name']
    image_name = item['image']['name']
    image_src = item['image']['src']

    message_text = f"ID: {id}\n"
    message_text += f"Название курса: {name}\n"
    message_text += f"Имя изображения: {image_name}\n"

    keyboard = InlineKeyboardMarkup(row_width=2)
    prev_button = InlineKeyboardButton("Назад", callback_data="prev_page")
    next_button = InlineKeyboardButton("Вперёд", callback_data="next_page")
    choose_button = InlineKeyboardButton("Выбрать курс", callback_data=f"choose_course_{id}")
    keyboard.row(prev_button, next_button)
    keyboard.add(choose_button)

    await message.answer_photo(photo=image_src, caption=message_text, reply_markup=keyboard)

# Обработчик нажатия кнопки "Назад"
@dp.callback_query_handler(text_contains='prev_page')
async def handle_prev_page(callback_query: types.CallbackQuery):
    current_page = int(callback_query.message.caption.split()[1])
    current_page -= 1
    await update_course_info(callback_query.message, current_page)

# Обработчик нажатия кнопки "Вперёд"
@dp.callback_query_handler(text_contains='next_page')
async def handle_next_page(callback_query: types.CallbackQuery):
    current_page = int(callback_query.message.caption.split()[1])
    current_page += 1
    await update_course_info(callback_query.message, current_page)

# Обработчик выбора курса
@dp.callback_query_handler(lambda c: c.data.startswith('choose_course_'))
async def handle_choose_course(callback_query: types.CallbackQuery):
    course_id = callback_query.data.split('_')[-1]
    content = load_data_from_json('courses.json')
    course_name = get_course_name_by_id(course_id, content)
    await callback_query.answer(f"Вы выбрали курс: {course_name}")

# Функция обновления информации о курсе
async def update_course_info(message: types.Message, current_page: int):
    content = load_data_from_json('courses.json')

    index = current_page - 1

    if index >= len(content):
        await message.answer("Страница не существует.")
        return

    item = content[index]
    id = item['id']
    name = item['name']
    image_name = item['image']['name']
    image_src = item['image']['src']

    message_text = f"ID: {id}\n"
    message_text += f"Название курса: {name}\n"
    message_text += f"Имя изображения: {image_name}\n"

    keyboard = InlineKeyboardMarkup(row_width=2)
    prev_button = InlineKeyboardButton("Назад", callback_data="prev_page")
    next_button = InlineKeyboardButton("Вперёд", callback_data="next_page")
    choose_button = InlineKeyboardButton("Выбрать курс", callback_data=f"choose_course_{id}")
    keyboard.row(prev_button, next_button)
    keyboard.add(choose_button)

    # Получаем новый URL из JSON
    new_image_src = item['image']['src']

    # Изменяем изображение, используя новый URL
    await message.edit_media(types.InputMediaPhoto(media=new_image_src, caption=message_text), reply_markup=keyboard)

if __name__ == '__main__':
    bot.start_polling()
