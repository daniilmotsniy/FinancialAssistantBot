from models.user import User, db
from models.assets import Asset, db
from models.asset_types import AssetTypes, db

db.create_all()
