from graphene import ObjectType, Int, String


class AssetsCount(ObjectType):
    user_stocks = Int()
    user_currencies = Int()
    user_cryptos = Int()
    user_resources = Int()


class LabelCount(ObjectType):
    label = String()
    count = Int()
