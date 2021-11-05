from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models.user import User
from models.assets import Asset
from models.assets import AssetTypes

from db import db
from app import app

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

manager.run()
