from sqlalchemy import Column, ForeignKey, String, JSON, Integer
from backend.db import db


class Assets(db.Model):
    __tablename__ = 'assets'

    assets_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete='CASCADE'))
    user_stocks = Column(JSON, nullable=True)
    user_currencies = Column(JSON, nullable=True)
    user_cryptos = Column(JSON, nullable=True)
    user_resources = Column(JSON, nullable=True)

    def __init__(self, user_id, user_stocks, user_currencies, user_cryptos, user_resources):
        self.user_id = user_id
        self.user_stocks = user_stocks
        self.user_currencies = user_currencies
        self.user_cryptos = user_cryptos
        self.user_resources = user_resources

    def to_dict(self):
        return {
            'user_stocks': self.user_stocks,
            'user_currencies': self.user_currencies,
            'user_cryptos': self.user_cryptos,
            'user_resources': self.user_resources,
        }