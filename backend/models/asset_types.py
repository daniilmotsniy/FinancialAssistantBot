from sqlalchemy import Column, String
from backend.db import db


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