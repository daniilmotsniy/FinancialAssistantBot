from collections import defaultdict
from datetime import date

from flask import jsonify, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from backend.auth.token_verify import token_required
from backend.models.assets import Asset
from backend.models.user import User

from backend.db import db
from marshmallow import Schema, fields, ValidationError
from flask import request


class UsersSchema(Schema):
    user_id = fields.String()
    user_name = fields.String()
    user_assets = fields.Dict()


class UserDataSchema(Schema):
    token = fields.String()


user_schema = UsersSchema()
user_data_schema = UserDataSchema()


class UsersAssetsApiParam(Resource):
    """
    API endpoints which use parameters for user entity
    """

    @staticmethod
    @token_required
    def get(user_id):
        """
        get the user record
        """
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            session = db.session
            new_user = User(user_id, None, date.today(), None)
            session.add(new_user)
            session.commit()
            user = new_user
        user_assets = Asset.query.with_entities(Asset.type_id,
                                                Asset.ticker).filter_by(user_id=user_id).all()
        user_dict = user.to_dict()
        assets_with_type = defaultdict(lambda: [])
        for asset in user_assets:
            assets_with_type[asset.type_id].append(asset.ticker)

        user_dict['user_assets'] = assets_with_type
        return jsonify(user_dict)

    @staticmethod
    @token_required
    def put(user_id):
        """
        update the record of user assets
        :return: response message
        """
        old_assets = Asset.query.filter_by(user_id=user_id).all()
        if not old_assets:
            return {'Message': f'No such user with id={user_id}'}, 404

        session = db.session
        json_data = request.json

        try:
            request_data = user_schema.load(json_data)
        except ValidationError as error:
            return {'Message': error.messages}, 406

        old_assets_tickers = [asset.ticker for asset in old_assets]

        try:
            for asset in old_assets:
                if asset.ticker not in request_data['user_assets'][str(asset.type_id)]:
                    session.delete(asset)

            for asset_type_id, asset_tickers in request_data['user_assets'].items():
                for ticker in asset_tickers:
                    if ticker not in old_assets_tickers:
                        new_asset = Asset(user_id,
                                          asset_type_id,
                                          ticker)
                        session.add(new_asset)
            session.commit()
            return {"User was updated with id": user_id}, 204
        except Exception:
            session.rollback()
            return {'Message': 'Internal error occurred'}, 500
        finally:
            session.close()


class UserAssetsApi(Resource):
    """
    API endpoints without parameters for campaign entity
    """

    @staticmethod
    @token_required
    def get():
        """
        get all user records
        """
        users = User.query.all()
        user_with_assets = []

        for user in users:
            user_assets = Asset.query.filter_by(user_id=user.user_id).all()
            user_dict = user.to_dict()
            assets_with_type = defaultdict(lambda: [])
            for asset in user_assets:
                assets_with_type[asset.type_id].append(asset.ticker)
            user_dict['user_assets'] = assets_with_type
            user_with_assets.append(user_dict)
        return user_with_assets, 200

    @staticmethod
    def post():
        """
        add new user
        :return: id of created user
        """
        session = db.session
        json_data = request.json
        try:
            request_data = user_schema.load(json_data)
        except ValidationError as error:
            return {'Message': error.messages}, 406
        try:
            new_user = User(request_data['user_id'],
                            request_data['user_name'],
                            date.today(), None)
            session.add(new_user)
            session.commit()
            for asset_type_id, asset_tickers in request_data['user_assets'].items():
                for ticker in asset_tickers:
                    new_assets = Asset(request_data['user_id'],
                                       asset_type_id,
                                       ticker)
                    session.add(new_assets)
            session.commit()
            return {"New user was added with id": new_user.user_id}, 201
        except IntegrityError as e:
            return {'Message': e}, 406
        except AttributeError as e:
            return {'Message': e}, 406
        except Exception as e:
            return {'Message': e}, 500
        finally:
            session.close()


class UsersDataApiParam(Resource):
    """
    API endpoints which use parameters for user entity
    """
    @staticmethod
    @token_required
    def get(user_id):
        """
        get the user record
        """
        user = User.query.filter_by(user_id=user_id).first()
        return jsonify(user.to_dict())

    @staticmethod
    @token_required
    def put(user_id):
        """
        update the record of user assets
        :return: response message
        """
        session = db.session
        json_data = request.json

        try:
            request_data = user_data_schema.load(json_data)
        except ValidationError as error:
            return {'Message': error.messages}, 406

        try:
            user = session.query(User).get(user_id)
            user.token = request_data['token']
            session.commit()
            return {"User was updated with id": user_id}, 204
        except Exception:
            session.rollback()
            return {'Message': 'Internal error occurred'}, 500
        finally:
            session.close()

    @staticmethod
    @token_required
    def delete(user_id):
        """
        delete user record
        :return: id of deleted user
        """
        session = db.session
        user = session.query(User).get(user_id)
        if user is None:
            abort(406, 'This record is absent in database')
        id_ = user_id
        session.delete(user)
        session.commit()
        session.close()
        return {"User was deleted with id": id_}, 200


class UsersAssetsTokenApiParam(Resource):
    """
    API endpoints which use parameters for user entity
    """

    @staticmethod
    def get(token):
        user = User.query.filter_by(token=token).first()
        user_assets = Asset.query.with_entities(Asset.type_id,
                                                Asset.ticker).filter_by(user_id=user.user_id).all()
        user_dict = user.to_dict()
        assets_with_type = defaultdict(lambda: [])
        for asset in user_assets:
            assets_with_type[asset.type_id].append(asset.ticker)

        user_dict['user_assets'] = assets_with_type
        return jsonify(user_dict)