import json
import logging
from hashlib import sha256

import requests
import telebot
from telebot import types

from telegram_bot.entity.asset_type import AssetTypes
from telegram_bot.public_api.api_runner import Runner

from config import TELEGRAM_BOT_TOKEN, API_URL

""" Bot """
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
logger = logging.getLogger()


@bot.message_handler(commands=["start"])
def start(message):
    # TODO refactor after creating API on BE
    asset_type_labels = [asset_type.label for asset_type
                         in AssetTypes.query.with_entities(AssetTypes.label).all()]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       row_width=len(asset_type_labels))
    buttons = [types.KeyboardButton(label) for label in asset_type_labels]
    markup.add(*buttons)
    say_hello = f"Hello {message.from_user.first_name}!\nI will help" \
                f" you to analyze your financial assets." \
                f" If you want to change assets to your own," \
                f" use command /get_token and then change it via" \
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
    # TODO refactor after creating API on BE
    asset_types = {asset_type.label: asset_type.type_id for asset_type
                   in AssetTypes.query.all()}
    token = sha256(str(message.chat.id).encode('utf-8')).hexdigest()

    if requests.get(API_URL + '/api/v1/users/' + token).status_code == 406:
        logger.log(logging.WARNING, "User not exists!")
    user_assets = requests.get(API_URL + '/api/v1/users/'
                               + token).json()['user_assets']
    asset_id = asset_types[message.text]
    bot.send_message(message.chat.id,
                     f'<pre>'
                     f'{Runner(asset_id, user_assets[asset_id]).generate_response()}'
                     f'</pre>',
                     parse_mode='html')


bot.polling(none_stop=True)
