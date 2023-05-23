import xlsxwriter
import EmailSender
import datetime
from datetime import datetime
addr_to = "denis.nikolaenko.2004@mail.ru"



def InsertTable(data):
    Collected_Data = (['Имя', data['name']], ['Фамилия', data['surname']],
                      ['Номер телефона', data['number']],
                      ['Адрес эл. почты', data['email']],
                      ['Возраст', data['age']],
                      ['Целевая аудитория', data['category']]
                      ['Дата отправки', datetime.datetime.now().strftime("%d-%m-%Y %H:%M")])
    workbook = xlsxwriter.Workbook('C:/Users/14/Desktop/Collected_info_user.xlsx')
    worksheet = workbook.add_worksheet("Лист 1")

    for i, (item, information) in enumerate(Collected_Data, start=1):  # Создание Exel таблицы
        worksheet.write(f'A{i}', item)
        worksheet.write(f'B{i}', information)
    workbook.close()

    files = ["C:/Users/14/Desktop/Collected_info_user.xlsx"]

    EmailSender.send_email(addr_to, "Test Exel", "А вот и текст:)", files)  # Почта находится в файле ForEmail.py

# await state.finish()