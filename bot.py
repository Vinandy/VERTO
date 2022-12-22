import telebot
import socket
import client as cl
from telebot import types

"----------------------------------"
port = 4005
host = '192.168.1.52'
server = ('192.168.1.52', 3001)
"----------------------------------"


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(host, port)
s.bind((host, port))



bot = telebot.TeleBot('5942657719:AAHnM1GwJhza0u6FqvH6S4Emv0LdVpqok68')

text_text = ["Введите состояние правой стороны автомобиля(0-5):", "Введите состояние левой стороны автомобиля(0-5):",
"Введите состояние передней части автомобиля(0-5):", "Введите состояние задней части автомобиля(0-5):", "Введите состояние двигателя автомобиля(0-5):",
"Введите состояние подвески автомобиля(0-5):", "Введите состояние фар автомобиля(0-5):", "Введите состояние стекол автомобиля(0-5):",
"Введите состояние электроники автомобиля(0-5):"
             ]
index = 0
name = ''


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    add = types.KeyboardButton('Добавить объявление')
    search = types.KeyboardButton('Поиск объявлений')
    info = types.KeyboardButton('Инструкция')

    markup.add(add, search, info)
    bot.send_message(message.chat.id, "Выберете режим работы: ", reply_markup=markup)


# ------------------------------------------------------------------------------------------------------
# Функция инструкция
@bot.message_handler(commands=["info"])
def info(message):
    mess = f'<b>{message.from_user.first_name}</b>, рады приветствовать тебя в нашем ТГ боте. \n<b>VERTO</b> - cовременный сервис по покупке автомобилей с уникальной системой поиска!\n /start - главное меню'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    start(message)


# ------------------------------------------------------------------------------------------------------
# Функция поиска объявлений
@bot.message_handler(commands=["search"])
def search(message):
    mess = f'<b>{message.from_user.first_name}</b>, ты выбрал <u>режим поиска объявлений!</u>'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.send_message(message.chat.id, 'Введите марку автомобиля: ')
    bot.register_next_step_handler(message, get_name_search)

def get_name_search(message):
    searching = message.text
    # bot.send_message(message.chat.id, name)
    ino = cl.view_market(searching)
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


# ------------------------------------------------------------------------------------------------------
# Функция добавления объявления через выбор кнопок
@bot.message_handler(commands=['add'])
def add(message):
    global name, index
    index = 0
    name = ''
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
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        bot.send_message(callback.message.chat.id, data)
        start(callback.message)
        print(data)
# -----------------------------------------------------------------------------------------------------------------------------


@bot.message_handler(content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"])
def get_user_text(message):
    if message.text == "Добавить объявление":
        add(message)
    elif message.text == "Поиск объявлений":
        search(message)
    elif message.text == "Инструкция":
        info(message)
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю\nВыбери /start или /info", parse_mode='html')
        start(message)





bot.polling(none_stop=True, interval=0)