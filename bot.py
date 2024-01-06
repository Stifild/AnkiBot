import json
from os import getenv

import telebot
from dotenv import load_dotenv

import tex

try:
    with open('datafile.json', 'rb') as f:
        user_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    user_info = {}

clean_markup = telebot.types.ReplyKeyboardRemove()

load_dotenv()
token = getenv('BOT_TOKEN')

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    if str(message.from_user.id) in user_info.keys() and user_info[str(message.from_user.id)]['stage'] != 'end':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(tex.t[message.from_user.language_code]['answers']['yes'],
                   tex.t[message.from_user.language_code]['answers']['no'])
        bot.send_message(chat_id=message.chat.id, text=tex.t[message.from_user.language_code]['answers']['resume'],
                         reply_markup=markup)
        user_info[str(message.from_user.id)]['resume'] = True
    else:
        send_welcome(message)


def send_welcome(message: telebot.types.Message):
    bot.send_message(chat_id=message.from_user.id,
                     text=tex.t[message.from_user.language_code]['service']['start'].replace('{}',
                                                                                             message.from_user.first_name))
    global user_info
    user_info[str(message.from_user.id)] = {
        'name': message.from_user.first_name,
        'stage': 'start',
        'age': -1,
        'resume': False,
        'answers': {},

    }
    with open('datafile.json', 'w', encoding='utf-8') as f:
        json.dump(user_info, f, ensure_ascii=False, indent=3)


@bot.message_handler(commands=['stop_bot'])
def stop_bot(message: telebot.types.Message):
    bot.send_message(chat_id=6303315695, text=f'Произведен запрос остановки бота от {message.from_user.id}')
    if message.from_user.id == 6303315695:
        bot.send_message(chat_id=6303315695, text='BOT STOP!!!')
        telebot.TeleBot.stop_bot()
    else:
        bot.send_message(chat_id=message.from_user.id, text='В доступе отказано!')


