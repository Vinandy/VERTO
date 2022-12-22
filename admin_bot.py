import telebot
import socket
import client as cl
from telebot import types

port = 4005

server = ('192.168.1.52', 3001)
#host = '192.168.31.84'
myHostName = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#host = socket.gethostbyname(myHostName)
host = '192.168.1.52'
print(host, port)
s.bind((host, port))

bot = telebot.TeleBot('5872218314:AAEx_66OCWAPu-3TdqF9paefpEY5D0htSjo')

text_text = ["Введите состояние правой стороны автомобиля(0-5):", "Введите состояние левой стороны автомобиля(0-5):",
"Введите состояние передней части автомобиля(0-5):", "Введите состояние задней части автомобиля(0-5):", "Введите состояние двигателя автомобиля(0-5):",
"Введите состояние подвески автомобиля(0-5):", "Введите состояние фар автомобиля(0-5):", "Введите состояние стекол автомобиля(0-5):",
"Введите состояние электроники автомобиля(0-5):"
             ]

name = ''
index = 0

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    view_market = types.KeyboardButton('Показать объявление (О)')
    view_avg = types.KeyboardButton('Показать средние цены')
    add_market = types.KeyboardButton('Добавить объявление')
    add_avg = types.KeyboardButton('Добавить машину (СЦ)')
    delete_market = types.KeyboardButton('Удалить объявление')
    delete_avg = types.KeyboardButton('Удалить машину (СЦ)')
    #view_all = types.KeyboardButton('/view_all')

    markup.add(view_market, view_avg, add_market, add_avg, delete_market, delete_avg)
    bot.send_message(message.chat.id, "Выберете режим работы: ", reply_markup=markup)

# Функция view_market
@bot.message_handler(commands=["view_market"])
def view_market(message):
    mess = f'<b>{message.from_user.first_name}</b>, ты выбрал <u>режим поиска объявлений!</u>'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.send_message(message.chat.id, 'Введите марку автомобиля: ')
    bot.register_next_step_handler(message, get_name_search)

def get_name_search(message):
    namee = message.text
    # bot.send_message(message.chat.id, name)
    ino = cl.view_market(namee)
    s.sendto(ino.encode('utf-8'), server)
    data, addr = s.recvfrom(4294967296)
    data = data.decode('utf-8')
    por = ""
    count = 0
    for i in range(len(data)):
        if data[i] == ";" and count == 50:
            bot.send_message(message.chat.id, por)
            por = ""
            count = 0
        elif data[i] == ";":
            por += "\n"
            count += 1
        else:
            por += data[i]
    if por != "":
        bot.send_message(message.chat.id, por)
    start(message)
    #print(por)


# Функция view_avg
@bot.message_handler(commands=["view_avg"])
def view_avg(message):
    mess = f'<b>{message.from_user.first_name}</b>, ты выбрал <u>режим просмотра базы средних цен!</u>'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    ino = cl.view_avg()
    s.sendto(ino.encode('utf-8'), server)
    data, addr = s.recvfrom(4294967296)
    data = data.decode('utf-8')
    por = ""
    count = 0
    for i in range(len(data)):
        if data[i] == ";" and count == 50:
            bot.send_message(message.chat.id, por)
            por = ""
            count = 0
        elif data[i] == ";":
            por += "\n"
            count += 1
        else:
            por += data[i]
    if por != "":
        bot.send_message(message.chat.id, por)
    start(message)
    # print(por)


# Функция add_market
@bot.message_handler(commands=['add_market'])
def add_market(message):
    global name, index
    name = ''
    index = 0
    mess = f'<b>{message.from_user.first_name}</b>, ты выбрал <u>режим добавления объявления!</u>'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.send_message(message.chat.id, 'Введите модель: ')
    bot.register_next_step_handler(message, get_model_add)

def get_model_add(message):
    global name
    name += message.text + ';'
    #bot.send_message(message.chat.id, name)
    bot.send_message(message.chat.id, 'Введите цену: ')
    bot.register_next_step_handler(message, get_price_add)

def get_price_add(message):
    global name
    name += message.text + ';'
    #bot.send_message(message.chat.id, name)
    bot.send_message(message.chat.id, 'Введите пробег: ')
    bot.register_next_step_handler(message, get_mileage_add)

def get_mileage_add(message):
    global name
    name += message.text + ';'
    #bot.send_message(message.chat.id, name)
    choose_0_5(message)

