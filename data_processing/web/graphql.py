from graphene import ObjectType, Int


class AssetsCount(ObjectType):
    user_stocks = Int()
    user_currencies = Int()
    user_cryptos = Int()
    user_resources = Int()