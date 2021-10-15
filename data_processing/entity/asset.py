from sqlalchemy import Column, String, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base


class Asset(declarative_base()):
    __tablename__ = 'assets'

    assets_id = Column(Integer, primary_key=True)
    user_id = Column(String)
    user_stocks = Column(JSON)
    user_cryptos = Column(JSON)
    user_currencies = Column(JSON)
    user_resources = Column(JSON)