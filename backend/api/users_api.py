from datetime import date

from flask import jsonify, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from backend.models.assets import Asset
from backend.models.user import User

from backend.db import db
from marshmallow import Schema, fields, ValidationError
from flask import request


class UsersSchema(Schema):
    user_id = fields.String()
    user_name = fields.String()
    user_assets = fields.Dict()


user_schema = UsersSchema()


class UsersApiParam(Resource):
    """
    API endpoints which use parameters for user entity
    """

    @staticmethod
    def get(user_id):
        """
        get the user record
        """
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            abort(406, 'This record is absent in database')

        user_assets = Asset.query.filter_by(user_id=user_id).all()
        user_dict = user.to_dict()
        user_dict['user_assets'] = [asset.to_dict() for asset in user_assets]
        return jsonify(user_dict)

    @staticmethod
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

    @staticmethod
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


class UsersApi(Resource):
    """
    API endpoints without parameters for campaign entity
    """

    @staticmethod
    def get():
        """
        get all user records
        """
        users = User.query.all()
        user_with_assets = []

        for user in users:
            user_assets = Asset.query.filter_by(user_id=user.user_id).all()
            user_dict = user.to_dict()
            assets_dict = [asset.to_dict() for asset in user_assets]
            user_dict['user_assets'] = assets_dict
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
                            date.today())
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
