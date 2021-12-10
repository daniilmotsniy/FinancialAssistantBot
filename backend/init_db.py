from models.user import User, db
from models.assets import Asset, AssetTypes, db
from models.portfolio import Portfolio, db

db.create_all()
