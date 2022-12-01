from flask import Flask, request
import telebot
import os

import dima_module
import helga_module

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}!')


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
    user_choices['year'] = message.text
    bot.send_message(message.chat.id, f'Ваш вибір: {user_choices["genre"]}, {user_choices["year"]}')
    result = dima_module.movie_finder(user_choices["genre"], int(user_choices["year"]))
    bot.send_message(message.chat.id, result)


# ===== DIMA'S FUNCTIONS END =====


@bot.message_handler(commands=['helga'])
def dima_func(message):
    bot.send_message(message.chat.id, helga_module.func())


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot", 200


@app.route('/')
def main():
    bot.remove_webhook()
    bot.set_webhook(url='https://telebot-pycourse.herokuapp.com/' + TOKEN)
    return "Python Telegram Bot", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))