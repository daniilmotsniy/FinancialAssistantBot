from sqlalchemy import Column, ForeignKey, String, Integer
from backend.db import db


class Asset(db.Model):
    __tablename__ = 'assets'

    asset_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete='CASCADE'))
    ticker = Column(String, nullable=False)
    type_id = Column(Integer)

    def __init__(self, user_id, type_id, ticker):
        self.user_id = user_id
        self.type_id = type_id
        self.ticker = ticker

    def to_dict(self):
        return {
            'asset_id': self.asset_id,
            'user_id': self.user_id,
            'type_id': self.type_id,
            'ticker': self.ticker,
        }