from flask_restful import Api
from backend.db import db

from backend.app import app
from backend.api.users_api import UserAssetsApi, UsersAssetsApiParam, UsersDataApiParam, UsersAssetsTokenApiParam
from backend.api.admins_api import AdminsApi, AdminsApiParam
from backend.api.assets_api import AssetsApi, AssetsApiParam, AssetTypesApi

api = Api(app)
api.add_resource(UserAssetsApi, '/api/v1/users')
api.add_resource(UsersAssetsApiParam, '/api/v1/users/<user_id>')
api.add_resource(AdminsApi, '/api/v1/admins')
api.add_resource(AdminsApiParam, '/api/v1/admins/<admin_id>')
api.add_resource(AssetsApi, '/api/v1/assets')
api.add_resource(AssetsApiParam, '/api/v1/assets/<type_id>/<ticker>')
api.add_resource(AssetTypesApi, '/api/v1/asset_types')
api.add_resource(UsersDataApiParam, '/api/v1/users/data/<user_id>')
api.add_resource(UsersAssetsTokenApiParam, '/api/v1/users/token/<token>')


db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
