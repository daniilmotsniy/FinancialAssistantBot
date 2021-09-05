from sqlalchemy import String, Integer, Column

from backend.db import db


class Admin(db.Model):
    __tablename__ = 'admins'

    admin_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    admin_name = Column(String, nullable=False)
    admin_password = Column(String, nullable=False)

    def __init__(self, admin_name, admin_password):
        self.admin_name = admin_name
        self.admin_password = admin_password

    def to_dict(self):
        return {
            'admin_id': self.admin_id,
            'admin_name': self.admin_name,
            'admin_password': self.admin_password
        }