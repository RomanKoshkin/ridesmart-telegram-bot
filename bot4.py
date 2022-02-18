# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

import random, pymongo, datetime, time, json, requests
from multiprocessing import Process
from bs4 import BeautifulSoup
import numpy as np

import telegram
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton


# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
myclient = pymongo.MongoClient("mongodb+srv://XXXXXXXXXXX@XXXXXXXXXXXX")
mydb = myclient["mydatabase"]# create a db in the client
mycol = mydb["customers"]      # create a collection in the db

def disengageOld(string):
    """
    THIS FUNCTION LAUNCHES A BACKGROUND PROCESS THAT POLLS THE DATABASE FOR USERS THAT WERE ENGAGED
    MORE THAN A MINUTE AGO AND ARE MARKED AS ENGAGED, AND DISENGAGES THEM SO THAT THEY BECOME VISIBLE TO OTHER
    USERS.
    """
    while True:
        myclient = pymongo.MongoClient("mongodb+srv://XXXXXXXXXXX@XXXXXXXXXXXX")
        mydb = myclient["mydatabase"]# create a db in the client
        mycol = mydb["customers"]      # create a collection in 
        
        # disengage entries that are one minute old
        offset = datetime.timedelta(minutes=1)
        now = datetime.datetime.now()
        t = now - offset
        myquery = {'engaged': True, 'updated': {'$lt': t} }
        newvalues = { "$set": { "engaged": False }}
        x = mycol.update_many(myquery, newvalues)
        
        # delete entries that are overdue more than 5 minutes
        offset = datetime.timedelta(minutes=1)
        now = datetime.datetime.now()
        t = now - offset
        myquery = {'time': {'$lt': t}}
        x = mycol.delete_many(myquery)
        
        time.sleep(30)

p = Process(target=disengageOld, args=('asdf', ))
print (p, p.is_alive())
p.start()
print (p, p.is_alive())


