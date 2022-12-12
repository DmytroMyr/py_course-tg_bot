from flask import Flask, request
import telebot
from telebot import types
import os

import dima_module
import helga_module

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}!\n/help - для довідки')


@bot.message_handler(commands=['help'])
def message_start(message):
    bot.send_message(message.chat.id, f"/movie - пошук фільмів\n/book - для пошук книг")


# ===== DIMA'S FUNCTIONS START =====
user_choices = {}


@bot.message_handler(commands=['dima', 'movie'])
def movie(message):
    bot.send_message(message.chat.id, '''Жанр ['бойовик', 'драма', 'мелодрама', 'фантастика', 'фентезі', 'пригоди', 
            'мультфільм', 'комедія', 'сімейний', 'детектив', 'військовий', 'біографія', 
            'кримінал', 'трилер', 'спорт', 'музика',
            'мюзикл', 'історія', 'аніме', 'вестерн', 'жахи']: ''')
    bot.register_next_step_handler(message, genre_input)


def genre_input(message):
    print(message.text)
    user_choices['genre'] = message.text
    bot.send_message(message.chat.id, 'Рік [2022-2003]: ')
    bot.register_next_step_handler(message, year_input)


def year_input(message):
    print(message.text)
    if message.text.isnumeric():
        user_choices['year'] = message.text
        bot.send_message(message.chat.id, f'Ваш вибір: {user_choices["genre"]}, {user_choices["year"]}')
        result = dima_module.movie_finder(user_choices["genre"], int(user_choices["year"]))
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, 'Невірне введення')
        bot.send_message(message.chat.id, f"/movie - пошук фільмів\n/book - для пошук книг")
        return None


# ===== DIMA'S FUNCTIONS END =====

# ===== HELGA'S FUNCTIONS START =====
selected = {}


@bot.message_handler(['book'])
def get_user_category(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    fiction = types.KeyboardButton('fiction')
    n_fiction = types.KeyboardButton('non-fiction')
    markup.add(fiction, n_fiction)
    bot.send_message(message.chat.id, f"Select category:", reply_markup=markup)
    bot.register_next_step_handler(message, receive_category)


def receive_category(message):
    selected['category'] = message.text
    bot.register_next_step_handler(message, get_user_subcategory)


@bot.message_handler(content_types=['text'])
def get_user_subcategory(message):
    if message.text == 'fiction':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("science fiction")
        btn2 = types.KeyboardButton("fantasy")
        back = types.KeyboardButton("action & adventure")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Select subcategory", reply_markup=markup)
    elif message.text == 'non-fiction':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("biographies")
        btn2 = types.KeyboardButton("history")
        back = types.KeyboardButton("science & nature")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Select subcategory", reply_markup=markup)
    bot.register_next_step_handler(message, receive_subcategory)


def receive_subcategory(message):
    selected['subcategory'] = message.text
    bot.send_message(message.chat.id, f"Search params: {selected['category']} & {selected['subcategory']}")
    result = helga_module.book_commend(selected['category'], selected['subcategory'])
    bot.send_message(message.chat.id, '5 bestselling books for you: ', parse_mode=None)
    bot.send_message(message.chat.id, result)


# ===== HELGA'S FUNCTIONS END =====


bot.polling(none_stop=True)


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot", 200


@app.route('/')
def main():
    bot.remove_webhook()
    bot.set_webhook(url='https://genit-telegrambot.herokuapp.com/' + TOKEN)
    return "Python Telegram Bot", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
