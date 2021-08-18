from graphene import ObjectType, Int, String, Field


class AssetsCount(ObjectType):
    user_stocks = Int()
    user_currencies = Int()
    user_cryptos = Int()
    user_resources = Int()


class KeyValue(ObjectType):
    label = String()
    value = Int()


class Asset(ObjectType):
    item = Field(KeyValue)