############################### DB ############################################
"""
OPEN A DATABASE. IT CAN BE HOSTED EITHER LOCALLY OR REMOTELY.
"""
def start(update, context):
    myclient = pymongo.MongoClient("mongodb+srv://nightman:Computer1@cluster0-dgw53.mongodb.net/test?retryWrites=true&w=majority")
    mydb = myclient["mydatabase"]# create a db in the client
    context.user_data['mycol'] = mydb["customers"]      # create a collection in the db
    context.user_data['arch'] = mydb["archive"]
    
    initUserData(context)

    goto = 'from'
    context.user_data['caller_stack'] = []
    context.user_data['geolocation'] = []
    context.user_data['returnToMain'] = False
    context.user_data['gif'] = False
    context.user_data['address_book'] = {
        'SVOBC': 'Шереметьево, Терминал B, Химки, Россия',
        'SVODEF': 'Шереметьево, Терминал D, Москва, Россия',
        'VKO': 'Внуково Международный Аэропорт, Внуково, Московская область, Россия',
        'DME': 'Московский аэропорт Домодедово, Московская область, Россия',
        'ZIA': 'Международный аэропорт Жуковский, улица Наркомвод, Жуковский, Россия',
        'МГУ': 'Московский государственный университет',
        'МГТУ':'МГТУ им. Н.Э.Баумана, 2-я Бауманская улица, Москва, Россия',
        'ВШЭ': 'Высшая школа экономики, Мясницкая улица, Москва, Россия',
        'РАНХиГС': 'РАНХиГС, проспект Вернадского, Москва, Россия',
        'МЭИ': 'Московский энергетический институт, Красноказарменная улица, Москва, Россия',
        'Белорусский': 'Белорусский вокзал, площадь Тверская Застава, Москва, Россия', 
        'Рижский': 'Рижский вокзал, Москва, Россия',
        'Казанский':'Казанский вокзал, Комсомольская площадь, Москва, Россия',
        'Ярославский': 'Ярославский вокзал, Комсомольская площадь, Москва, Россия',
        'Арбатская': 'Метро Арбатская, Москва, Россия', 
        'Бауманская': 'Метро Бауманская, Москва, Россия', 
        'Волоколамская': 'Метро Волоколамская, Москва, Россия', 
        'Измайловская': 'Метро Измайловская, Москва, Россия', 
        'Киевская': 'Метро Киевская, Москва, Россия', 
        'Крылатское': 'Метро Крылатское, Москва, Россия', 
        'Кунцевская': 'Метро Кунцевская, Москва, Россия', 
        'Курская': 'Метро Курская, Москва, Россия', 
        'Митино': 'Метро Митино, Москва, Россия', 
        'Молодёжная': 'Метро Молодёжная, Москва, Россия', 
        'Мякинино': 'Метро Мякинино, Москва, Россия', 
        'ПаркПобеды': 'Метро Парк Победы, Москва, Россия', 
        'Партизанская': 'Метро Партизанская, Москва, Россия', 
        'Первомайская': 'Метро Первомайская, Москва, Россия', 
        'ПлощадьРеволюции': 'Метро Площадь Революции, Москва, Россия', 
        'ПятницкоеШоссе': 'Метро Пятницкое шоссе, Москва, Россия', 
        'Семёновская': 'Метро Семёновская, Москва, Россия', 
        'СлавянскийБульвар': 'Метро Славянский бульвар, Москва, Россия', 
        'Смоленская': 'Метро Смоленская, Москва, Россия', 
        'Строгино': 'Метро Строгино, Москва, Россия', 
        'Щёлковская': 'Метро Щёлковская, Москва, Россия', 
        'Электрозаводская': 'Метро Электрозаводская, Москва, Россия',
        'Авиамоторная': 'Метро Авиамоторная, Москва, Россия', 
        'АминьевскоеШоссе': 'Метро Аминьевское шоссе, Москва, Россия', 
        'Воронцовская': 'Метро Воронцовская, Москва, Россия', 
        'ДеловойЦентр': 'Метро Деловой центр, Москва, Россия', 
        'Каховская': 'Метро Каховская, Москва, Россия', 
        'Каширская': 'Метро Каширская, Москва, Россия', 
        'Кунцевская': 'Метро Кунцевская, Москва, Россия', 
        'Лефортово': 'Метро Лефортово, Москва, Россия', 
        'МичуринскийПроспект': 'Метро Мичуринский проспект, Москва, Россия', 
        'Мневники': 'Метро Мневники, Москва, Россия', 
        'НагатинскийЗатон': 'Метро Нагатинский затон, Москва, Россия', 
        'Нижегородская улица': 'Метро Нижегородская улица, Москва, Россия', 
        'НижняяМасловка': 'Метро Нижняя Масловка, Москва, Россия', 
        'ПетровскийПарк': 'Метро Петровский парк, Москва, Россия', 
        'Печатники': 'Метро Печатники, Москва, Россия', 
        'ПроспектВернадского': 'Метро Проспект Вернадского, Москва, Россия', 
        'Ржевская': 'Метро Ржевская, Москва, Россия', 
        'Савеловская': 'Метро Савеловская, Москва, Россия', 
        'СевастопольскийПроспект': 'Метро Севастопольский проспект, Москва, Россия', 
        'Сокольники': 'Метро Сокольники, Москва, Россия', 
        'Текстильщики': 'Метро Текстильщики, Москва, Россия', 
        'Терехово': 'Метро Терехово, Москва, Россия', 
        'УлицаНародногоОполчения': 'Метро Улица Народного ополчения, Москва, Россия', 
        'УлицаНоваторов': 'Метро Улица Новаторов, Москва, Россия', 
        'ХодынскоеПоле': 'Метро Ходынское поле, Москва, Россия', 
        'Хорошёвская': 'Метро Хорошёвская, Москва, Россия', 
        'ЦСКА': 'Метро ЦСКА, Москва, Россия', 
        'Шелепиха': 'Метро Шелепиха, Москва, Россия', 
        'Шереметьевская': 'Метро Шереметьевская, Москва, Россия', 
        'Электрозаводская': 'Метро Электрозаводская, Москва, Россия',
        'Автозаводская': 'Метро Автозаводская, Москва, Россия', 
        'АлмаАтинская': 'Метро Алма-Атинская, Москва, Россия', 
        'Аэропорт': 'Метро Аэропорт, Москва, Россия', 
        'Беломорская': 'Метро Беломорская, Москва, Россия', 
        'Белорусская': 'Метро Белорусская, Москва, Россия', 
        'ВодныйCтадион': 'Метро Водный стадион, Москва, Россия', 
        'Войковская': 'Метро Войковская, Москва, Россия', 
        'Динамо': 'Метро Динамо, Москва, Россия', 
        'Домодедовская': 'Метро Домодедовская, Москва, Россия', 
        'Кантемировская': 'Метро Кантемировская, Москва, Россия', 
        'Каширская': 'Метро Каширская, Москва, Россия', 
        'Коломенская': 'Метро Коломенская, Москва, Россия', 
        'Красногвардейская': 'Метро Красногвардейская, Москва, Россия', 
        'Маяковская': 'Метро Маяковская, Москва, Россия', 
        'Новокузнецкая': 'Метро Новокузнецкая, Москва, Россия', 
        'Орехово': 'Метро Орехово, Москва, Россия', 
        'Павелецкая': 'Метро Павелецкая, Москва, Россия', 
        'Речной вокзал': 'Метро Речной вокзал, Москва, Россия', 
        'Сокол': 'Метро Сокол, Москва, Россия', 
        'Тверская': 'Метро Тверская, Москва, Россия', 
        'Театральная': 'Метро Театральная, Москва, Россия', 
        'Технопарк': 'Метро Технопарк, Москва, Россия', 
        'Ховрино': 'Метро Ховрино, Москва, Россия', 
        'Царицыно': 'Метро Царицыно, Москва, Россия',
        'Авиамоторная': 'Метро Авиамоторная, Москва, Россия', 
        'Марксистская': 'Метро Марксистская, Москва, Россия', 
        'Новогиреево': 'Метро Новогиреево, Москва, Россия', 
        'Новокосино': 'Метро Новокосино, Москва, Россия', 
        'Перово': 'Метро Перово, Москва, Россия', 
        'ПлощадьИльича': 'Метро Площадь Ильича, Москва, Россия', 
        'Третьяковская': 'Метро Третьяковская, Москва, Россия', 
        'ШоссеЭнтузиастов': 'Метро Шоссе Энтузиастов, Москва, Россия', 
        'Академическая': 'Метро Академическая, Москва, Россия', 
        'Алексеевская': 'Метро Алексеевская, Москва, Россия', 
        'Бабушкинская': 'Метро Бабушкинская, Москва, Россия', 
        'Беляево': 'Метро Беляево, Москва, Россия', 
        'Ботанический сад': 'Метро Ботанический сад, Москва, Россия', 
        'ВДНХ': 'Метро ВДНХ, Москва, Россия', 
        'Калужская': 'Метро Калужская, Москва, Россия', 
        'КитайГород': 'Метро Китай-город, Москва, Россия', 
        'Коньково': 'Метро Коньково, Москва, Россия', 
        'ЛенинскийПроспект': 'Метро Ленинский проспект, Москва, Россия', 
        'Медведково': 'Метро Медведково, Москва, Россия', 
        'Новоясеневская': 'Метро Новоясеневская, Москва, Россия', 
        'НовыеЧерёмушки': 'Метро Новые Черёмушки, Москва, Россия', 
        'Октябрьская': 'Метро Октябрьская, Москва, Россия', 
        'ПроспектМира': 'Метро Проспект Мира, Москва, Россия', 
        'Профсоюзная': 'Метро Профсоюзная, Москва, Россия', 
        'Рижская': 'Метро Рижская, Москва, Россия', 
        'Свиблово': 'Метро Свиблово, Москва, Россия', 
        'Сухаревская': 'Метро Сухаревская, Москва, Россия', 
        'ТёплыйСтан': 'Метро Тёплый стан, Москва, Россия', 
        'Третьяковская': 'Метро Третьяковская, Москва, Россия', 
        'Тургеневская': 'Метро Тургеневская, Москва, Россия', 
        'Челобитьево': 'Метро Челобитьево, Москва, Россия', 
        'Шаболовская': 'Метро Шаболовская, Москва, Россия', 
        'Ясенево': 'Метро Ясенево, Москва, Россия',
        'Варшавская': 'Метро Варшавская, Москва, Россия', 
        'Каховская': 'Метро Каховская, Москва, Россия', 
        'Каширская': 'Метро Каширская, Москва, Россия', 
        'Белорусская': 'Метро Белорусская, Москва, Россия', 
        'Добрынинская': 'Метро Добрынинская, Москва, Россия', 
        'Киевская': 'Метро Киевская, Москва, Россия', 
        'Комсомольская': 'Метро Комсомольская, Москва, Россия', 
        'Краснопресненская': 'Метро Краснопресненская, Москва, Россия', 
        'Курская': 'Метро Курская, Москва, Россия', 
        'Новослободская': 'Метро Новослободская, Москва, Россия', 
        'Октябрьская': 'Метро Октябрьская, Москва, Россия', 
        'Павелецкая': 'Метро Павелецкая, Москва, Россия', 
        'ПаркКультуры': 'Метро Парк культуры, Москва, Россия', 
        'ПроспектМира': 'Метро Проспект Мира, Москва, Россия', 
        'Суворовская': 'Метро Суворовская, Москва, Россия', 
        'Таганская': 'Метро Таганская, Москва, Россия',
        'Борисово': 'Метро Борисово, Москва, Россия', 
        'Братиславская': 'Метро Братиславская, Москва, Россия', 
        'Бутырская': 'Метро Бутырская, Москва, Россия', 
        'ВерхниеЛихоборы': 'Метро Верхние Лихоборы, Москва, Россия', 
        'Волжская': 'Метро Волжская, Москва, Россия', 
        'ДмитровскоеШоссе': 'Метро Дмитровское шоссе, Москва, Россия', 
        'Достоевская': 'Метро Достоевская, Москва, Россия', 
        'Дубровка': 'Метро Дубровка, Москва, Россия', 
        'Зябликово': 'Метро Зябликово, Москва, Россия', 
        'Кожуховская': 'Метро Кожуховская, Москва, Россия', 
        'КрестьянскаяЗастава': 'Метро Крестьянская застава, Москва, Россия', 
        'Люблино': 'Метро Люблино, Москва, Россия', 
        'Марьина роща': 'Метро Марьина роща, Москва, Россия', 
        'Марьино': 'Метро Марьино, Москва, Россия', 
        'Окружная': 'Метро Окружная, Москва, Россия', 
        'ПетровскоРазумовская': 'Метро Петровско-Разумовская, Москва, Россия', 
        'Печатники': 'Метро Печатники, Москва, Россия', 
        'Римская': 'Метро Римская, Москва, Россия', 
        'Селигерская': 'Метро Селигерская, Москва, Россия', 
        'СретенскийБульвар': 'Метро Сретенский бульвар, Москва, Россия', 
        'Трубная': 'Метро Трубная, Москва, Россия', 
        'Фонвизинская': 'Метро Фонвизинская, Москва, Россия', 
        'Чкаловская': 'Метро Чкаловская, Москва, Россия', 
        'Шипиловская': 'Метро Шипиловская, Москва, Россия', 
        'Выставочный центр': 'Метро Выставочный центр, Москва, Россия', 
        'Телецентр': 'Метро Телецентр, Москва, Россия', 
        'Тимирязевская': 'Метро Тимирязевская, Москва, Россия', 
        'УлицаАкадемикаКоролёва': 'Метро Улица академика Королёва, Москва, Россия', 
        'УлицаМилашенкова': 'Метро Улица Милашенкова, Москва, Россия', 
        'УлицаСергеяЭйзенштейна': 'Метро Улица Сергея Эйзенштейна, Москва, Россия', 
        'Автозаводская': 'Метро Автозаводская, Москва, Россия', 
        'Андроновка': 'Метро Андроновка, Москва, Россия', 
        'Балтийская': 'Метро Балтийская, Москва, Россия', 
        'Белокаменная': 'Метро Белокаменная, Москва, Россия', 
        'БотаническийСад': 'Метро Ботанический сад, Москва, Россия', 
        'БульварРокоссовского': 'Метро Бульвар Рокоссовского, Москва, Россия', 
        'ВерхниеКотлы': 'Метро Верхние Котлы, Москва, Россия', 
        'Владыкино': 'Метро Владыкино, Москва, Россия', 
        'ДеловойЦентр': 'Метро Деловой центр, Москва, Россия', 
        'Дубровка': 'Метро Дубровка, Москва, Россия', 
        'ЗИЛ': 'Метро ЗИЛ, Москва, Россия', 
        'Зорге': 'Метро Зорге, Москва, Россия', 
        'Измайлово': 'Метро Измайлово, Москва, Россия', 
        'Коптево': 'Метро Коптево, Москва, Россия', 
        'Крымская': 'Метро Крымская, Москва, Россия', 
        'Кутузовская': 'Метро Кутузовская, Москва, Россия', 
        'Лихоборы': 'Метро Лихоборы, Москва, Россия', 
        'Локомотив': 'Метро Локомотив, Москва, Россия', 
        'Лужники': 'Метро Лужники, Москва, Россия', 
        'Нижегородская': 'Метро Нижегородская, Москва, Россия', 
        'Новохохловская': 'Метро Новохохловская, Москва, Россия', 
        'Окружная': 'Метро Окружная, Москва, Россия', 
        'Панфиловская': 'Метро Панфиловская, Москва, Россия', 
        'ПлощадьГагарина': 'Метро Площадь Гагарина, Москва, Россия', 
        'Ростокино': 'Метро Ростокино, Москва, Россия', 
        'СоколинаяГора': 'Метро Соколиная Гора, Москва, Россия', 
        'Стрешнево': 'Метро Стрешнево, Москва, Россия', 
        'Угрешская': 'Метро Угрешская, Москва, Россия', 
        'Хорошёво': 'Метро Хорошёво, Москва, Россия', 
        'Шелепиха': 'Метро Шелепиха, Москва, Россия', 
        'ШоссеЭнтузиастов': 'Метро Шоссе Энтузиастов, Москва, Россия', 
        'Авиамоторная': 'Метро Авиамоторная, Москва, Россия', 
        'Косино': 'Метро Косино, Москва, Россия', 
        'Лухмановская': 'Метро Лухмановская, Москва, Россия', 
        'Некрасовка': 'Метро Некрасовка, Москва, Россия', 
        'Нижегородская улица': 'Метро Нижегородская улица, Москва, Россия', 
        'ОкскаяУлица': 'Метро Окская улица, Москва, Россия', 
        'Стахановская': 'Метро Стахановская, Москва, Россия', 
        'УлицаДмитриевского': 'Метро улица Дмитриевского, Москва, Россия', 
        'ЮгоВосточная': 'Метро Юго-Восточная, Москва, Россия', 
        'Алтуфьево': 'Метро Алтуфьево, Москва, Россия', 
        'Аннино': 'Метро Аннино, Москва, Россия', 
        'Бибирево': 'Метро Бибирево, Москва, Россия', 
        'Боровицкая': 'Метро Боровицкая, Москва, Россия', 
        'БульварДмитрияДонского': 'Метро Бульвар Дмитрия Донского, Москва, Россия', 
        'Владыкино': 'Метро Владыкино, Москва, Россия', 
        'Дмитровская': 'Метро Дмитровская, Москва, Россия', 
        'Менделеевская': 'Метро Менделеевская, Москва, Россия', 
        'Нагатинская': 'Метро Нагатинская, Москва, Россия', 
        'Нагорная': 'Метро Нагорная, Москва, Россия', 
        'НахимовскийПроспект': 'Метро Нахимовский проспект, Москва, Россия', 
        'Отрадное': 'Метро Отрадное, Москва, Россия', 
        'ПетровскоРазумовская': 'Метро Петровско-Разумовская, Москва, Россия', 
        'Полянка': 'Метро Полянка, Москва, Россия', 
        'Пражская': 'Метро Пражская, Москва, Россия', 
        'Савёловская': 'Метро Савёловская, Москва, Россия', 
        'Севастопольская': 'Метро Севастопольская, Москва, Россия', 
        'Серпуховская': 'Метро Серпуховская, Москва, Россия', 
        'Тимирязевская': 'Метро Тимирязевская, Москва, Россия', 
        'Тульская': 'Метро Тульская, Москва, Россия', 
        'УлицаАкадемикаЯнгеля': 'Метро Улица академика Янгеля, Москва, Россия', 
        'ЦветнойБульвар': 'Метро Цветной бульвар, Москва, Россия', 
        'Чертановская': 'Метро Чертановская, Москва, Россия', 
        'Чеховская': 'Метро Чеховская, Москва, Россия', 
        'Южная': 'Метро Южная, Москва, Россия', 
        'Библиотека имени Ленина': 'Метро Библиотека имени Ленина, Москва, Россия', 
        'БульварРокоссовского': 'Метро Бульвар Рокоссовского, Москва, Россия', 
        'Воробьёвы горы': 'Метро Воробьёвы горы, Москва, Россия', 
        'Коммунарка': 'Метро Коммунарка, Москва, Россия', 
        'Комсомольская': 'Метро Комсомольская, Москва, Россия', 
        'Красносельская': 'Метро Красносельская, Москва, Россия', 
        'КрасныеВорота': 'Метро Красные ворота, Москва, Россия', 
        'Кропоткинская': 'Метро Кропоткинская, Москва, Россия', 
        'Лубянка': 'Метро Лубянка, Москва, Россия', 
        'Ольховая': 'Метро Ольховая, Москва, Россия', 
        'ОхотныйРяд': 'Метро Охотный ряд, Москва, Россия', 
        'ПаркКультуры': 'Метро Парк культуры, Москва, Россия', 
        'Преображенская площадь': 'Метро Преображенская площадь, Москва, Россия', 
        'Прокшино': 'Метро Прокшино, Москва, Россия', 
        'ПроспектВернадского': 'Метро Проспект Вернадского, Москва, Россия', 
        'Румянцево': 'Метро Румянцево, Москва, Россия', 
        'Саларьево': 'Метро Саларьево, Москва, Россия', 
        'Сокольники': 'Метро Сокольники, Москва, Россия', 
        'Спортивная': 'Метро Спортивная, Москва, Россия', 
        'Тропарёво': 'Метро Тропарёво, Москва, Россия', 
        'Университет': 'Метро Университет, Москва, Россия', 
        'ФилатовЛуг': 'Метро Филатов луг, Москва, Россия', 
        'Фрунзенская': 'Метро Фрунзенская, Москва, Россия', 
        'Черкизовская': 'Метро Черкизовская, Москва, Россия', 
        'Чистые пруды': 'Метро Чистые пруды, Москва, Россия', 
        'ЮгоЗападная': 'Метро Юго-Западная, Москва, Россия', 
        'Боровское шоссе': 'Метро Боровское шоссе, Москва, Россия', 
        'Волхонка': 'Метро Волхонка, Москва, Россия', 
        'Говорово': 'Метро Говорово, Москва, Россия', 
        'ДеловойЦентр': 'Метро Деловой центр, Москва, Россия', 
        'Дорогомиловская': 'Метро Дорогомиловская, Москва, Россия', 
        'ЛомоносовскийПроспект': 'Метро Ломоносовский проспект, Москва, Россия', 
        'Минская': 'Метро Минская, Москва, Россия', 
        'МичуринскийПроспект': 'Метро Мичуринский проспект, Москва, Россия', 
        'Новопеределкино': 'Метро Новопеределкино, Москва, Россия', 
        'Озерная': 'Метро Озерная, Москва, Россия', 
        'Очаково': 'Метро Очаково, Москва, Россия', 
        'ПаркПобеды': 'Метро Парк Победы, Москва, Россия', 
        'Плющиха': 'Метро Плющиха, Москва, Россия', 
        'Раменки': 'Метро Раменки, Москва, Россия', 
        'Рассказовка': 'Метро Рассказовка, Москва, Россия', 
        'Солнцево': 'Метро Солнцево, Москва, Россия', 
        'Терешково': 'Метро Терешково, Москва, Россия', 
        'Третьяковская': 'Метро Третьяковская, Москва, Россия', 
        'Баррикадная': 'Метро Баррикадная, Москва, Россия', 
        'Беговая': 'Метро Беговая, Москва, Россия', 
        'Волгоградский проспект': 'Метро Волгоградский проспект, Москва, Россия', 
        'Выхино': 'Метро Выхино, Москва, Россия', 
        'Жулебино': 'Метро Жулебино, Москва, Россия', 
        'КитайГород': 'Метро Китай-город, Москва, Россия', 
        'Котельники': 'Метро Котельники, Москва, Россия', 
        'Кузнецкий мост': 'Метро Кузнецкий мост, Москва, Россия', 
        'Кузьминки': 'Метро Кузьминки, Москва, Россия', 
        'ЛермонтовскийПроспект': 'Метро Лермонтовский проспект, Москва, Россия', 
        'Октябрьское поле': 'Метро Октябрьское поле, Москва, Россия', 
        'Планерная': 'Метро Планерная, Москва, Россия', 
        'Полежаевская': 'Метро Полежаевская, Москва, Россия', 
        'Пролетарская': 'Метро Пролетарская, Москва, Россия', 
        'Пушкинская': 'Метро Пушкинская, Москва, Россия', 
        'РязанскийПроспект': 'Метро Рязанский проспект, Москва, Россия', 
        'Спартак': 'Метро Спартак, Москва, Россия', 
        'Сходненская': 'Метро Сходненская, Москва, Россия', 
        'Таганская': 'Метро Таганская, Москва, Россия', 
        'Текстильщики': 'Метро Текстильщики, Москва, Россия', 
        'Тушинская': 'Метро Тушинская, Москва, Россия', 
        'Улица1905Года': 'Метро Улица 1905 года, Москва, Россия', 
        'Щукинская': 'Метро Щукинская, Москва, Россия', 
        'АлександровскийСад': 'Метро Александровский сад, Москва, Россия', 
        'Арбатская': 'Метро Арбатская, Москва, Россия', 
        'Багратионовская': 'Метро Багратионовская, Москва, Россия', 
        'Выставочная': 'Метро Выставочная, Москва, Россия', 
        'Киевская': 'Метро Киевская, Москва, Россия', 
        'Кунцевская': 'Метро Кунцевская, Москва, Россия', 
        'Кутузовская': 'Метро Кутузовская, Москва, Россия', 
        'Международная': 'Метро Международная, Москва, Россия', 
        'Пионерская': 'Метро Пионерская, Москва, Россия', 
        'Смоленская': 'Метро Смоленская, Москва, Россия', 
        'Студенческая': 'Метро Студенческая, Москва, Россия', 
        'Филёвский парк': 'Метро Филёвский парк, Москва, Россия', 
        'Фили': 'Метро Фили, Москва, Россия',
        'БитцевскийПарк': 'Метро Битцевский парк, Москва, Россия', 
        'БульварАдмиралаУшакова': 'Метро Бульвар адмирала Ушакова, Москва, Россия', 
        'БунинскаяАллея': 'Метро Бунинская аллея, Москва, Россия', 
        'Лесопарковая': 'Метро Лесопарковая, Москва, Россия', 
        'УлицаГорчакова': 'Метро Улица Горчакова, Москва, Россия', 
        'УлицаСкобелевская': 'Метро Улица Скобелевская, Москва, Россия', 
        'УлицаСтарокачаловская': 'Метро Улица Старокачаловская, Москва, Россия'}

    # loc_keyboard = KeyboardButton(text="Определить мои координаты", request_location=True)
    # custom_keyboard = [[loc_keyboard]]
    # reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                            text="Здравствуйте. Я помогаю найти попутчиков для вашей поездки на такси. Если возникла какая-то проблема, перезапустите меня, набрав /start. Выберите, откуда Вы планируте поездку.")
    out = update.message.reply_text(menu_message(goto, context), reply_markup=menu_keyboard(goto, context), parse_mode=telegram.ParseMode.HTML)
    context.user_data['last_message_id'] = out.message_id

