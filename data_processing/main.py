from typing import Optional

from fastapi import FastAPI
from graphene import ObjectType, Schema, Int, String, Field
from starlette.graphql import GraphQLApp

from csv_handler import assets_total_count

app = FastAPI()

FILE_PATH = 'test_users.csv'

class AssetsCount(ObjectType):
    user_stocks = Int()
    user_currencies = Int()
    user_cryptos = Int()
    user_resources = Int()


class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))
    assets_count = Field(AssetsCount)

    def resolve_assets_count(self, info):
        total_count = assets_total_count(FILE_PATH)
        return total_count

    def resolve_hello(self, info, name):
        return "Hello " + name


app.add_route("/", GraphQLApp(schema=Schema(query=Query)))


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
