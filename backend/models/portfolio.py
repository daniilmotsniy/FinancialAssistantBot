from sqlalchemy import Column, ForeignKey, String, Integer
from backend.db import db


class Portfolio(db.Model):
    __tablename__ = 'portfolio'

    portfolio_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete='CASCADE'))
    name = Column(String)
    status = Column(String, default='default')

    def __init__(self, user_id, name, status):
        self.user_id = user_id
        self.name = name
        self.status = status

    def to_dict(self):
        return {
            'portfolio_id': self.portfolio_id,
            'user_id': self.user_id,
            'name': self.name,
            'status': self.status,
        }