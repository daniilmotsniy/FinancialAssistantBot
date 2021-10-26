import json
import logging
from hashlib import sha256

import requests
import telebot
from telebot import types

from telegram_bot.entity.asset_type import AssetTypes

from telegram_bot.public_api.cionmarket_api import get_crypto_data
from telegram_bot.public_api.nbu_api import get_fiat_data
from telegram_bot.public_api.finhub_api import get_stock_data

from config import TELEGRAM_BOT_TOKEN, API_URL

""" Bot """
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
logger = logging.getLogger()


@bot.message_handler(commands=["start"])
def start(message):
    asset_type_labels = [asset_type.label for asset_type
                         in AssetTypes.query.with_entities(AssetTypes.label).all()]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       row_width=len(asset_type_labels))
    buttons = [types.KeyboardButton(label) for label in asset_type_labels]
    markup.add(*buttons)
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
    if requests.get(API_URL + '/api/v1/users/' + token).status_code == 406:
        try:
            requests.post(API_URL + '/api/v1/users',
                          headers={"Content-Type": "application/json"},
                          data=data)
        except Exception as e:
            logger.log(logging.ERROR, f"Error: {e}")
    text = f"Your token is bellow, please don't give it anyone if you want" \
           f" to control your assets by your own." \
           f"\n \n {token}"
    bot.send_message(message.chat.id, text,
                     parse_mode='html')


@bot.message_handler(content_types=["text"])
def mess(message):
    get_message = message.text.strip().lower()
    token = sha256(str(message.chat.id).encode('utf-8')).hexdigest()
    if requests.get(API_URL + '/api/v1/users/' + token).status_code == 406:
        logger.log(logging.WARNING, "User not exists!")
    user_assets = requests.get(API_URL + '/api/v1/users/' + token).json()['user_assets']

    if get_message == 'cryptos':
        bot.send_message(message.chat.id, f'<pre>{get_crypto_data(user_assets["user_cryptos"])}</pre>',
                         parse_mode='html')
    if get_message == 'currencies':
        bot.send_message(message.chat.id, f'<pre>{get_fiat_data(user_assets["user_currencies"])}</pre>',
                         parse_mode='html')
    if get_message == 'stocks':
        bot.send_message(message.chat.id, f'<pre>{get_stock_data(user_assets["user_stocks"])}</pre>',
                         parse_mode='html')


bot.polling(none_stop=True)
