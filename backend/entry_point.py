from flask_restful import Api
from backend.db import db

from backend.app import app
from backend.api.users_api import UsersApi, UsersApiParam
from backend.api.admins_api import AdminsApi, AdminsApiParam

api = Api(app)
api.add_resource(UsersApi, '/api/v1/users')
api.add_resource(UsersApiParam, '/api/v1/users/<user_id>')
api.add_resource(AdminsApi, '/api/v1/admins')
api.add_resource(AdminsApiParam, '/api/v1/admins/<admin_id>')

db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