@bot.message_handler(commands=['admin'])
def open_admin(message: telebot.types.Message):
    bot.send_message(chat_id=6303315695, text=f'Произведен запрос ответов от {message.from_user.id}')
    if message.from_user.id == 6303315695:
        for i in range(len(json.dumps(user_info, indent=3)) // 4096):
            bot.send_message(chat_id=6303315695, text=json.dumps(user_info, indent=3)[i * 4096:i * 4096 + 4096],
                             protect_content=True)
    else:
        bot.send_message(chat_id=message.from_user.id, text='В доступе отказано!')


@bot.message_handler(content_types=['text'])
def send_anketa(message: telebot.types.Message):
    global user_info
    if user_info[str(message.from_user.id)]['resume']:
        if message.text.lower() == 'yes' or message.text.lower() == 'да':
            bot.send_message(chat_id=message.chat.id,
                             text=tex.t[message.from_user.language_code]['answers']['resume_yes'],
                             reply_markup=clean_markup)
            user_info[str(message.from_user.id)]['resume'] = False
        else:
            bot.send_message(chat_id=message.chat.id,
                             text=tex.t[message.from_user.language_code]['answers']['resume_no'],
                             reply_markup=clean_markup)
            user_info[str(message.from_user.id)]['resume'] = False
            send_welcome(message)
    elif user_info[str(message.from_user.id)]['stage'] == 'start':
        bot.send_message(chat_id=message.from_user.id,
                         text=tex.t[message.from_user.language_code]['question']['age'])
        user_info[str(message.from_user.id)]['stage'] = 'get_age'
    elif user_info[str(message.from_user.id)]['stage'] == 'get_age' and message.text.isdigit():
        user_info[str(message.from_user.id)]['age'] = message.text
        bot.send_message(chat_id=message.from_user.id,
                         text=tex.t[message.from_user.language_code]['question'][1])
        user_info[str(message.from_user.id)]['stage'] = 'qw1'
    elif user_info[str(message.from_user.id)]['stage'] == 'qw1' and message.text.isdigit():
        bot.send_message(chat_id=message.from_user.id,
                         text=tex.t[message.from_user.language_code]['question'][2])
        user_info[str(message.from_user.id)]['answers']['1'] = message.text
        user_info[str(message.from_user.id)]['stage'] = 'qw2'
    elif user_info[str(message.from_user.id)]['stage'] == 'qw2':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(len(tex.t[message.from_user.language_code]['answers'][3])): markup.add(
            tex.t[message.from_user.language_code]['answers'][3][i])
        bot.send_message(chat_id=message.from_user.id,
                         text=tex.t[message.from_user.language_code]['question'][3],
                         reply_markup=markup)
        user_info[str(message.from_user.id)]['answers']['2'] = message.text
        user_info[str(message.from_user.id)]['stage'] = 'qw3'
    elif user_info[str(message.from_user.id)]['stage'] == 'qw3':
        bot.send_message(chat_id=message.from_user.id,
                         text=tex.t[message.from_user.language_code]['question'][4], reply_markup=clean_markup)
        user_info[str(message.from_user.id)]['answers']['3'] = message.text
        user_info[str(message.from_user.id)]['stage'] = 'qw4'
    elif user_info[str(message.from_user.id)]['stage'] == 'qw4' and message.text.isdigit():
        bot.send_message(chat_id=message.from_user.id,
                         text=tex.t[message.from_user.language_code]['question'][5])
        user_info[str(message.from_user.id)]['answers']['4'] = message.text
        user_info[str(message.from_user.id)]['stage'] = 'qw5'
    elif user_info[str(message.from_user.id)]['stage'] == 'qw5' and message.text.isdigit():
        bot.send_message(chat_id=message.from_user.id,
                         text=tex.t[message.from_user.language_code]['question'][6])
        user_info[str(message.from_user.id)]['answers']['5'] = message.text
        user_info[str(message.from_user.id)]['stage'] = 'qw6'
    elif user_info[str(message.from_user.id)]['stage'] == 'qw6':
        bot.send_message(chat_id=message.from_user.id,
                         text=tex.t[message.from_user.language_code]['question'][7])
        user_info[str(message.from_user.id)]['answers']['6'] = message.text
        user_info[str(message.from_user.id)]['stage'] = 'qw7'
    elif user_info[str(message.from_user.id)]['stage'] == 'qw7' and message.text.isdigit():
        bot.send_message(chat_id=message.from_user.id,
                         text=tex.t[message.from_user.language_code]['question'][8])
        user_info[str(message.from_user.id)]['answers']['7'] = message.text
        user_info[str(message.from_user.id)]['stage'] = 'qw8'
    elif user_info[str(message.from_user.id)]['stage'] == 'qw8':
        with open('img/enot.png', 'rb') as photo:
            bot.send_photo(chat_id=message.from_user.id, photo=photo,
                           caption=tex.t[message.from_user.language_code]['service']['end'].replace('{}',
                                                                                                    message.from_user.first_name))

        if ((int(user_info[str(message.from_user.id)]['answers']['1']) + int(
                user_info[str(message.from_user.id)]['answers']['4']) + int(
            user_info[str(message.from_user.id)]['answers']['5']) + int(
            user_info[str(message.from_user.id)]['answers']['7'])) / 40) * 100 < 50:
            bot.send_message(chat_id=message.from_user.id,
                             text=tex.t[message.from_user.language_code]['answers']['end1'])
        else:
            bot.send_message(chat_id=message.from_user.id,
                             text=tex.t[message.from_user.language_code]['answers']['end2'])
        user_info[str(message.from_user.id)]['answers']['8'] = message.text
        user_info[str(message.from_user.id)]['stage'] = 'end'
    else:
        bot.send_message(chat_id=message.from_user.id,
                         text=tex.t[message.from_user.language_code]['service']['error'].replace('{}',
                                                                                                 message.from_user.first_name))
    with open('datafile.json', 'w', encoding='utf-8') as f:
        json.dump(user_info, f, ensure_ascii=False, indent=3)


bot.infinity_polling(timeout=8)
