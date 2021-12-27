import requests

PUBLIC_KEY = requests.get('https://dev-ecasl1ud.us.auth0.com/.well-known/jwks.json').json()['keys'][0]['x5c'][0]


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:root@localhost:5432/financial_assistant'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CERTIFICATE = "-----BEGIN CERTIFICATE-----\n" + PUBLIC_KEY + "\n-----END CERTIFICATE-----"


class TestConfiguration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