def initUserData(context):
    mydict = {"user_name": 0, 
              "chat_id": 0, 
              "user_id": 0, 
              "start_loc": 0,
              "target_loc": 0,
              "start_str": 0,
              "target_str": 0,
              "time": 0,
              "engaged": 0,
              "updated": 0}
    context.user_data['mydict'] = mydict

def button(update, context):
    query = update.callback_query
    try:
        query.answer() # CallbackQueries need to be answered, even if no notification to the user is needed   
    except:
        pass
    
    caller = query.data.split('_')[0]
    answer = query.data.split('_')[1]
    if answer != 'map':
        context.user_data['caller_stack'].append(caller)
    # context.bot.delete_message(chat_id=348368436, message_id=2280)


    if caller=='from' or caller=='to':
        message_id = update.effective_message.message_id
        if answer != 'back' and answer != 'map':
            goto = answer
        elif answer == 'map':
            context.user_data['gif'] = True
            ret0 = context.bot.edit_message_text(chat_id=update.effective_chat.id, 
                                        message_id=query.message.message_id, 
                                        text='<b>Нажмите на скрепку => Локация, затем укажите ваше местоположение на карте</b>', 
                                        parse_mode=telegram.ParseMode.HTML)
            message_id = ret0.message_id
            ret1 = context.bot.send_animation(chat_id=update.effective_chat.id, animation='https://media.giphy.com/media/dt08hHC78HEjocF1r1/giphy.gif', timeout=60)
            
            time.sleep(5)
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=ret1.message_id)
            goto = caller

        else:
            context.user_data['caller_stack'].pop()
            goto = context.user_data['caller_stack'][-1]
            context.user_data['caller_stack'].pop()
            if len(context.user_data['caller_stack']) == 0:
                context.user_data['geolocation'] = []
                context.user_data['mydict']['start_loc'] = 0
                context.user_data['mydict']['target_loc'] = 0
                context.user_data['mydict']['start_str'] = 0
                context.user_data['mydict']['target_str'] = 0
                context.user_data['mydict']['time'] = 0
        
        out = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                            message_id=message_id,
                            text=menu_message(goto, context),
                            parse_mode=telegram.ParseMode.HTML, 
                            reply_markup=menu_keyboard(goto, context))
        context.user_data['last_message_id'] = out.message_id
    
    elif caller=='ChooseTime':
        if answer != 'back':
            context.user_data['mydict']['time'] = answer
            goto = 'Confirm'
        else:
            context.user_data['caller_stack'].pop()
            goto = context.user_data['caller_stack'][-1]
            context.user_data['caller_stack'].pop()
        out = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                        message_id=query.message.message_id,
                        text=menu_message(goto, context), 
                        parse_mode=telegram.ParseMode.HTML, 
                        reply_markup=menu_keyboard(goto, context))
        context.user_data['last_message_id'] = out.message_id

    elif (caller=='ВУЗы' or caller=='вокзалы' or caller=='аэропорты' or caller[:-1]=='линия'):
        if answer != 'back':
            if 'to' in context.user_data['caller_stack']:
                context.user_data['mydict']['target_str'] = context.user_data['address_book'][answer]
                context.user_data['mydict']['target_loc'] = forward_geocode(context.user_data['mydict']['target_str'])
                goto = 'ChooseTime'
            else:
                context.user_data['mydict']['start_str'] = context.user_data['address_book'][answer]
                context.user_data['mydict']['start_loc'] = forward_geocode(context.user_data['mydict']['start_str'])
                goto = 'to'
                
        else:
            # goto = context.user_data['caller_stack'][-1]
            context.user_data['caller_stack'].pop()
            goto = context.user_data['caller_stack'][-1]
            context.user_data['caller_stack'].pop()
        out = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                        message_id=query.message.message_id,
                        text=menu_message(goto, context), 
                        parse_mode=telegram.ParseMode.HTML, 
                        reply_markup=menu_keyboard(goto, context))
        context.user_data['last_message_id'] = out.message_id

    elif caller=='метро':
        if answer != 'back':
            goto = answer
        else:
            context.user_data['caller_stack'].pop()
            goto = context.user_data['caller_stack'][-1]
            context.user_data['caller_stack'].pop()
        out = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                            message_id=query.message.message_id,
                            text=menu_message(goto, context), 
                            reply_markup=menu_keyboard(goto, context),
                            parse_mode=telegram.ParseMode.HTML)
        context.user_data['last_message_id'] = out.message_id
    
    elif caller=='Confirm':
        if answer != 'cancel':
            write2db(update, context)
            latest_matches, reply_markup = menu_kb2(context)
            text = 'Polling...' if len(latest_matches) > 0 else '*Пока ничего не найдено.* Мы предложим Вам подходящие варианты, как только они появятся в базе. Вы также можете сделать запрос на другое время.'
            context.user_data['message_id'] = update.effective_message.message_id
            context.user_data['chat_id'] = update.effective_chat.id
            context.user_data['enough'] = False
            context.job_queue.run_repeating(refresh, interval=4, first=1, context=context.user_data)
        else:
            context.user_data['mydict']['start_loc'] = 0
            context.user_data['mydict']['target_loc'] = 0
            context.user_data['mydict']['start_str'] = 0
            context.user_data['mydict']['target_str'] = 0
            context.user_data['mydict']['time'] = 0
            context.user_data['caller_stack'] = []
            context.user_data['geolocation'] = []

            try:
                # remove the returnToMainOnDefault job
                context.job_queue.get_jobs_by_name('returnToMainOnDefault')[0].schedule_removal()
            except:
                pass
            goto = 'from'
            disengagePairOfUsers(update, context)
        
            context.user_data['enough'] = True # mark the job for removal
        try:
            out = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                message_id=query.message.message_id,
                                text=menu_message(goto, context), 
                                reply_markup=menu_keyboard(goto, context),
                                parse_mode=telegram.ParseMode.HTML)
            context.user_data['last_message_id'] = out.message_id
        except:
            pass
    
    elif caller=='SelectMatch' or caller=='Searching' or caller=='ContactChosen':
        if answer[:3]=='opt':
            context.user_data['enough'] = True # mark the job for removal
            showClickedContact(update, context, answer[3:])
        if answer == 'cancel':
            try:
                # remove the returnToMainOnDefault job
                context.job_queue.get_jobs_by_name('returnToMainOnDefault')[0].schedule_removal()
            except:
                pass
            goto = 'from'
            context.user_data['geolocation'] = []
            context.user_data['mydict']['start_loc'] = 0
            context.user_data['mydict']['target_loc'] = 0
            context.user_data['mydict']['start_str'] = 0
            context.user_data['mydict']['target_str'] = 0
            context.user_data['mydict']['time'] = 0

            disengagePairOfUsers(update, context)
            context.user_data['caller_stack'] = []
            context.user_data['enough'] = True # mark the job for removal
            out = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                message_id=query.message.message_id,
                                text=menu_message(goto, context), 
                                reply_markup=menu_keyboard(goto, context),
                                parse_mode=telegram.ParseMode.HTML)
            context.user_data['last_message_id'] = out.message_id
    else:
        pass

