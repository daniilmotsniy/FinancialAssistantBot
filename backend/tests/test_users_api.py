import json

from test_base_api import TestUsersBase


class TestUserApi(TestUsersBase):
    """
    class for users api test cases
    """
    test_user = json.dumps(
        {
            "user_id": "12345678",
            "user_name": "Test",
            "user_assets": {
                "user_stocks": ["AAPL"],
                "user_currencies": ["USD", "EUR"],
                "user_cryptos": ["BTC", "ETH", "XRP"],
                "user_resources": ["Oil"],
            }
        })

    def test_get_users(self):
        """
        checks whether the get request to api works well
        """
        request = self.client.get('/api/v1/users')
        self.assertEqual(200, request.status_code)

    def test_get_user(self):
        """
        checks whether the get request to api works well
        """
        self.client.post('/api/v1/users', headers={"Content-Type": "application/json"}, data=self.test_user)
        request = self.client.get('/api/v1/users/ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f')
        self.assertEqual(200, request.status_code)

    def test_post_user(self):
        """
        checks whether the post request to api works well
        """
        request = self.client.post('/api/v1/users', headers={"Content-Type": "application/json"}, data=self.test_user)
        self.assertEqual(201, request.status_code)

    def test_put_user(self):
        """
        checks whether the put request to api works well
        """
        self.client.post('/api/v1/users', headers={"Content-Type": "application/json"}, data=self.test_user)
        data_to_update = json.dumps(
            {
                "user_assets": {
                    "user_stocks": ["AAPL"],
                    "user_currencies": ["USD", "EUR"],
                    "user_cryptos": ["BTC", "ETH", "XRP"],
                    "user_resources": ["Oil"],
                }
            })
        request = self.client.put('/api/v1/users/ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f',
                                  headers={"Content-Type": "application/json"}, data=data_to_update)
        self.assertEqual(204, request.status_code)

    def test_delete_user(self):
        """
        checks whether the delete request to api works well
        """
        self.client.post('/api/v1/users', headers={"Content-Type": "application/json"}, data=self.test_user)
        request = self.client.delete('/api/v1/users/ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f')
        self.assertEqual(200, request.status_code)