from flask import jsonify, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from backend.models.assets import Assets
from backend.models.user import User
from backend.db import db
from marshmallow import Schema, fields, ValidationError
from flask import request


class UsersSchema(Schema):
    user_id = fields.String()
    user_name = fields.String()
    user_assets = fields.Field()


class AssetsSchema(Schema):
    user_id = fields.String()
    user_stocks = fields.Field()
    user_currencies = fields.Field()
    user_cryptos = fields.Field()
    user_resources = fields.Field()


user_schema = UsersSchema()
assets_schema = AssetsSchema()


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

        assets_dict = [asset.to_dict() for asset in user.user_assets][0]
        user_dict = user.to_dict()

        user_with_assets = {
            'user_id': user_dict['user_id'],
            'user_name': user_dict['user_name'],
            'user_assets': assets_dict
        }
        return jsonify(user_with_assets)

    @staticmethod
    def put(user_id):
        """
        update the record of user assets
        :return: response message
        """
        old_assets = Assets.query.filter_by(user_id=user_id).first()
        if old_assets:
            session = db.session
            json_data = request.json
            try:
                request_data = user_schema.load(json_data)
            except ValidationError as error:
                return {'Message': error.messages}, 406

            try:
                old_assets.user_stocks = request_data['user_assets']['user_stocks']
                old_assets.user_currencies = request_data['user_assets']['user_currencies']
                old_assets.user_cryptos = request_data['user_assets']['user_cryptos']
                old_assets.user_resources = request_data['user_assets']['user_resources']
                session.commit()
                return {"User was updated with id": user_id}, 204
            except Exception:
                session.rollback()
                return {'Message': 'Internal error occurred'}, 500
            finally:
                session.close()
        else:
            return {'Message': f'No such user with id={user_id}'}, 404

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
        # FIXME assets_dict replace user_cryptos and user_currencies
        for user in users:
            user_dict = user.to_dict()
            assets_dict = [asset.to_dict() for asset in user.user_assets][0]
            user_with_assets.append({
                'user_id': user_dict['user_id'],
                'user_name': user_dict['user_name'],
                'user_assets': assets_dict
            })
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
            try:
                request_data = user_schema.load(json_data)
            except ValidationError as error:
                return {'Message': error.messages}, 406
            new_user = User(request_data['user_id'],
                            request_data['user_name'])
            new_assets = Assets(request_data['user_id'],
                                request_data['user_assets']['user_stocks'],
                                request_data['user_assets']['user_cryptos'],
                                request_data['user_assets']['user_currencies'],
                                request_data['user_assets']['user_resources'],)
            session.add(new_user)
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