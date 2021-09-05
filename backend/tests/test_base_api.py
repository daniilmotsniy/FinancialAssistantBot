import unittest

from backend.entry_point import app
from backend.config import TestConfiguration
from backend.db import db


class TestAPIBase(unittest.TestCase):
    def setUp(self):
        self.test_app = app
        self.test_app.config.from_object(TestConfiguration)
        self.db = db
        self.db.create_all()
        self.client = self.test_app.test_client()

    def tearDown(self):
        self.db.drop_all()
