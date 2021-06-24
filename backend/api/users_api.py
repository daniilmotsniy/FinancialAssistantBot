from hashlib import sha256

from flask import jsonify, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from backend.models.user import User
from backend.db import db
from marshmallow import Schema, fields, ValidationError
from flask import request


class UsersSchema(Schema):
    user_id = fields.String()
    user_name = fields.String()
    user_assets = fields.Field()


user_schema = UsersSchema()


class UsersApiParam(Resource):
    """
    API endpoints which use parameters for user entity
    """

    @staticmethod
    def get(user_id):
        """
        get the record of the users by user_id
        :param user_id: id of user
        :return: json of user
        """
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            abort(406, 'This record is absent in database')
        return jsonify(**user.to_dict())

    @staticmethod
    def put(user_id):
        """
        update the record of the user by user_id
        :param user_id: id of  user
        :return: json of user
        """
        user = User.query.filter_by(user_id=user_id).first()

        if user:
            session = db.session
            json_data = request.json
            try:
                request_data = user_schema.load(json_data)
            except ValidationError as error:
                return {'Message': error.messages}, 406

            try:
                user.user_assets = request_data['user_assets']
                session.commit()
                return {"User was updated with id": user_id}, 204
            except Exception as e:
                session.rollback()
                print(e)
                return {'Message': 'Internal error occurred'}, 500
            finally:
                session.close()
        else:
            return {'Message': f'No such user with id={user_id}'}, 404

    @staticmethod
    def delete(user_id):
        """
        delete the record of the user
        :param user_id: id of the user
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
        get all records from the table
        :return: json of all records
        """
        users = User.query.all()
        all_users = []
        for campaign in users:
            all_users.append(
                {**campaign.to_dict()}
            )
        return all_users, 200

    @staticmethod
    def post():
        """
        add new user to the table
        :return: id of created user
        """
        session = db.session
        json_data = request.json
        try:
            try:
                request_data = user_schema.load(json_data)
            except ValidationError as error:
                return {'Message': error.messages}, 406
            new_user = User(request_data['user_id'], request_data['user_name'], request_data['user_assets'])
            session.add(new_user)
            session.commit()
            return {"New user was added with id": new_user.user_id}, 201
        except IntegrityError as e:
            print(e)
            return {'Message': e}, 406
        except AttributeError as e:
            print(e)
            return {'Message': e}, 406
        except Exception as e:
            return {'Message': e}, 500
        finally:
            session.close()