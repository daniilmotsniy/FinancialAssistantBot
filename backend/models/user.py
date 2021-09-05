from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from backend.db import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True, nullable=False)
    user_name = Column(String, nullable=False)
    user_assets = relationship('Assets', backref='assets', passive_deletes=True)

    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
        }