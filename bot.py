import json
from os import getenv

import telebot
from dotenv import load_dotenv

import tex

qw3 = ["Производственные работники","Кассиры и операторы на складе","Дорожные рабочие","Операторы по телемаркетингу","Некоторые аспекты медицинской диагностики","Банковские служащие","Программисты для рутинных задач","Автоперевозки (водители грузовиков и таксисты)","Рабочие в сфере обслуживания","Функции бухгалтерии и финансов","Специалисты по технической поддержке","Операторы видеонаблюдения","Работники на складе в электронной коммерции","Разработчики автоматизированных систем","Административные ассистенты","Специалисты по анализу данных"]
user_info = None
try:
    with open('datafile.json', 'r') as f:
        user_info = json.load(f)
except:
    user_info = {}
    with open('datafile.json', 'w') as f:
        json.dump(user_info, f)

load_dotenv()
token = getenv('BOT_TOKEN')

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    bot.send_message(chat_id=message.from_user.id,
                     text=tex.t[message.from_user.language_code]['service']['start'].replace('{}',
                                                                                             message.from_user.first_name))
    global user_info
    user_info[message.from_user.id] = {
        'name': message.from_user.first_name,
        'stage': 'start',
        'answers': {},
        'age': 0
    }
    with open('datafile.json', 'w') as f:
        json.dump(user_info, f)


@bot.message_handler(content_types=['text'])
def send_anketa(message: telebot.types.Message):
    global user_info
    if False:
        pass
    elif user_info[message.from_user.id]['stage'] == 'start':
        bot.send_message(chat_id=message.from_user.id, text=tex.t[message.from_user.language_code]['question']['age'])
        user_info[message.from_user.id]['stage'] = 'get_age'
    elif user_info[message.from_user.id]['stage'] == 'get_age' and message.text.isdigit():
        user_info[message.from_user.id]['age'] = message.text
        bot.send_message(chat_id=message.from_user.id, text=tex.t[message.from_user.language_code]['question'][1])
        user_info[message.from_user.id]['stage'] = 'qw1'
    elif user_info[message.from_user.id]['stage'] == 'qw1' and message.text.isdigit():
        bot.send_message(chat_id=message.from_user.id, text=tex.t[message.from_user.language_code]['question'][2])
        user_info[message.from_user.id]['answers'][1] = message.text
        user_info[message.from_user.id]['stage'] = 'qw2'
    elif user_info[message.from_user.id]['stage'] == 'qw2':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(len(qw3)): markup.add(qw3[i])
        bot.send_message(chat_id=message.from_user.id, text=tex.t[message.from_user.language_code]['question'][3],
                         reply_markup=markup)
        user_info[message.from_user.id]['answers'][2] = message.text
        user_info[message.from_user.id]['stage'] = 'qw3'
    elif user_info[message.from_user.id]['stage'] == 'qw3':
        bot.send_message(chat_id=message.from_user.id, text=tex.t[message.from_user.language_code]['question'][4])
        user_info[message.from_user.id]['answers'][3] = message.text
        user_info[message.from_user.id]['stage'] = 'qw4'
    elif user_info[message.from_user.id]['stage'] == 'qw4' and message.text.isdigit():
        bot.send_message(chat_id=message.from_user.id, text=tex.t[message.from_user.language_code]['question'][5])
        user_info[message.from_user.id]['answers'][4] = message.text
        user_info[message.from_user.id]['stage'] = 'qw5'
    elif user_info[message.from_user.id]['stage'] == 'qw5' and message.text.isdigit():
        bot.send_message(chat_id=message.from_user.id, text=tex.t[message.from_user.language_code]['question'][6])
        user_info[message.from_user.id]['answers'][5] = message.text
        user_info[message.from_user.id]['stage'] = 'qw6'
    elif user_info[message.from_user.id]['stage'] == 'qw6':
        bot.send_message(chat_id=message.from_user.id, text=tex.t[message.from_user.language_code]['question'][7])
        user_info[message.from_user.id]['answers'][6] = message.text
        user_info[message.from_user.id]['stage'] = 'qw7'
    elif user_info[message.from_user.id]['stage'] == 'qw7' and message.text.isdigit():
        bot.send_message(chat_id=message.from_user.id, text=tex.t[message.from_user.language_code]['question'][8])
        user_info[message.from_user.id]['answers'][7] = message.text
        user_info[message.from_user.id]['stage'] = 'qw8'
    elif user_info[message.from_user.id]['stage'] == 'qw8':
        photo = open('./img/enot.png', 'r')
        bot.send_photo(chat_id=message.from_user.id, photo='./img/enot.png',
                       caption=tex.t[message.from_user.language_code]['service']['end'].replace('{}',
                                                                                                message.from_user.first_name))
        photo.close()
        if ((int(user_info[message.from_user.id]['answers'][1]) + int(
                user_info[message.from_user.id]['answers'][2]) + int(user_info[message.from_user]['answers'][3]) + int(
            user_info[message.from_user]['answers'][4])) / 40) * 100 < 50:
            bot.send_message(chat_id=message.from_user.id,
                             text=tex.t[message.from_user.language_code]['answers']['end1'])
        else:
            bot.send_message(chat_id=message.from_user.id, text=tex.t[message.from_user]['answers']['end2'])
        user_info[message.from_user.id]['answers'][8] = message.text
        user_info[message.from_user.id]['stage'] = 'end'
    else:
        bot.send_message(chat_id=message.from_user.id,
                         text=tex.t[message.from_user.language_code]['service']['error'].replace('{}',
                                                                                                 message.from_user.first_name))
    with open('datafile.json', 'w') as f:
        json.dump(user_info, f)


def is_admin(message: telebot.types.Message):
    if message.from_user.id == 6303315695:
        return True
    else:
        return False


@bot.message_handler(commands=['admin'], func=is_admin)
def open_admin():
    with open('datafile.json', 'r') as f:
        user_info = json.load(f)
        bot.send_message(chat_id=6303315695, text=json.dumps(user_info, indent=2))


bot.polling(none_stop=True)
