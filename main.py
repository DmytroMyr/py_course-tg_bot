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
    bot.send_message(message.chat.id, 'Hello, user!')


@bot.message_handler(commands=['dima'])
def dima_func(message):
    bot.send_message(message.chat.id, dima_module.func())


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
    bot.set_webhook(url='https://dashboard.heroku.com/apps/telebot-pycourse/' + TOKEN)
    return "Python Telegram Bot", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
