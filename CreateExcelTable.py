import pandas as pd
import xlsxwriter
import EmailSender
from datetime import datetime

addr_to = "denis.nikolaenko.2004@mail.ru"
file_path = 'C:/Users/14/Desktop/Collected_info_user.xlsx'

def InsertTable(data):
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
        existing_data = pd.read_excel(file_path)
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    except FileNotFoundError:
        # Если файл не существует, создаем DataFrame только с новыми данными
        combined_data = new_data

    # Сохранение комбинированных данных в Excel-файл
    combined_data.to_excel(file_path, index=False)

    files = [file_path]

    EmailSender.send_email(addr_to, "Test Exel", "А вот и текст:)", files)  # Почта находится в файле ForEmail.py
