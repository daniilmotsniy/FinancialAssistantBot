class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:root@localhost:5432/financial_assistant'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfiguration(object):
    """ configuration for tests """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False