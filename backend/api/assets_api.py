from flask import jsonify, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from backend.models.assets import Asset, AssetTypes
from backend.db import db
from marshmallow import Schema, fields, ValidationError
from flask import request


class AssetsSchema(Schema):
    user_id = fields.String()
    ticker = fields.String()
    type_id = fields.String()


asset_schema = AssetsSchema()


class AssetsApiParam(Resource):
    """
    API endpoints which use parameters for asset entity
    """

    @staticmethod
    def get(type_id, ticker):
        """
        get the asset record
        """
        asset = Asset.query.filter_by(type_id=type_id, ticker=ticker).first()
        if not asset:
            abort(406, 'This record is absent in database')

        asset_type = AssetTypes.query.get(asset.type_id)
        asset_data = asset.to_dict()
        asset_data['type_id'] = asset_type.label
        return jsonify(asset_data)

    @staticmethod
    def delete(type_id, ticker):
        """
        delete asset record
        :return: id of deleted asset
        """
        session = db.session
        asset = session.query(Asset).filter_by(type_id=type_id, ticker=ticker).first()
        if asset is None:
            abort(406, 'This record is absent in database')
        id_ = asset.asset_id
        session.delete(asset)
        session.commit()
        session.close()
        return {"Asset was deleted with id": id_}, 200


class AssetsApi(Resource):
    """
    API endpoints without parameters for campaign entity
    """

    @staticmethod
    def get():
        """
        get all asset records
        """
        return [asset.to_dict() for asset in Asset.query.all()], 200

    @staticmethod
    def post():
        """
        add new asset
        :return: id of created asset
        """
        session = db.session
        json_data = request.json
        try:
            try:
                request_data = asset_schema.load(json_data)
            except ValidationError as error:
                return {'Message': error.messages}, 406

            old_asset = Asset.query.with_entities(Asset.asset_id).filter_by(user_id=request_data['user_id'],
                                                                            ticker=request_data['ticker'],
                                                                            type_id=request_data['type_id']).first()
            if not old_asset:
                new_asset = Asset(request_data['user_id'], request_data['type_id'],
                                  request_data['ticker'])
                session.add(new_asset)
                session.commit()
                return {"New asset was added with id: ": new_asset.asset_id}, 201
            else:
                return {"You already have such asset with id: ": old_asset.asset_id}, 200
        except IntegrityError as e:
            return {'Error: ': e}, 406
        finally:
            session.close()


class AssetTypesApi(Resource):
    """
    API endpoints without parameters for campaign entity
    """

    @staticmethod
    def get():
        """
        get all asset types records
        """
        return [asset_type.to_dict() for asset_type in AssetTypes.query.all()], 200
