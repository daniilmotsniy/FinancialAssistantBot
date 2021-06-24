from flask_restful import Api
# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager
from backend.db import db

from backend.app import app
from backend.api.users_api import UsersApi, UsersApiParam

api = Api(app)
api.add_resource(UsersApi, '/api/v1/users')
api.add_resource(UsersApiParam, '/api/v1/users/<user_id>')

db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
