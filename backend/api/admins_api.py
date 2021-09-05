from hashlib import sha256

from flask import jsonify, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from backend.models.admin import Admin
from backend.db import db
from marshmallow import Schema, fields, ValidationError
from flask import request


class AdminsSchema(Schema):
    admin_name = fields.String()
    admin_password = fields.String()


admin_schema = AdminsSchema()


class AdminsApiParam(Resource):
    """
    API endpoints which use parameters for admin entity
    """

    @staticmethod
    def get(admin_id):
        """
        get the admin record
        """
        admin = Admin.query.filter_by(admin_id=admin_id).first()

        if not admin:
            abort(406, 'This record is absent in database')

        return jsonify(admin.to_dict())

    @staticmethod
    def put(admin_id):
        """
        update the record of admin assets
        :return: response message
        """
        old_admin_data = Admin.query.filter_by(admin_id=admin_id).first()
        if old_admin_data:
            session = db.session
            json_data = request.json
            try:
                request_data = admin_schema.load(json_data)
            except ValidationError as error:
                return {'Message': error.messages}, 406

            try:
                old_admin_data.admin_name = request_data['admin_name']
                new_password = sha256(request_data['admin_password'].encode()).hexdigest()
                old_admin_data.admin_password = new_password
                session.commit()
                return {"Admin was updated with id": admin_id}, 204
            except Exception:
                session.rollback()
                return {'Message': 'Internal error occurred'}, 500
            finally:
                session.close()
        else:
            return {'Message': f'No such admin with id={admin_id}'}, 404

    @staticmethod
    def delete(admin_id):
        """
        delete admin record
        :return: id of deleted admin
        """
        session = db.session
        admin = session.query(Admin).get(admin_id)
        if admin is None:
            abort(406, 'This record is absent in database')
        id_ = admin_id
        session.delete(admin)
        session.commit()
        session.close()
        return {"Admin was deleted with id": id_}, 200


class AdminsApi(Resource):
    """
    API endpoints without parameters for campaign entity
    """
    @staticmethod
    def get():
        """
        get all admin records
        """
        return [admin.to_dict() for admin in Admin.query.all()], 200

    @staticmethod
    def post():
        """
        add new admin
        :return: id of created admin
        """
        session = db.session
        json_data = request.json
        try:
            try:
                request_data = admin_schema.load(json_data)
            except ValidationError as error:
                return {'Message': error.messages}, 406
            new_password = sha256(request_data['admin_password'].encode()).hexdigest()
            new_admin = Admin(request_data['admin_name'], new_password)
            session.add(new_admin)
            session.commit()
            return {"New admin was added with id": new_admin.admin_id}, 201
        except IntegrityError as e:
            return {'Message': e}, 406
        except AttributeError as e:
            return {'Message': e}, 406
        except Exception as e:
            return {'Message': e}, 500
        finally:
            session.close()