import telebot
from telebot import types

from cionmarket_api import get_crypto_data
from nbu_api import get_fiat_data
from finhub_api import get_stock_data

from config import TELEGRAM_BOT_TOKEN

""" Data """
from config import symbol_, ticker_, cc_


""" Bot """
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    currencies_btn = types.KeyboardButton("Currencies")
    crypto_btn = types.KeyboardButton("Crypto")
    stocks_btn = types.KeyboardButton("Stocks")
    markup.add(currencies_btn, crypto_btn, stocks_btn)
    say_hello = f"Hello {message.from_user.first_name}!\nI will help you to analyze your financial assets."
    bot.send_message(message.chat.id, say_hello, reply_markup=markup)


@bot.message_handler(content_types=["text"])
def mess(message):
    get_message = message.text.strip().lower()
    if get_message == "currencies":
        bot.send_message(message.chat.id, f'<pre>{get_fiat_data(cc_)}</pre>', parse_mode='html')
    elif get_message == "crypto":
        bot.send_message(message.chat.id, f'<pre>{get_crypto_data(symbol_)}</pre>', parse_mode='html')
    elif get_message == "stocks":
        bot.send_message(message.chat.id, f'<pre>{get_stock_data(ticker_)}</pre>', parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Sorry, something is wrong. Use buttons or commands.")


bot.polling(none_stop=True)