def choose_0_5(message):
    global index, text_text
    index += 1
    kb = types.InlineKeyboardMarkup(row_width=3)
    btn0 = types.InlineKeyboardButton(text='0', callback_data='0')
    btn1 = types.InlineKeyboardButton(text='1', callback_data='1')
    btn2 = types.InlineKeyboardButton(text='2', callback_data='2')
    btn3 = types.InlineKeyboardButton(text='3', callback_data='3')
    btn4 = types.InlineKeyboardButton(text='4', callback_data='4')
    btn5 = types.InlineKeyboardButton(text='5', callback_data='5')
    kb.add(btn0, btn1, btn2, btn3, btn4, btn5)

    bot.send_message(message.chat.id, text_text[index-1], reply_markup=kb)

@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    global name, index
    name += callback.data + ';'
    bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.message_id, text="Принято!")
    #bot.send_message(callback.message.chat.id, name)
    if index < 9:
            choose_0_5(callback.message)
    else:
        ino = cl.add_market(name)
        name = ''
        index = 0
        s.sendto(ino.encode('utf-8'), server)
        data, addr = s.recvfrom(4294967296)
        data = data.decode('utf-8')
        bot.send_message(callback.message.chat.id, data)
        start(callback.message)
        print(data)


# Функция add_avg
@bot.message_handler(commands=['add_avg'])
def add_avg(message):
    mess = f'<b>{message.from_user.first_name}</b>, ты выбрал <u>режим добавления машины в базу средних цен!</u>'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.send_message(message.chat.id, 'Введите модель: ')
    bot.register_next_step_handler(message, get_model_avg)

def get_model_avg(message):
    namee = message.text + ';'
    #bot.send_message(message.chat.id, name)
    bot.send_message(message.chat.id, 'Введите цену: ')
    bot.register_next_step_handler(message, get_price_avg, namee)

def get_price_avg(message, namee):
    namee += message.text + ';'
    #bot.send_message(message.chat.id, name)
    ino = cl.add_avg(namee)
    s.sendto(ino.encode('utf-8'), server)
    data, addr = s.recvfrom(4294967296)
    data = data.decode('utf-8')
    bot.send_message(message.chat.id, data)
    start(message)
    print(data)


# Функция delete_market
@bot.message_handler(commands=["delete_market"])
def delete_market(message):
    mess = f'<b>{message.from_user.first_name}</b>, ты выбрал <u>режим удаления объявления!</u>'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.send_message(message.chat.id, 'Введите ID: ')
    bot.register_next_step_handler(message, get_id_market)

def get_id_market(message):
    namee = message.text
    ino = cl.delete_market(namee)
    s.sendto(ino.encode('utf-8'), server)
    data, addr = s.recvfrom(4294967296)
    data = data.decode('utf-8')
    bot.send_message(message.chat.id, data)
    start(message)
    print(data)


# Функция delete_avg
@bot.message_handler(commands=["delete_avg"])
def delete_avg(message):
    mess = f'<b>{message.from_user.first_name}</b>, ты выбрал <u>режим удаления машины из базы средних цен!</u>'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.send_message(message.chat.id, 'Введите Марку машины: ')
    bot.register_next_step_handler(message, get_del_avg)

def get_del_avg(message):
    namee = message.text
    ino = cl.delete_avg(namee)
    s.sendto(ino.encode('utf-8'), server)
    data, addr = s.recvfrom(4294967296)
    data = data.decode('utf-8')
    bot.send_message(message.chat.id, data)
    start(message)
    print(data)

"""
# Функция view_all
@bot.message_handler(commands=["view_all"])
def view_all(message):
    mess = f'<b>{message.from_user.first_name}</b>, ты выбрал <u>режим просмотра всех объявлений!</u>'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    ino = cl.view_all()
    name = ''
    s.sendto(ino.encode('utf-8'), server)
    data, addr = s.recvfrom(4294967296)
    data = data.decode('utf-8')
    por = ""
    for i in range(len(data)):
        if data[i] == ";":
            por += '\n'
        else:
            por += data[i]
    bot.send_message(message.chat.id, por)
    start(message)
    # print(por)
"""

@bot.message_handler(content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"])
def get_user_text(message):
    if message.text == 'Показать объявление (О)':
        view_market(message)
    elif message.text == 'Показать средние цены':
        view_avg(message)
    elif message.text == 'Добавить объявление':
        add_market(message)
    elif message.text == 'Добавить машину (СЦ)':
        add_avg(message)
    elif message.text == 'Удалить объявление':
        delete_market(message)
    elif message.text == 'Удалить машину (СЦ)':
        delete_avg(message)
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю\nВыбери /start или /info", parse_mode='html')
        start(message)


bot.polling(none_stop=True, interval=0)