def engagePairOfUsers(update, context):
    chosen_uid = context.user_data['chosen_uid']
    active_uid = context.user_data['current_uid']
    mycol = context.user_data['mycol']
    myquery = { "user_id": {"$in": [chosen_uid, active_uid] } }
    newvalues = { "$set": { "engaged": True, "updated": datetime.datetime.now()}}
    x = mycol.update_many(myquery, newvalues)

def disengagePairOfUsers(update, context):
    try:
        mycol = context.job.context['mycol']
        try:
            chosen_uid = context.job.context['chosen_uid']
            active_uid = context.job.context['current_uid']
            myquery = { "user_id": {"$in": [chosen_uid, active_uid] } }
            newvalues = { "$set": { "engaged": False, "updated": datetime.datetime.now()} }
            x = mycol.update_many(myquery, newvalues)
            context.job.context['mydict']['start_loc'] = 0
            context.job.context['mydict']['target_loc'] = 0
            context.job.context['mydict']['start_str'] = 0
            context.job.context['mydict']['target_str'] = 0
        except:
            pass
    except:
        mycol = context.user_data['mycol']
        try:
            chosen_uid = context.user_data['chosen_uid']
            active_uid = context.user_data['current_uid']
            myquery = { "user_id": {"$in": [chosen_uid, active_uid] } }
            newvalues = { "$set": { "engaged": False, "updated": datetime.datetime.now()} }
            x = mycol.update_many(myquery, newvalues)
            context.user_data['mydict']['start_loc'] = 0
            context.user_data['mydict']['target_loc'] = 0
            context.user_data['mydict']['start_str'] = 0
            context.user_data['mydict']['target_str'] = 0
        except:
            pass
    finally:
        try:
            active_uid = context.user_data['mydict']['user_id']
        except:
            active_uid = context.job.context['mydict']['user_id']
        myquery = { "user_id": active_uid}
        x = mycol.delete_one(myquery)

def showClickedContact(update, context, clicked_user_id_name):
    time.sleep(1)
    query = update.callback_query
    user_id = int(clicked_user_id_name.split('@')[0])
    user_name = clicked_user_id_name.split('@')[1]
    context.user_data['chosen_uid'] = user_id
    context.user_data['current_uid'] = update.effective_user.id

    engagePairOfUsers(update, context)

    text = 'Свяжитесь с пользователем [{}](tg://user?id={}) в течение 1 минуты и договоритесь о месте встречи.'.format(user_name, str(user_id))
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Отмена', callback_data='ContactChosen_cancel')]])
    out = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                            message_id=query.message.message_id,
                            text=text, 
                            parse_mode='Markdown', 
                            reply_markup=reply_markup)
    context.user_data['last_message_id'] = out.message_id
    context.job_queue.run_once(returnToMainOnDefault, when=10, context=context.user_data)

def returnToMainOnDefault(context: CallbackContext):
    message_id = context.job.context['message_id']
    chat_id = context.job.context['chat_id']
    context.job.context['caller_stack'] = []
    goto = 'from'
    disengagePairOfUsers(None, context)

    try:
        context.user_data['enough'] = True # mark the job for removal
    except:
        context.job.context['enough'] = True # mark the job for removal
    context.bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=menu_message(goto, context),
                                reply_markup=menu_keyboard(goto, context),
                                parse_mode=telegram.ParseMode.HTML)

