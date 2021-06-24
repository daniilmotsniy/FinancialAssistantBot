from sqlalchemy import String, Column, JSON
from backend.db import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True, nullable=False)
    user_name = Column(String, nullable=False)
    user_assets = Column(JSON, nullable=True)

    def __init__(self, user_id, user_name, user_assets):
        self.user_id = user_id
        self.user_name = user_name
        self.user_assets = user_assets

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_assets': self.user_assets,
        }