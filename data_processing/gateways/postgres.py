from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_STR = "postgresql+psycopg2://postgres:root@localhost:5432/financial_assistant"


class Postgres:
    def __init__(self):
        self.session = sessionmaker(create_engine(DATABASE_STR))