def menu_keyboard(goto, context):
    if goto == 'back':
        goto = context.user_data['caller_stack'][-1]
        context.user_data['caller_stack'].pop()
    
    elif goto == 'from':
        time.sleep(1)
        keyboard = [[InlineKeyboardButton('ВУЗ', callback_data='from_ВУЗы'),
                    InlineKeyboardButton('Аэропорт', callback_data='from_аэропорты')],
                    [InlineKeyboardButton('Вокзал', callback_data='from_вокзалы'),
                    InlineKeyboardButton('Станция метро', callback_data='from_метро')],
                    [InlineKeyboardButton('Как выбрать на карте?', callback_data='from_map')]]            
    
    elif goto == 'to':
        keyboard = [[InlineKeyboardButton('ВУЗ', callback_data='to_ВУЗы'),
                    InlineKeyboardButton('Аэропорт', callback_data='to_аэропорты')],
                    [InlineKeyboardButton('Вокзал', callback_data='to_вокзалы'),
                    InlineKeyboardButton('Станция метро', callback_data='to_метро')],
                    [InlineKeyboardButton('Выбрать на карте', callback_data='to_map'),
                    InlineKeyboardButton('Назад', callback_data='to_back')]]
    
    elif goto == 'ВУЗы':
        keyboard = [[InlineKeyboardButton('МГУ', callback_data='ВУЗы_МГУ'), 
                     InlineKeyboardButton('МГТУ', callback_data='ВУЗы_МГТУ'),
                     InlineKeyboardButton('ВШЭ', callback_data='ВУЗы_ВШЭ')],
                    [InlineKeyboardButton('РАНХиГС', callback_data='ВУЗы_РАНХиГС'),
                    InlineKeyboardButton('МЭИ', callback_data='ВУЗы_МЭИ'),
                    InlineKeyboardButton('Назад', callback_data='ВУЗы_back')]]
    
    elif goto == 'аэропорты':
        keyboard = [[InlineKeyboardButton('Шереметьево В/С', callback_data='аэропорты_SVOBC'), 
                     InlineKeyboardButton('Шереметьево D/E/F', callback_data='аэропорты_SVODEF'),
                     InlineKeyboardButton('Внуково', callback_data='аэропорты_VKO')],
                    [InlineKeyboardButton('Домодедово', callback_data='аэропорты_DME'),
                    InlineKeyboardButton('Жуковский', callback_data='аэропорты_ZIA'),
                    InlineKeyboardButton('Назад', callback_data='аэропорты_back')]]
    
    elif goto == 'вокзалы':
        keyboard = [[InlineKeyboardButton('Белорусский', callback_data='вокзалы_Белорусский'), 
                     InlineKeyboardButton('Рижский', callback_data='вокзалы_Рижский'),
                     InlineKeyboardButton('Казанский', callback_data='вокзалы_Казанский')],
                    [InlineKeyboardButton('Ярославский', callback_data='вокзалы_Ярославский'),
                    InlineKeyboardButton('Курский', callback_data='вокзалы_Курский'),
                    InlineKeyboardButton('Назад', callback_data='вокзалы_back')]]
    
    elif goto == 'метро':
        keyboard = [[InlineKeyboardButton('Бутовская', callback_data='метро_линия1'),
                  InlineKeyboardButton('Арбатско-Покровская', callback_data='метро_линия2')],
                  [InlineKeyboardButton('Замоскворецкая', callback_data='метро_линия3'),
                  InlineKeyboardButton('Большая кольцевая', callback_data='метро_линия4')],
                  [InlineKeyboardButton('Калининская', callback_data='метро_линия5'),
                  InlineKeyboardButton('Калужско-Рижская', callback_data='метро_линия6')],
                  [InlineKeyboardButton('Каховская', callback_data='метро_линия7'),
                  InlineKeyboardButton('Кольцевая', callback_data='метро_линия8')],
                  [InlineKeyboardButton('Люблинско-Дмитриевская', callback_data='метро_линия9'),
                  InlineKeyboardButton('Монорельс', callback_data='метро_линияA')],
                  [InlineKeyboardButton('МЦК', callback_data='метро_линияB'),
                  InlineKeyboardButton('Некрасовская', callback_data='метро_линияC')],
                  [InlineKeyboardButton('Серпуховско-Тимирязевская', callback_data='метро_линияD'),
                  InlineKeyboardButton('Сокольническая', callback_data='метро_линияE')],
                  [InlineKeyboardButton('Солнцевская', callback_data='метро_линияF'),
                  InlineKeyboardButton('Таганско-Краснопресненская', callback_data='метро_линияG')],
                  [InlineKeyboardButton('Филёвская', callback_data='метро_линияH'),
                  InlineKeyboardButton('Назад', callback_data='метро_back')]]
   
    elif goto == 'линия1': # Бутовская    
        keyboard = [[InlineKeyboardButton('Битцевский парк', callback_data='линия1_БитцевскийПарк'),
            InlineKeyboardButton('Бульвар адмирала Ушакова', callback_data='линия1_БульварAдмиралаУшакова')],
            [InlineKeyboardButton('Бунинская аллея', callback_data='линия1_БунинскаяAллея'),
            InlineKeyboardButton('Лесопарковая', callback_data='линия1_Лесопарковая')],
            [InlineKeyboardButton('Улица Горчакова', callback_data='линия1_УлицаГорчакова'),
            InlineKeyboardButton('Улица Скобелевская', callback_data='линия1_УлицаСкобелевская')],
            [InlineKeyboardButton('Улица Старокачаловская', callback_data='линия1_УлицаСтарокачаловская')]]
    
    elif goto == 'линия2':  # Арбатско-Покровская        
        keyboard = [[InlineKeyboardButton('Арбатская', callback_data='линия2_Арбатская'),
                    InlineKeyboardButton('Бауманская', callback_data='линия2_Бауманская')],
                    [InlineKeyboardButton('Волоколамская', callback_data='линия2_Волоколамская'),
                    InlineKeyboardButton('Измайловская', callback_data='линия2_Измайловская')],
                    [InlineKeyboardButton('Киевская', callback_data='линия2_Киевская'),
                    InlineKeyboardButton('Крылатское', callback_data='линия2_Крылатское')],
                    [InlineKeyboardButton('Кунцевская', callback_data='линия2_Кунцевская'),
                    InlineKeyboardButton('Курская', callback_data='линия2_Курская')],
                    [InlineKeyboardButton('Митино', callback_data='линия2_Митино'),
                    InlineKeyboardButton('Молодёжная', callback_data='линия2_Молодёжная')],
                    [InlineKeyboardButton('Мякинино', callback_data='линия2_Мякинино'),
                    InlineKeyboardButton('Парк Победы', callback_data='линия2_ПаркПобеды')],
                    [InlineKeyboardButton('Партизанская', callback_data='линия2_Партизанская'),
                    InlineKeyboardButton('Первомайская', callback_data='линия2_Первомайская')],
                    [InlineKeyboardButton('Площадь Революции', callback_data='линия2_ПлощадьРеволюции'),
                    InlineKeyboardButton('Пятницкое шоссе', callback_data='линия2_ПятницкоеШоссе')],
                    [InlineKeyboardButton('Семёновская', callback_data='линия2_Семёновская'),
                    InlineKeyboardButton('Славянский бульвар', callback_data='линия2_СлавянскийБульвар')],
                    [InlineKeyboardButton('Смоленская', callback_data='линия2_Смоленская'),
                    InlineKeyboardButton('Строгино', callback_data='линия2_Строгино')],
                    [InlineKeyboardButton('Щёлковская', callback_data='линия2_Щёлковская'),
                    InlineKeyboardButton('Электрозаводская', callback_data='линия2_Электрозаводская')],
                    [InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'линия3': # Замоскворецкая
        keyboard = [[InlineKeyboardButton('Автозаводская', callback_data='линия3_Автозаводская'),
                    InlineKeyboardButton('Алма-Атинская', callback_data='линия3_АлмаАтинская')],
                    [InlineKeyboardButton('Аэропорт', callback_data='линия3_Аэропорт'),
                    InlineKeyboardButton('Беломорская', callback_data='линия3_Беломорская')],
                    [InlineKeyboardButton('Белорусская', callback_data='линия3_Белорусская'),
                    InlineKeyboardButton('Водный стадион', callback_data='линия3_ВодныйCтадион')],
                    [InlineKeyboardButton('Войковская', callback_data='линия3_Войковская'),
                    InlineKeyboardButton('Динамо', callback_data='линия3_Динамо')],
                    [InlineKeyboardButton('Домодедовская', callback_data='линия3_Домодедовская'),
                    InlineKeyboardButton('Кантемировская', callback_data='линия3_Кантемировская')],
                    [InlineKeyboardButton('Каширская', callback_data='линия3_Каширская'),
                    InlineKeyboardButton('Коломенская', callback_data='линия3_Коломенская')],
                    [InlineKeyboardButton('Красногвардейская', callback_data='линия3_Красногвардейская'),
                    InlineKeyboardButton('Маяковская', callback_data='линия3_Маяковская')],
                    [InlineKeyboardButton('Новокузнецкая', callback_data='линия3_Новокузнецкая'),
                    InlineKeyboardButton('Орехово', callback_data='линия3_Орехово')],
                    [InlineKeyboardButton('Павелецкая', callback_data='линия3_Павелецкая'),
                    InlineKeyboardButton('Речной вокзал', callback_data='линия3_РечнойВокзал')],
                    [InlineKeyboardButton('Сокол', callback_data='линия3_Сокол'),
                    InlineKeyboardButton('Тверская', callback_data='линия3_Тверская')],
                    [InlineKeyboardButton('Театральная', callback_data='линия3_Театральная'),
                    InlineKeyboardButton('Технопарк', callback_data='линия3_Технопарк')],
                    [InlineKeyboardButton('Ховрино', callback_data='линия3_Ховрино'),
                    InlineKeyboardButton('Царицыно', callback_data='линия3_Царицыно')],
                    [InlineKeyboardButton('Назад', callback_data='метро_back')]]
    
    elif goto == 'линия4': # Большая кольцевая
        keyboard = [[InlineKeyboardButton('Авиамоторная', callback_data='линия4_Авиамоторная'),
                    InlineKeyboardButton('Аминьевское шоссе', callback_data='линия4_АминьевскоеШоссе')],
                    [InlineKeyboardButton('Воронцовская', callback_data='линия4_Воронцовская'),
                    InlineKeyboardButton('Деловой центр', callback_data='линия4_ДеловойЦентр')],
                    [InlineKeyboardButton('Каховская', callback_data='линия4_Каховская'),
                    InlineKeyboardButton('Каширская', callback_data='линия4_Каширская')],
                    [InlineKeyboardButton('Кунцевская', callback_data='линия4_Кунцевская'),
                    InlineKeyboardButton('Лефортово', callback_data='линия4_Лефортово')],
                    [InlineKeyboardButton('Мичуринский проспект', callback_data='линия4_МичуринскийПроспект'),
                    InlineKeyboardButton('Мневники', callback_data='линия4_Мневники')],
                    [InlineKeyboardButton('Нагатинский затон', callback_data='линия4_НагатинскийЗатон'),
                    InlineKeyboardButton('Нижегородская улица', callback_data='линия4_НижегородскаяУлица')],
                    [InlineKeyboardButton('Нижняя Масловка', callback_data='линия4_НижняяМасловка'),
                    InlineKeyboardButton('Петровский парк', callback_data='линия4_ПетровскийПарк')],
                    [InlineKeyboardButton('Печатники', callback_data='линия4_Печатники'),
                    InlineKeyboardButton('Проспект Вернадского', callback_data='линия4_ПроспектВернадского')],
                    [InlineKeyboardButton('Ржевская', callback_data='линия4_Ржевская'),
                    InlineKeyboardButton('Савеловская', callback_data='линия4_Савеловская')],
                    [InlineKeyboardButton('Севастопольский проспект', callback_data='линия4_СевастопольскийПроспект'),
                    InlineKeyboardButton('Сокольники', callback_data='линия4_Сокольники')],
                    [InlineKeyboardButton('Текстильщики', callback_data='линия4_Текстильщики'),
                    InlineKeyboardButton('Терехово', callback_data='линия4_Терехово')],
                    [InlineKeyboardButton('Улица Народного ополчения', callback_data='линия4_УлицаНародногоОполчения'),
                    InlineKeyboardButton('Улица Новаторов', callback_data='линия4_УлицаНоваторов')],
                    [InlineKeyboardButton('Ходынское поле', callback_data='линия4_ХодынскоеПоле'),
                    InlineKeyboardButton('Хорошёвская', callback_data='линия4_Хорошёвская')],
                    [InlineKeyboardButton('ЦСКА', callback_data='линия4_ЦСКА'),
                    InlineKeyboardButton('Шелепиха', callback_data='линия4_Шелепиха')],
                    [InlineKeyboardButton('Шереметьевская', callback_data='линия4_Шереметьевская'),
                    InlineKeyboardButton('Электрозаводская', callback_data='линия4_Электрозаводская')],
                    [InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'линия5': # Калининская
        keyboard = [[InlineKeyboardButton('Авиамоторная', callback_data='линия5_Авиамоторная'),
                    InlineKeyboardButton('Марксистская', callback_data='линия5_Марксистская')],
                    [InlineKeyboardButton('Новогиреево', callback_data='линия5_Новогиреево'),
                    InlineKeyboardButton('Новокосино', callback_data='линия5_Новокосино')],
                    [InlineKeyboardButton('Перово', callback_data='линия5_Перово'),
                    InlineKeyboardButton('Площадь Ильича', callback_data='линия5_ПлощадьИльича')],
                    [InlineKeyboardButton('Третьяковская', callback_data='линия5_Третьяковская'),
                    InlineKeyboardButton('Шоссе Энтузиастов', callback_data='линия5_ШоссеЭнтузиастов')],
                    [InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'линия6': # Калужско-Рижская
        keyboard = [[InlineKeyboardButton('Академическая', callback_data='линия6_Академическая'),
                    InlineKeyboardButton('Алексеевская', callback_data='линия6_Алексеевская')],
                    [InlineKeyboardButton('Бабушкинская', callback_data='линия6_Бабушкинская'),
                    InlineKeyboardButton('Беляево', callback_data='линия6_Беляево')],
                    [InlineKeyboardButton('Ботанический сад', callback_data='линия6_БотаническийСад'),
                    InlineKeyboardButton('ВДНХ', callback_data='линия6_ВДНХ')],
                    [InlineKeyboardButton('Калужская', callback_data='линия6_Калужская'),
                    InlineKeyboardButton('Китай-город', callback_data='линия6_КитайГород')],
                    [InlineKeyboardButton('Коньково', callback_data='линия6_Коньково'),
                    InlineKeyboardButton('Ленинский проспект', callback_data='линия6_ЛенинскийПроспект')],
                    [InlineKeyboardButton('Медведково', callback_data='линия6_Медведково'),
                    InlineKeyboardButton('Новоясеневская', callback_data='линия6_Новоясеневская')],
                    [InlineKeyboardButton('Новые Черёмушки', callback_data='линия6_НовыеЧерёмушки'),
                    InlineKeyboardButton('Октябрьская', callback_data='линия6_Октябрьская')],
                    [InlineKeyboardButton('Проспект Мира', callback_data='линия6_ПроспектМира'),
                    InlineKeyboardButton('Профсоюзная', callback_data='линия6_Профсоюзная')],
                    [InlineKeyboardButton('Рижская', callback_data='линия6_Рижская'),
                    InlineKeyboardButton('Свиблово', callback_data='линия6_Свиблово')],
                    [InlineKeyboardButton('Сухаревская', callback_data='линия6_Сухаревская'),
                    InlineKeyboardButton('Тёплый стан', callback_data='линия6_ТёплыйCтан')],
                    [InlineKeyboardButton('Третьяковская', callback_data='линия6_Третьяковская'),
                    InlineKeyboardButton('Тургеневская', callback_data='линия6_Тургеневская')],
                    [InlineKeyboardButton('Челобитьево', callback_data='линия6_Челобитьево'),
                    InlineKeyboardButton('Шаболовская', callback_data='линия6_Шаболовская')],
                    [InlineKeyboardButton('Ясенево', callback_data='линия6_Ясенево'), 
                    InlineKeyboardButton('Назад', callback_data='метро_back')]]
    
    elif goto == 'линия7': # Каховская
        keyboard = [[InlineKeyboardButton('Варшавская', callback_data='линия7_Варшавская'),
            InlineKeyboardButton('Каховская', callback_data='линия7_Каховская')],
            [InlineKeyboardButton('Каширская', callback_data='линия7_Каширская'),
            InlineKeyboardButton('Назад', callback_data='метро_back')]]
    
    elif goto == 'линия8': # Кольцевая
        keyboard = [[InlineKeyboardButton('Белорусская', callback_data='линия4_Белорусская')],
                    [InlineKeyboardButton('Добрынинская', callback_data='линия4_Добрынинская'),
                    InlineKeyboardButton('Киевская', callback_data='линия4_Киевская')],
                    [InlineKeyboardButton('Комсомольская', callback_data='линия4_Комсомольская'),
                    InlineKeyboardButton('Краснопресненская', callback_data='линия4_Краснопресненская')],
                    [InlineKeyboardButton('Курская', callback_data='линия4_Курская'),
                    InlineKeyboardButton('Новослободская', callback_data='линия4_Новослободская')],
                    [InlineKeyboardButton('Октябрьская', callback_data='линия4_Октябрьская'),
                    InlineKeyboardButton('Павелецкая', callback_data='линия4_Павелецкая')],
                    [InlineKeyboardButton('Парк культуры', callback_data='линия4_ПаркКультуры'),
                    InlineKeyboardButton('Проспект Мира', callback_data='линия4_ПроспектМира')],
                    [InlineKeyboardButton('Суворовская', callback_data='линия4_Суворовская'),
                    InlineKeyboardButton('Таганская', callback_data='линия4_Таганская')],
                    [InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'линия9': # Люблинско-дмитриевская
        keyboard = [[InlineKeyboardButton('Борисово', callback_data='линия9_Борисово'),
            InlineKeyboardButton('Братиславская', callback_data='линия9_Братиславская')],
            [InlineKeyboardButton('Бутырская', callback_data='линия9_Бутырская'),
            InlineKeyboardButton('Верхние Лихоборы', callback_data='линия9_ВерхниеЛихоборы')],
            [InlineKeyboardButton('Волжская', callback_data='линия9_Волжская'),
            InlineKeyboardButton('Дмитровское шоссе', callback_data='линия9_ДмитровскоеШоссе')],
            [InlineKeyboardButton('Достоевская', callback_data='линия9_Достоевская'),
            InlineKeyboardButton('Дубровка', callback_data='линия9_Дубровка')],
            [InlineKeyboardButton('Зябликово', callback_data='линия9_Зябликово'),
            InlineKeyboardButton('Кожуховская', callback_data='линия9_Кожуховская')],
            [InlineKeyboardButton('Крестьянская застава', callback_data='линия9_КрестьянскаяЗастава'),
            InlineKeyboardButton('Люблино', callback_data='линия9_Люблино')],
            [InlineKeyboardButton('Марьина роща', callback_data='линия9_МарьинаРоща'),
            InlineKeyboardButton('Марьино', callback_data='линия9_Марьино')],
            [InlineKeyboardButton('Окружная', callback_data='линия9_Окружная'),
            InlineKeyboardButton('Петровско-Разумовская', callback_data='линия9_ПетровскоРазумовская')],
            [InlineKeyboardButton('Печатники', callback_data='линия9_Печатники'),
            InlineKeyboardButton('Римская', callback_data='линия9_Римская')],
            [InlineKeyboardButton('Селигерская', callback_data='линия9_Селигерская'),
            InlineKeyboardButton('Сретенский бульвар', callback_data='линия9_СретенскийБульвар')],
            [InlineKeyboardButton('Трубная', callback_data='линия9_Трубная'),
            InlineKeyboardButton('Фонвизинская', callback_data='линия9_Фонвизинская')],
            [InlineKeyboardButton('Чкаловская', callback_data='линия9_Чкаловская'),
            InlineKeyboardButton('Шипиловская', callback_data='линия9_Шипиловская')],
            [InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'линияA': #монорельс
        keyboard = [[InlineKeyboardButton('Выставочный центр', callback_data='линияA_ВыставочныйЦентр'),
            InlineKeyboardButton('Телецентр', callback_data='линияA_Телецентр')],
            [InlineKeyboardButton('Тимирязевская', callback_data='линияA_Тимирязевская'),
            InlineKeyboardButton('Улица академика Королёва', callback_data='линияA_УлицаАкадемикаКоролёва')],
            [InlineKeyboardButton('Улица Милашенкова', callback_data='линияA_УлицаМилашенкова'),
            InlineKeyboardButton('Улица Сергея Эйзенштейна', callback_data='линияA_УлицаСергеяЭйзенштейна')],
            [InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'линияB': # МЦК
        keyboard = [[InlineKeyboardButton('Автозаводская', callback_data='линияB_Автозаводская'),
            InlineKeyboardButton('Андроновка', callback_data='линияB_Андроновка')],
            [InlineKeyboardButton('Балтийская', callback_data='линияB_Балтийская'),
            InlineKeyboardButton('Белокаменная', callback_data='линияB_Белокаменная')],
            [InlineKeyboardButton('Ботанический сад', callback_data='линияB_БотаническийСад'),
            InlineKeyboardButton('Бульвар Рокоссовского', callback_data='линияB_БульварРокоссовского')],
            [InlineKeyboardButton('Верхние Котлы', callback_data='линияB_ВерхниеКотлы'),
            InlineKeyboardButton('Владыкино', callback_data='линияB_Владыкино')],
            [InlineKeyboardButton('Деловой центр', callback_data='линияB_ДеловойЦентр'),
            InlineKeyboardButton('Дубровка', callback_data='линияB_Дубровка')],
            [InlineKeyboardButton('ЗИЛ', callback_data='линияB_ЗИЛ'),
            InlineKeyboardButton('Зорге', callback_data='линияB_Зорге')],
            [InlineKeyboardButton('Измайлово', callback_data='линияB_Измайлово'),
            InlineKeyboardButton('Коптево', callback_data='линияB_Коптево')],
            [InlineKeyboardButton('Крымская', callback_data='линияB_Крымская'),
            InlineKeyboardButton('Кутузовская', callback_data='линияB_Кутузовская')],
            [InlineKeyboardButton('Лихоборы', callback_data='линияB_Лихоборы'),
            InlineKeyboardButton('Локомотив', callback_data='линияB_Локомотив')],
            [InlineKeyboardButton('Лужники', callback_data='линияB_Лужники'),
            InlineKeyboardButton('Нижегородская', callback_data='линияB_Нижегородская')],
            [InlineKeyboardButton('Новохохловская', callback_data='линияB_Новохохловская'),
            InlineKeyboardButton('Окружная', callback_data='линияB_Окружная')],
            [InlineKeyboardButton('Панфиловская', callback_data='линияB_Панфиловская'),
            InlineKeyboardButton('Площадь Гагарина', callback_data='линияB_ПлощадьГагарина')],
            [InlineKeyboardButton('Ростокино', callback_data='линияB_Ростокино'),
            InlineKeyboardButton('Соколиная Гора', callback_data='линияB_СоколинаяГора')],
            [InlineKeyboardButton('Стрешнево', callback_data='линияB_Стрешнево'),
            InlineKeyboardButton('Угрешская', callback_data='линияB_Угрешская')],
            [InlineKeyboardButton('Хорошёво', callback_data='линияB_Хорошёво'),
            InlineKeyboardButton('Шелепиха', callback_data='линияB_Шелепиха')],
            [InlineKeyboardButton('Шоссе Энтузиастов', callback_data='линияB_ШоссеЭнтузиастов'),
            InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'линияC': # Некрасовская
        keyboard = [[InlineKeyboardButton('Авиамоторная', callback_data='линияC_Авиамоторная'),
            InlineKeyboardButton('Косино', callback_data='линияC_Косино')],
            [InlineKeyboardButton('Лухмановская', callback_data='линияC_Лухмановская'),
            InlineKeyboardButton('Некрасовка', callback_data='линияC_Некрасовка')],
            [InlineKeyboardButton('Нижегородская улица', callback_data='линияC_НижегородскаяУлица'),
            InlineKeyboardButton('Окская улица', callback_data='линияC_ОкскаяУлица')],
            [InlineKeyboardButton('Стахановская', callback_data='линияC_Стахановская'),
            InlineKeyboardButton('улица Дмитриевского', callback_data='линияC_УлицаДмитриевского')],
            [InlineKeyboardButton('Юго-Восточная', callback_data='линияC_ЮгоВосточная'),
            InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'линияD': # Серпуховско-Тимирязевская
        keyboard = [[InlineKeyboardButton('Алтуфьево', callback_data='линияD_Алтуфьево'),
            InlineKeyboardButton('Аннино', callback_data='линияD_Аннино')],
            [InlineKeyboardButton('Бибирево', callback_data='линияD_Бибирево'),
            InlineKeyboardButton('Боровицкая', callback_data='линияD_Боровицкая')],
            [InlineKeyboardButton('Бульвар Дмитрия Донского', callback_data='линияD_БульварДмитрияДонского'),
            InlineKeyboardButton('Владыкино', callback_data='линияD_Владыкино')],
            [InlineKeyboardButton('Дмитровская', callback_data='линияD_Дмитровская'),
            InlineKeyboardButton('Менделеевская', callback_data='линияD_Менделеевская')],
            [InlineKeyboardButton('Нагатинская', callback_data='линияD_Нагатинская'),
            InlineKeyboardButton('Нагорная', callback_data='линияD_Нагорная')],
            [InlineKeyboardButton('Нахимовский проспект', callback_data='линияD_НахимовскийПроспект'),
            InlineKeyboardButton('Отрадное', callback_data='линияD_Отрадное')],
            [InlineKeyboardButton('Петровско-Разумовская', callback_data='линияD_ПетровскоРазумовская'),
            InlineKeyboardButton('Полянка', callback_data='линияD_Полянка')],
            [InlineKeyboardButton('Пражская', callback_data='линияD_Пражская'),
            InlineKeyboardButton('Савёловская', callback_data='линияD_Савёловская')],
            [InlineKeyboardButton('Севастопольская', callback_data='линияD_Севастопольская'),
            InlineKeyboardButton('Серпуховская', callback_data='линияD_Серпуховская')],
            [InlineKeyboardButton('Тимирязевская', callback_data='линияD_Тимирязевская'),
            InlineKeyboardButton('Тульская', callback_data='линияD_Тульская')],
            [InlineKeyboardButton('Улица академика Янгеля', callback_data='линияD_УлицаАкадемикаЯнгеля'),
            InlineKeyboardButton('Цветной бульвар', callback_data='линияD_ЦветнойБульвар')],
            [InlineKeyboardButton('Чертановская', callback_data='линияD_Чертановская'),
            InlineKeyboardButton('Чеховская', callback_data='линияD_Чеховская')],
            [InlineKeyboardButton('Южная', callback_data='линияD_Южная'),
            InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'линияE': # Сокольническая
        keyboard = [[InlineKeyboardButton('Библиотека имени Ленина', callback_data='линияE_БиблиотекаИмениЛенина'),
            InlineKeyboardButton('Бульвар Рокоссовского', callback_data='линияE_БульварРокоссовского')],
            [InlineKeyboardButton('Воробьёвы горы', callback_data='линияE_ВоробьёвыГоры'),
            InlineKeyboardButton('Коммунарка', callback_data='линияE_Коммунарка')],
            [InlineKeyboardButton('Комсомольская', callback_data='линияE_Комсомольская'),
            InlineKeyboardButton('Красносельская', callback_data='линияE_Красносельская')],
            [InlineKeyboardButton('Красные ворота', callback_data='линияE_КрасныеВорота'),
            InlineKeyboardButton('Кропоткинская', callback_data='линияE_Кропоткинская')],
            [InlineKeyboardButton('Лубянка', callback_data='линияE_Лубянка'),
            InlineKeyboardButton('Ольховая', callback_data='линияE_Ольховая')],
            [InlineKeyboardButton('Охотный ряд', callback_data='линияE_ОхотныйРяд'),
            InlineKeyboardButton('Парк культуры', callback_data='линияE_ПаркКультуры')],
            [InlineKeyboardButton('Преображенская площадь', callback_data='линияE_ПреображенскаяПлощадь'),
            InlineKeyboardButton('Прокшино', callback_data='линияE_Прокшино')],
            [InlineKeyboardButton('Проспект Вернадского', callback_data='линияE_ПроспектВернадского'),
            InlineKeyboardButton('Румянцево', callback_data='линияE_Румянцево')],
            [InlineKeyboardButton('Саларьево', callback_data='линияE_Саларьево'),
            InlineKeyboardButton('Сокольники', callback_data='линияE_Сокольники')],
            [InlineKeyboardButton('Спортивная', callback_data='линияE_Спортивная'),
            InlineKeyboardButton('Тропарёво', callback_data='линияE_Тропарёво')],
            [InlineKeyboardButton('Университет', callback_data='линияE_Университет'),
            InlineKeyboardButton('Филатов луг', callback_data='линияE_ФилатовЛуг')],
            [InlineKeyboardButton('Фрунзенская', callback_data='линияE_Фрунзенская'),
            InlineKeyboardButton('Черкизовская', callback_data='линияE_Черкизовская')],
            [InlineKeyboardButton('Чистые пруды', callback_data='линияE_ЧистыеПруды'),
            InlineKeyboardButton('Юго-Западная', callback_data='линияE_ЮгоЗападная')],
            [InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'линияF': # Солнцевская
        keyboard = [[InlineKeyboardButton('Боровское шоссе', callback_data='линияF_БоровскоеШоссе'),
            InlineKeyboardButton('Волхонка', callback_data='линияF_Волхонка')],
            [InlineKeyboardButton('Говорово', callback_data='линияF_Говорово'),
            InlineKeyboardButton('Деловой центр', callback_data='линияF_ДеловойЦентр')],
            [InlineKeyboardButton('Дорогомиловская', callback_data='линияF_Дорогомиловская'),
            InlineKeyboardButton('Ломоносовский проспект', callback_data='линияF_ЛомоносовскийПроспект')],
            [InlineKeyboardButton('Минская', callback_data='линияF_Минская'),
            InlineKeyboardButton('Мичуринский проспект', callback_data='линияF_МичуринскийПроспект')],
            [InlineKeyboardButton('Новопеределкино', callback_data='линияF_Новопеределкино'),
            InlineKeyboardButton('Озерная', callback_data='линияF_Озерная')],
            [InlineKeyboardButton('Очаково', callback_data='линияF_Очаково'),
            InlineKeyboardButton('Парк Победы', callback_data='линияF_ПаркПобеды')],
            [InlineKeyboardButton('Плющиха', callback_data='линияF_Плющиха'),
            InlineKeyboardButton('Раменки', callback_data='линияF_Раменки')],
            [InlineKeyboardButton('Рассказовка', callback_data='линияF_Рассказовка'),
            InlineKeyboardButton('Солнцево', callback_data='линияF_Солнцево')],
            [InlineKeyboardButton('Терешково', callback_data='линияF_Терешково'),
            InlineKeyboardButton('Третьяковская', callback_data='линияF_Третьяковская')],
            [InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'линияG': # Таганско-Краснопресненская
        keyboard = [[InlineKeyboardButton('Баррикадная', callback_data='линияG_Баррикадная'),
            InlineKeyboardButton('Беговая', callback_data='линияG_Беговая')],
            [InlineKeyboardButton('Волгоградский проспект', callback_data='линияG_ВолгоградскийПроспект'),
            InlineKeyboardButton('Выхино', callback_data='линияG_Выхино')],
            [InlineKeyboardButton('Жулебино', callback_data='линияG_Жулебино'),
            InlineKeyboardButton('Китай-город', callback_data='линияG_КитайГород')],
            [InlineKeyboardButton('Котельники', callback_data='линияG_Котельники'),
            InlineKeyboardButton('Кузнецкий мост', callback_data='линияG_КузнецкийМост')],
            [InlineKeyboardButton('Кузьминки', callback_data='линияG_Кузьминки'),
            InlineKeyboardButton('Лермонтовский проспект', callback_data='линияG_ЛермонтовскийПроспект')],
            [InlineKeyboardButton('Октябрьское поле', callback_data='линияG_ОктябрьскоеПоле'),
            InlineKeyboardButton('Планерная', callback_data='линияG_Планерная')],
            [InlineKeyboardButton('Полежаевская', callback_data='линияG_Полежаевская'),
            InlineKeyboardButton('Пролетарская', callback_data='линияG_Пролетарская')],
            [InlineKeyboardButton('Пушкинская', callback_data='линияG_Пушкинская'),
            InlineKeyboardButton('Рязанский проспект', callback_data='линияG_РязанскийПроспект')],
            [InlineKeyboardButton('Спартак', callback_data='линияG_Спартак'),
            InlineKeyboardButton('Сходненская', callback_data='линияG_Сходненская')],
            [InlineKeyboardButton('Таганская', callback_data='линияG_Таганская'),
            InlineKeyboardButton('Текстильщики', callback_data='линияG_Текстильщики')],
            [InlineKeyboardButton('Тушинская', callback_data='линияG_Тушинская'),
            InlineKeyboardButton('Улица 1905 года', callback_data='линияG_Улица1905Года')],
            [InlineKeyboardButton('Щукинская', callback_data='линияG_Щукинская'),
            InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'линияH': # Филёвская
        keyboard = [[InlineKeyboardButton('Александровский сад', callback_data='линияH_АлександровскийСад'),
            InlineKeyboardButton('Арбатская', callback_data='линияH_Арбатская')],
            [InlineKeyboardButton('Багратионовская', callback_data='линияH_Багратионовская'),
            InlineKeyboardButton('Выставочная', callback_data='линияH_Выставочная')],
            [InlineKeyboardButton('Киевская', callback_data='линияH_Киевская'),
            InlineKeyboardButton('Кунцевская', callback_data='линияH_Кунцевская')],
            [InlineKeyboardButton('Кутузовская', callback_data='линияH_Кутузовская'),
            InlineKeyboardButton('Международная', callback_data='линияH_Международная')],
            [InlineKeyboardButton('Пионерская', callback_data='линияH_Пионерская'),
            InlineKeyboardButton('Смоленская', callback_data='линияH_Смоленская')],
            [InlineKeyboardButton('Студенческая', callback_data='линияH_Студенческая'),
            InlineKeyboardButton('Филёвский парк', callback_data='линияH_ФилёвскийПарк')],
            [InlineKeyboardButton('Фили', callback_data='линияH_Фили'),
            InlineKeyboardButton('Назад', callback_data='метро_back')]]

    elif goto == 'ChooseTime':
        keyboard = [[InlineKeyboardButton('10 мин.', callback_data='ChooseTime_10'), 
                        InlineKeyboardButton('20 мин.', callback_data='ChooseTime_20'),
                        InlineKeyboardButton('30 мин.', callback_data='ChooseTime_30')],
                        [InlineKeyboardButton('45 мин.', callback_data='ChooseTime_45'), 
                        InlineKeyboardButton('60 мин.', callback_data='ChooseTime_60'),
                        InlineKeyboardButton('К предыдущему меню', callback_data='ChooseTime_back')]]
    
    elif goto == 'Confirm':  
        keyboard = [[InlineKeyboardButton('Подтвердить', callback_data='Confirm_yes'), 
                     InlineKeyboardButton('Отмена', callback_data='Confirm_cancel')]]
    
    else:
        keyboard = None
    return InlineKeyboardMarkup(keyboard)

# Haversine formula:
def getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2):
    R = 6371 # Radius of the earth in km
    dLat = deg2rad(lat2-lat1) # deg2rad below
    dLon = deg2rad(lon2-lon1) 
    a = (np.sin(dLat/2) * np.sin(dLat/2) +
         np.cos(deg2rad(lat1)) * np.cos(deg2rad(lat2)) * np.sin(dLon/2) * np.sin(dLon/2))
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a)) 
    d = R * c # Distance in km
    return int(d*1000)

def deg2rad(deg):
    return deg * np.pi / 180


def menu_kb2(context):
    latest_matches = get_options(context)
    if latest_matches != 0:
        keyboard = [[InlineKeyboardButton('Новый запрос', callback_data='Searching_cancel'), 
                    InlineKeyboardButton('Обновить', callback_data='Searching_check')]]
        for i, match in enumerate(latest_matches):
            try:
                myloc = context.job.context['mydict']['start_loc']
                hisloc = match['start_loc']
                dist = getDistanceFromLatLonInKm(myloc[1],myloc[0],hisloc[1],hisloc[0])
            except:
                dist = '?'

            caption = "{} выезжает до {}, расст.: {} м".format(match['user_name'],
                                                match['time'].time().strftime("%H:%M"),
                                                dist)
            callback_data = 'SelectMatch_opt{}@{}'.format(match['user_id'], match['user_name'])
            keyboard.append([InlineKeyboardButton(caption, callback_data=callback_data)])
        return latest_matches, InlineKeyboardMarkup(keyboard)
    else:
        return 0, 0
    
def refresh(context: CallbackContext):
    
    if context.job.context['enough'] == True:
        context.job.schedule_removal()
    else:
        message_id = context.job.context['message_id']
        chat_id = context.job.context['chat_id']
        latest_matches, reply_markup = menu_kb2(context)
        if latest_matches != 0:
            text = 'Мы подобрали для вас следующие варианты:' if len(latest_matches) > 0 else '<b>Пока ничего не найдено.</b> \nВы увидите подходящие варианты ниже, как только они появятся базе. Вы также можете сделать запрос на другое время.'
            try:
                out = context.bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                            text = text, #  + str(random.randint(0, 100000))
                                            reply_markup=reply_markup,
                                            parse_mode=telegram.ParseMode.HTML)
                context.user_data['last_message_id'] = out.message_id
            except:
                pass
    
def menu_message(goto, context):
    if goto == 'back':
        context.user_data['caller_stack'].pop()
        goto = context.user_data['caller_stack'][-1]
    elif goto == 'from':
        return "<b>Откуда</b> вы планируете ехать? \n<i>Вы можете отправить адрес ответным сообщением, выбрать точку на карте (нажмите скрепку) или выбрать из списка общественных мест ниже)</i>"
    elif goto == 'to':
        return "Понятно. Вы планируете ехать от <b>{}</b>. Теперь выберите, <b>КУДА</b> Вы планируте ехать. <i> (Или введите адрес в ответном сообщении.</i>)".format(context.user_data['mydict']['start_str'])
    # text = "Вы не связались с выбранным пользователем в течение минуты. Ничего страшного, повторите поиск. Откуда едем?"
    elif goto == 'ВУЗы':          
        return 'Выберите ВУЗ'
    elif goto == 'вокзалы':
        return 'Выберите вокзал'
    elif goto == 'аэропорты':
        return 'Выберите аэропорт'
    elif goto == 'метро':
        return 'Выберите линию'
    elif goto[:-1] == 'линия':
        return 'Выберите станцию'
    elif goto == 'ChooseTime':
        return '<b>Через сколько вы готовы выехать? </b>'
    elif goto == 'Confirm':
        abs_target_time = datetime.datetime.now() + datetime.timedelta(minutes=int(context.user_data['mydict']['time']))
        text = 'Вы планируете ехать от <b>{}</b> до <b>{}</b> через <b>{}</b> минут (т.е. в <b>{}</b>), верно?'.format(
                         context.user_data['mydict']['start_str'],
                         context.user_data['mydict']['target_str'],
                         context.user_data['mydict']['time'],
                         abs_target_time.time().strftime("%H:%M"))
        return text 
    else:
        pass
      
def write2db(update, context):
    mycol = context.user_data['mycol']
    arch = context.user_data['arch']
    query = update.callback_query
    
    now = datetime.datetime.now()
    offset = datetime.timedelta(minutes=int(context.user_data['mydict']['time']))

    context.user_data['mydict']['user_name'] = update.effective_user.first_name
    context.user_data['mydict']['user_id'] = update.effective_user.id
    context.user_data['mydict']['chat_id'] = update.effective_chat.id
    context.user_data['mydict']['time'] = now + offset
    context.user_data['mydict']['engaged'] = False
    context.user_data['mydict']['updated'] = datetime.datetime.now()
    
    
    mydict = context.user_data['mydict']
    myquery = {'user_id': context.user_data['mydict']['user_id']}
    if mycol.count_documents(myquery)==0:
        mycol.insert_one(mydict)
    if mycol.count_documents(myquery)==1:
        newvalues = { "$set": mydict}
        x = mycol.update_one(myquery, newvalues)
    # insert a record into the archive for to do analytics on:
    arch.insert_one(mydict)
    mydict.pop('_id', None) # the command insert modifies the argument (which is weird)
   
def findLatestSelf(context):
    try:
        mycol = context.user_data['mycol']
        myquery = {"user_id": context.user_data['mydict']['user_id']}
    except:
        mycol = context.job.context['mycol']
        myquery = {"user_id": context.job.context['mydict']['user_id']}

    mydoc = mycol.find(myquery).sort( [['_id', -1]] ).limit(1)
    X = []
    for x in mydoc:
        X.append(x)
    try:
        latest = X[0]
    except:
        latest = 0
    return latest

def findMatchOnLatestSelf(context, latest):
    try:
        mycol = context.user_data['mycol']
    except:
        mycol = context.job.context['mycol']

    offset = datetime.timedelta(minutes=10) # +/- 10 minutes of the desired departure
    lb = latest["time"] - offset
    ub = latest["time"] + offset
    # myquery = {"start_loc": latest["start_loc"],
    #            "target_loc":latest["target_loc"],
    #            "time": {"$gte": lb, "$lt": ub},
    #            "user_id": {"$ne": latest["user_id"]},
    #            "engaged": False}
    myquery = {"start_loc.0": {"$gt": latest["start_loc"][0]-0.004},
               "start_loc.1": {"$lt": latest["start_loc"][1]+0.004},
               "target_loc.0": {"$gt": latest["target_loc"][0]-0.04},
               "target_loc.1": {"$lt": latest["target_loc"][1]+0.04},
               "time": {"$gte": lb, "$lt": ub},
               "user_id": {"$ne": latest["user_id"]},
               "engaged": False}
    mydoc = mycol.find(myquery).sort([("time", 1)])
    
    X, U = [], []
    for match in mydoc:
        if match['user_id'] not in U:
            U.append(match['user_id'])
            X.append(match)
    latest_matches = X[-5:] # latest three matches
    return latest_matches

def get_options(context): 
    latest = findLatestSelf(context)
    if latest != 0:
        latest_matches = findMatchOnLatestSelf(context, latest)
    else:
        latest_matches = 0 
    return latest_matches

def reverse_geocode(lng, lat):
    send_text = 'https://geocode-maps.yandex.ru/1.x/?lang=ru_RU&apikey=3fee8092-d268-42df-bba0-bacc4b15ca7f&geocode={},{}'.format(lng, lat)
    response = requests.get(send_text)
    soup = BeautifulSoup(response.text, 'lxml')
    text = soup.select_one('featureMember').select('Formatted')[-1].text.strip()
    return text

def forward_geocode(string):
    send_text = 'https://geocode-maps.yandex.ru/1.x/?lang=ru_RU&apikey=3fee8092-d268-42df-bba0-bacc4b15ca7f&geocode={}'.format(string)
    response = requests.get(send_text)
    soup = BeautifulSoup(response.text, 'lxml')
    text = soup.select_one('featureMember').select('Point')[-1].text.strip()
    coord = [float(i) for i in text.split(' ')]
    lng = coord[0]
    lat = coord[1]
    return lng, lat

def handle_message(update, context):
    lng, lat = forward_geocode(update.message.text)

    print(update.message.message_id)
    print(update.effective_message.message_id)

    context.bot.delete_message(chat_id=update.effective_chat.id,
                                message_id=update.effective_message.message_id)
    # context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    
    if 'from' not in context.user_data['caller_stack']:
        context.user_data['caller_stack'].append('from')
        context.user_data['geolocation'].append((lng, lat))
        context.user_data['mydict']['start_loc'] = (lng, lat)
        context.user_data['mydict']['start_str'] = reverse_geocode(lng, lat)
        caller = 'from'
        goto = 'to'
    else:
        context.user_data['geolocation'].append((lng, lat))
        context.user_data['mydict']['target_loc'] = (lng, lat)
        context.user_data['mydict']['target_str'] = reverse_geocode(lng, lat)
        context.user_data['caller_stack'].append('to')
        caller = 'to'
        goto = 'ChooseTime'
    
    reply_markup = menu_keyboard(goto, context)
    message_id = context.user_data['last_message_id']
    text = menu_message(goto, context)
    out = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                message_id=message_id,
                                text=text,
                                reply_markup=reply_markup,
                                parse_mode=telegram.ParseMode.HTML)
    context.user_data['last_message_id'] = out.message_id
    

def handle_location(update, context):

    print(update.message.message_id)
    lng = update.message.location.longitude
    lat = update.message.location.latitude
    # send_text = 'https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={}&longitude={}&localityLanguage=ru'.format(lat, lng)
    # response = requests.get(send_text)
    # parsed_response = json.loads(response.text)
    # a = parsed_response['localityInfo']['informative'][3]['name']
    # b = parsed_response['localityInfo']['informative'][3]['description']
    # text = '{}, {}'.format(a, b)
    
    print(update.effective_message.message_id)
    context.bot.delete_message(chat_id=update.effective_chat.id,
                                message_id=update.effective_message.message_id)
    # context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    
    if 'from' not in context.user_data['caller_stack']:
        context.user_data['caller_stack'].append('from')
        context.user_data['geolocation'].append((lng, lat))
        context.user_data['mydict']['start_loc'] = (lng, lat)
        context.user_data['mydict']['start_str'] = reverse_geocode(lng, lat)
        caller = 'from'
        goto = 'to'
    else:
        context.user_data['geolocation'].append((lng, lat))
        context.user_data['mydict']['target_loc'] = (lng, lat)
        context.user_data['mydict']['target_str'] = reverse_geocode(lng, lat)
        context.user_data['caller_stack'].append('to')
        caller = 'to'
        goto = 'ChooseTime'
    
    reply_markup = menu_keyboard(goto, context)
    message_id = context.user_data['last_message_id']
    text = menu_message(goto, context)
    out = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                message_id=message_id,
                                text=text,
                                reply_markup=reply_markup,
                                parse_mode=telegram.ParseMode.HTML)
    context.user_data['last_message_id'] = out.message_id




if __name__ == "__main__":
    ############################# Handlers #########################################
    updater = Updater(token='YOUR_TELEGRAM_API_TOKEN', use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.dispatcher.add_handler(MessageHandler(Filters.location, handle_location))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()

    while True:
        time.sleep(4)