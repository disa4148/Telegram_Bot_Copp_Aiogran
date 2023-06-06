import pandas as pd
import xlsxwriter
import EmailSender
from datetime import datetime

addr_to = "denis.nikolaenko.2004@mail.ru"
file_path_user = 'CollectedData/Collected_info_user.xlsx'
file_path_event = "CollectedData/Collected_info_events.xlsx"

def InsertTable_Events(data):
    # Создание нового DataFrame с новыми данными

    # Получаем данные из словаря состояния
    collection = data.get('collection')

    new_data = pd.DataFrame({
        "Название мероприятия": collection.get('name'),
        "Целевая аудитория": collection.get('targetGroup'),
        "Типо курса":  collection.get('type'),
        "Почта организатора": collection.get('speakerEmail'),
        "Телефон огранизатора": collection.get('speakerPhone'),
        "Дата проведения": collection.get('begin_time'),
        "Начало": collection.get('begin_data')
    })
    # Чтение существующего файла, если он существует
    try:
        existing_data = pd.read_excel(file_path_event)
        combined_data = pd.concat([new_data, existing_data], ignore_index=True)
    except:
    # Если файл не существует, создаем DataFrame только с новыми данными
        combined_data = new_data

    # Сохранение комбинированных данных в Excel-файл
    combined_data.to_excel(file_path_event, index=False)

def InsertTable_User(data):
    # Создание нового DataFrame с новыми данными
    new_data = pd.DataFrame({
        'Имя': [data['name']],
        'Фамилия': [data['surname']],
        'Номер телефона': [data['number']],
        'Адрес эл. почты': [data['email']],
        'Возраст': [data['age']],
        'Целевая аудитория': [data['category']],
        'Время создания заявки': [data['time']]
    })

    try:
        # Чтение существующего файла, если он существует
        existing_data = pd.read_excel(file_path_user)
        combined_data = pd.concat([new_data, existing_data], ignore_index=True)
    except FileNotFoundError:
        # Если файл не существует, создаем DataFrame только с новыми данными
        combined_data = new_data

    # Сохранение комбинированных данных в Excel-файл
    combined_data.to_excel(file_path_user, index=False)

    files = [file_path_user]

    EmailSender.send_email(addr_to, "Test Exel", "А вот и текст:)", files)  # Почта находится в файле ForEmail.py
