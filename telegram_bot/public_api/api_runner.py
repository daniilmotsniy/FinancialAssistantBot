from telegram_bot.public_api.nbu_api import CurrenciesApi
from telegram_bot.public_api.finhub_api import StocksApi
from telegram_bot.public_api.cionmarket_api import CryptoApi

mapper = {
    'user_stocks': StocksApi,
    'user_cryptos': CryptoApi,
    'user_currencies': CurrenciesApi,
}


class Runner:
    def __init__(self, asset_id, tickers):
        self.asset_id = asset_id
        self.tickers = tickers

    def generate_response(self):
        return mapper[self.asset_id]().get_table(self.tickers)