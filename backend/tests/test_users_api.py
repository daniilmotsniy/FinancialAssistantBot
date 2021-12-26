import json

from backend.tests.test_base_api import TestAPIBase


class TestUserApi(TestAPIBase):
    """
    class for users api test cases
    """
    test_user = json.dumps({
        "user_id": "ef797c8118f02dfb649607dd5d3f8c76"
                   "23048c9c063d532cc95c5ed7a898a64f",
        "user_name": "Test",
        "user_assets": {
            "user_currency": ["USD", "EUR"],
            "user_crypto": ["BTC", "ETH", "XRP"],
            "user_resources": ["Oil"],
            "user_stocks": ["AAPL"],
        }
    })

    test_user2 = json.dumps({
        "user_id": "af797c8118f02dfb649607dd5d3f8c762"
                   "3048c9c063d532cc95c5ed7a8982463g",
        "user_name": "Test2",
        "user_assets": {
            "user_currency": ["EUR"],
            "user_crypto": ["BTC", "ETH"],
            "user_resources": ["Oil"],
            "user_stocks": ["BMW"],
        }
    })

    def test_get_users(self):
        """
        checks whether the get request to api works well
        """
        self.client.post('/api/v1/users',
                         headers={"Content-Type": "application/json"},
                         data=self.test_user)
        self.client.post('/api/v1/users',
                         headers={"Content-Type": "application/json"},
                         data=self.test_user2)
        request = self.client.get('/api/v1/users')
        self.assertEqual(2, len(json.loads(request.data)))
        self.assertEqual(200, request.status_code)

    def test_get_user(self):
        """
        checks whether the get request to api works well
        """
        self.client.post('/api/v1/users',
                         headers={"Content-Type": "application/json"},
                         data=self.test_user)
        request = self.client.get('/api/v1/users/ef797c8118f02dfb649607dd5'
                                  'd3f8c7623048c9c063d532cc95c5ed7a898a64f')
        self.assertEqual(200, request.status_code)

    def test_post_user(self):
        """
        checks whether the post request to api works well
        """
        request = self.client.post('/api/v1/users',
                                   headers={"Content-Type": "application/json"},
                                   data=self.test_user)
        self.assertEqual(201, request.status_code)

    def test_put_user(self):
        """
        checks whether the put request to api works well
        """
        self.client.post('/api/v1/users',
                         headers={"Content-Type": "application/json"},
                         data=self.test_user)
        data_to_update = json.dumps({
            "user_assets": {
                "user_stocks": ["AAPL", "MCFE"],
                "user_currency": ["USD", "EUR"],
                "user_crypto": ["BTC", "ETH", "XRP"],
                "user_resources": ["Oil"],
            }
        })
        request = self.client.put('/api/v1/users/ef797c8118f02dfb649607dd5'
                                  'd3f8c7623048c9c063d532cc95c5ed7a898a64f',
                                  headers={"Content-Type": "application/json"},
                                  data=data_to_update)
        new_user = self.client.get('/api/v1/users/ef797c8118f02dfb649607dd5'
                                   'd3f8c7623048c9c063d532cc95c5ed7a898a64f')
        self.assertEqual("MCFE", json.loads(new_user.data)['user_assets']['user_stocks'][1])
        self.assertEqual(204, request.status_code)

    def test_delete_user(self):
        """
        checks whether the delete request to api works well
        """
        self.client.post('/api/v1/users', headers={"Content-Type": "application/json"},
                         data=self.test_user)
        request = self.client.delete('/api/v1/users/ef797c8118f02dfb649607dd5'
                                     'd3f8c7623048c9c063d532cc95c5ed7a898a64f')
        self.assertEqual(200, request.status_code)