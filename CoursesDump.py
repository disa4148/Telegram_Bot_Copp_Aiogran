import json
import bot
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

dp = bot.dp

# Загружаем данные из файла JSON
def load_data_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data['content']
    except Exception as e:
        print("Произошла ошибка при загрузке данных из JSON:", str(e))
        return []

# Получаем имя курса по его идентификатору
def get_course_name_by_id(course_id, content):
    try:
        for item in content:
            if str(item['id']) == course_id:
                return item['name']
        return None
    except Exception as e:
        print("Произошла ошибка при получении имени курса по идентификатору:", str(e))
        return None

def get_course(course_direction, cource_target_audience, cource):
    try:
        result = {"content": []}
        for item in cource:
            if course_direction == str(item["type"]):
                result["content"].append(item)
        return result
    except Exception as e:
        print("Произошла ошибка при получении курса:", str(e))
        return {"content": []}

# Обработчик команды /course
@dp.message_handler(commands=['course'])
async def start_work(message: types.Message):
    try:
        msg = await message.answer(
            "Выберите интересующее вас направление курса  🙌\n\n" "❗Исходя из выбранного направления вам будут предложены соответствующие программы")

        content = load_data_from_json('groupCourses.json')

        current_page = 1
        index = current_page - 1

        if index >= len(content):
            await message.answer("Вы посмотрели все категории курсов. 🚫\n\n"
                                 "Для просмотра прошлых категорий курсов нажмите кнопку 'Назад' ⬅")
            return

        item = content[index]
        id = item['id']
        name = item['name']
        image_name = item['image']['name']
        image_src = item['image']['src']

        message_text = f"ID: {id}\n"
        message_text += f"Название направления: {name}\n"

        keyboard = InlineKeyboardMarkup(row_width=2)
        prev_button = InlineKeyboardButton("Назад", callback_data="prev_page")
        next_button = InlineKeyboardButton("Вперёд", callback_data="next_page")
        choose_button = InlineKeyboardButton("Выбрать направление", callback_data=f"choose_course_{id}")
        keyboard.row(prev_button, next_button)
        keyboard.add(choose_button)

        await message.answer_photo(photo=image_src, caption=message_text, reply_markup=keyboard)
    except Exception as e:
        print("Произошла ошибка при обработке команды /course:", str(e))

# Обработчик нажатия кнопки "Назад"
@dp.callback_query_handler(text_contains='prev_page')
async def handle_prev_page(callback_query: types.CallbackQuery):
    try:
        current_page = int(callback_query.message.caption.split()[1])
        current_page -= 1
        await update_course_info(callback_query.message, current_page)
    except Exception as e:
        print("Произошла ошибка при обработке нажатия кнопки 'Назад':", str(e))

# Обработчик нажатия кнопки "Вперёд"
@dp.callback_query_handler(text_contains='next_page')
async def handle_next_page(callback_query: types.CallbackQuery):
    try:
        current_page = int(callback_query.message.caption.split()[1])
        current_page += 1
        await update_course_info(callback_query.message, current_page)
    except Exception as e:
        print("Произошла ошибка при обработке нажатия кнопки 'Вперёд':", str(e))

# Обработчик выбора курса
@dp.callback_query_handler(lambda c: c.data.startswith('choose_course_'))
async def handle_choose_course(callback_query: types.CallbackQuery):
    try:
        course_id = callback_query.data.split('_')[-1]
        content = load_data_from_json('groupCourses.json')
        find_courses = load_data_from_json('courses.json')
        course_name = get_course_name_by_id(course_id, content)
        await callback_query.answer(f"Вы выбрали курс: {course_name}")
        keyboard = InlineKeyboardMarkup(row_width=1)
        prev_button = InlineKeyboardButton("Назад", callback_data='course')
        keyboard.row(prev_button)

        line = ""
        all_courses = get_course(course_name, 0, find_courses)
        for element in all_courses['content']:
            line = line + f'✅ <b>{element["name"]}</b>\n<em>Направление курса: {element["type"]}\nЦелевая аудитория: {element["target_audience"]}</em>\n\n'

        await callback_query.message.answer("Курсы от ЦОППа!:\n\n" + line, parse_mode='html', reply_markup=keyboard)
    except Exception as e:
        print("Произошла ошибка при обработке выбора курса:", str(e))

@dp.callback_query_handler(text_contains='course')
async def go_back_course(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.delete()
    except Exception as e:
        print("Произошла ошибка при обработке нажатия кнопки 'Назад' (курсы):", str(e))

# Функция обновления информации о курсе
async def update_course_info(message: types.Message, current_page: int):
    try:
        content = load_data_from_json('groupCourses.json')

        index = current_page - 1

        if index >= len(content):
            await message.answer("Вы посмотрели все категории курсов. 🚫\n\n"
                                 "Для просмотра прошлых категорий курсов нажмите кнопку 'Назад' ⬅")
            return

        item = content[index]
        id = item['id']
        name = item['name']
        image_name = item['image']['name']
        image_src = item['image']['src']

        message_text = f"ID: {id}\n"
        message_text += f"Название курса: {name}\n"

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
    except Exception as e:
        print("Произошла ошибка при обновлении информации о курсе (слишком много запросов):", str(e))
