from fastapi import FastAPI
from graphene import ObjectType, Schema, String, Field
from starlette.graphql import GraphQLApp

from entities.assets_analytics import AssetsAnalytics
from helpers.constants import DB_BACKUP_CSV_PATH
from web.graphql import AssetsCount

app = FastAPI()

assets_analytics = AssetsAnalytics(DB_BACKUP_CSV_PATH)


class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))
    assets_count = Field(AssetsCount)

    def resolve_assets_count(self, info):
        total_count = assets_analytics.assets_total_count()
        return total_count

    def resolve_hello(self, info, name):
        return "Hello " + name


app.add_route("/", GraphQLApp(schema=Schema(query=Query)))
