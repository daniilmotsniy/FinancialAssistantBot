from sqlalchemy import String, Column, Date, Integer
from sqlalchemy.orm import relationship

from backend.db import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True, nullable=False)
    user_name = Column(String, nullable=False)
    user_assets = relationship('Assets', backref='assets', passive_deletes=True)
    registration_date = Column(Date)

    def __init__(self, user_id, user_name, registration_date):
        self.user_id = user_id
        self.user_name = user_name
        self.registration_date = registration_date

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'registration_date': self.registration_date
        }