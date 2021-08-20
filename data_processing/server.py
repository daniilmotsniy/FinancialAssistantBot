from fastapi import FastAPI
from graphene import ObjectType, Schema, String, Field, List
from starlette.graphql import GraphQLApp

from entities.assets_analytics import AssetsAnalytics
from helpers.constants import DB_BACKUP_CSV_PATH
from graph.graph_entities import AssetsCount, LabelCount

app = FastAPI()

assets_analytics = AssetsAnalytics(DB_BACKUP_CSV_PATH)


class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))
    assets_count = Field(AssetsCount)
    asset_count = List(LabelCount, asset=String(required=True))

    def resolve_assets_count(self, info):
        return assets_analytics.assets_total_count()

    def resolve_asset_count(self, info, asset):
        return assets_analytics.asset_total_count(asset)


app.add_route("/", GraphQLApp(schema=Schema(query=Query)))