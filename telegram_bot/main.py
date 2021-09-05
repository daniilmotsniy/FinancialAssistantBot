import json
from hashlib import sha256

import requests
import telebot
from telebot import types

from cionmarket_api import get_crypto_data
from nbu_api import get_fiat_data
from finhub_api import get_stock_data

from config import TELEGRAM_BOT_TOKEN, API_URL

""" Bot """
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    currencies_btn = types.KeyboardButton("Currencies")
    crypto_btn = types.KeyboardButton("Crypto")
    stocks_btn = types.KeyboardButton("Stocks")
    markup.add(currencies_btn, crypto_btn, stocks_btn)
    say_hello = f"Hello {message.from_user.first_name}!\nI will help you to analyze your financial assets." \
                f" If you want to change assets to your own, use command /get_token and then change it via" \
                f" assistant admin."
    bot.send_message(message.chat.id, say_hello, reply_markup=markup)


@bot.message_handler(commands=["get_token"])
def get_token(message):
    token = sha256(str(message.chat.id).encode('utf-8')).hexdigest()
    data = json.dumps({
        'user_id': token,
        'user_name': message.from_user.first_name,
        'user_assets': {
            'user_stocks': ["AAPL", "MSFT"],
            'user_cryptos': ["BTC", "ETH"],
            'user_currencies': ["USD", "EUR"],
            'user_resources': [],
        }
    })
    try:
        r = requests.get(API_URL + '/api/v1/users/' + token).json()
        if not 'user_id' in r.keys():
            requests.post(API_URL + '/api/v1/users',  headers={"Content-Type": "application/json"}, data=data)
    except Exception as e:
        print(e)
    text = f"Your token is bellow, please don't give it anyone if you want to control your assets by your own." \
           f"\n \n { token }"
    bot.send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(content_types=["text"])
def mess(message):
    get_message = message.text.strip().lower()

    # TODO fix 406 while user making requests without account
    data = requests.get(API_URL + '/api/v1/users/'
                        + str(sha256(str(message.chat.id).encode('utf-8')).hexdigest())).json()

    try:
        currencies = data['user_assets']['user_currencies']
        crypto = data['user_assets']['user_cryptos']
        stocks = data['user_assets']['user_stocks']
    except KeyError:
        currencies = ['USD', 'EUR']
        crypto = ['BTC', 'ETH']
        stocks = ['AAPL', 'MSFT']

    if get_message == "currencies":
        bot.send_message(message.chat.id, f'<pre>{get_fiat_data(currencies)}</pre>', parse_mode='html')
    elif get_message == "crypto":
        bot.send_message(message.chat.id, f'<pre>{get_crypto_data(crypto)}</pre>', parse_mode='html')
    elif get_message == "stocks":
        bot.send_message(message.chat.id, f'<pre>{get_stock_data(stocks)}</pre>', parse_mode='html')


bot.polling(none_stop=True)
