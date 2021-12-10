from flask import jsonify, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from backend.db import db
from marshmallow import Schema, fields, ValidationError
from flask import request

from backend.models.assets import Asset
from backend.models.portfolio import Portfolio


class PortfolioSchema(Schema):
    user_id = fields.String()
    name = fields.String()
    status = fields.String()


portfolio_schema = PortfolioSchema()


class PortfoliosApiParam(Resource):
    """
    API endpoints which use parameters for portfolio entity
    """
    @staticmethod
    def get(portfolio_id):
        """
        get the portfolio record
        """
        portfolio = Portfolio.query.filter_by(portfolio_id=portfolio_id).first()
        if not portfolio:
            abort(406, 'This record is absent in database')

        portfolio_with_assets = portfolio.to_dict()
        assets = Asset.query.filter_by(portfolio_id=portfolio_id)
        portfolio_with_assets['assets'] = [asset.to_dict() for asset in assets]

        return jsonify(portfolio_with_assets)

    @staticmethod
    def delete(portfolio_id):
        """
        delete portfolio record
        :return: id of deleted portfolio
        """
        session = db.session
        portfolio = session.query(Portfolio).filter_by(portfolio_id=portfolio_id).first()
        if portfolio is None:
            abort(406, 'This record is absent in database')
        id_ = portfolio.portfolio_id
        session.delete(portfolio)
        session.commit()
        session.close()
        return {"Portfolio was deleted with id": id_}, 200


class PortfoliosApi(Resource):
    """
    API endpoints without parameters for campaign entity
    """

    @staticmethod
    def get():
        """
        get all portfolio records
        """
        return [portfolio.to_dict() for portfolio in Portfolio.query.all()], 200

    @staticmethod
    def post():
        """
        add new portfolio
        :return: id of created portfolio
        """
        session = db.session
        json_data = request.json
        try:
            try:
                request_data = portfolio_schema.load(json_data)
            except ValidationError as error:
                return {'Message': error.messages}, 406
            new_portfolio = Portfolio(request_data['user_id'], request_data['name'],
                                      request_data['status'])
            session.add(new_portfolio)
            session.commit()
            return {"New portfolio was added with id: ": new_portfolio.portfolio_id}, 201
        except IntegrityError as e:
            return {'Error: ': e}, 406
        finally:
            session.close()
