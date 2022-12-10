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

books = {
    'fiction': 'science fiction; fantasy; action & adventure',
    'non-fiction': 'biographies; history; science & nature'
}

selection = {}

@bot.message_handler(commands=['helga', 'book'])
def message_books(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)  # create and design keyboard
    categ = list(books.keys())
    categ = ','.join(categ)
    button = telebot.types.InlineKeyboardButton(text=categ.split(','))
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Available categories', reply_markup=keyboard)
    bot.register_next_step_handler(message, category_input)

def category_input(message):
    c_reply = message.text
    selection['category'] = c_reply
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    subcateg = books[c_reply]
    button = telebot.types.InlineKeyboardButton(text=subcateg.split('; '))
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Select subcategory', reply_markup=keyboard)
    bot.register_next_step_handler(message, subcategory_input)


def subcategory_input(message):
    s_reply = message.text
    selection['subcategory'] = s_reply
    bot.send_message(message.chat.id, f"Your preference: {selection['subcategory']}")
    result = helga_module.book_commend(selection['category'], selection['subcategory'])
    bot.send_message(message.chart.id, '5 bestselling books for you:\n', result)

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
