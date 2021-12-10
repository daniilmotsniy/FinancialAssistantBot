from sqlalchemy import Column, ForeignKey, String, Integer, Index
from backend.db import db


class Asset(db.Model):
    __tablename__ = 'assets'

    asset_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete='CASCADE'))
    portfolio_id = Column(Integer, ForeignKey("portfolio.portfolio_id", ondelete='CASCADE'))
    ticker = Column(String, nullable=False)
    count = Column(Integer, default=1)
    type_id = Column(String)

    def __init__(self, user_id, type_id, ticker, count, portfolio_id):
        self.user_id = user_id
        self.type_id = type_id
        self.ticker = ticker
        self.count = count
        self.portfolio_id = portfolio_id

    def to_dict(self):
        return {
            'asset_id': self.asset_id,
            'type_id': self.type_id,
            'ticker': self.ticker,
        }


class AssetTypes(db.Model):
    __tablename__ = 'asset_types'

    type_id = Column(String, primary_key=True)
    label = Column(String, nullable=False)

    def __init__(self, label):
        self.label = label

    def to_dict(self):
        return {
            'type_id': self.type_id,
            'label': self.label,
        }
