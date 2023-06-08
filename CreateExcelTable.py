import pandas as pd
import xlsxwriter
import EmailSender
from datetime import datetime

addr_to = "denis.nikolaenko.2004@mail.ru"
file_path_user = 'CollectedData/Collected_info_user.xlsx'
file_path_event = "CollectedData/Collected_info_events.xlsx"
data_new = pd.DataFrame()
def Insert_Table(numer,data1):
    global data_new
    if numer == 1:
        data_new = pd.DataFrame({
            'Имя': [data1['name'].strip()],
            'Фамилия': [data1['surname'].strip()],
            'Номер телефона': [data1['number'].strip()],
            'Адрес эл. почты': [data1['email'].strip()],
            'Возраст': [str(data1['age']).strip()],
            'Аудитория': [data1['category'].strip()],
            'Время создания заявки': [data1['time'].strip()]
        })
        print(data_new)
    if numer == 1:
        def InsertTable_User(data):
            # Создание нового DataFrame с новыми данными
            new_data = pd.DataFrame({
                'Имя': [data['name']],
                'Фамилия': [data['surname']],
                'Номер телефона': [data['number']],
                'Адрес эл. почты': [data['email']],
                'Возраст': [data['age']],
                'Аудитория': [data['category']],
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
        InsertTable_User(data1)



    else:
        print(data_new)
        def InsertTable_Events(data,data_new):
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
            data_new = data_new.reset_index(drop=True)
            new_data = new_data.reset_index(drop=True)
            new_data = pd.concat([new_data,data_new], ignore_index=False, axis=1)
            print(new_data)
            # Чтение существующего файла, если он существует
            try:
                existing_data = pd.read_excel(file_path_event)
                combined_data = pd.concat([new_data, existing_data], ignore_index=True)
            except:
            # Если файл не существует, создаем DataFrame только с новыми данными
                combined_data = new_data

            # Сохранение комбинированных данных в Excel-файл
            combined_data.to_excel(file_path_event, index=False)

        InsertTable_Events(data1,data_new)
