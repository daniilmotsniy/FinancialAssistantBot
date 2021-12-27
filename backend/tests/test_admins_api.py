import json

from backend.tests.test_base_api import TestAPIBase


class TestAdminApi(TestAPIBase):
    """
    class for admins api test cases
    """
    test_admin = json.dumps({
            "admin_name": "TestAdmin",
            "admin_password": "123456abcd"
        })

    test_admin2 = json.dumps({
        "admin_name": "TestAdmin2",
        "admin_password": "ABCD123456"
    })

    def test_get_admins(self):
        """
        checks whether the get request to api works well
        """
        self.client.post('/api/v1/admins', headers={"Content-Type": "application/json"},
                         data=self.test_admin)
        self.client.post('/api/v1/admins', headers={"Content-Type": "application/json"},
                         data=self.test_admin2)
        request = self.client.get('/api/v1/admins')
        assert len(json.loads(request.data)) == 2
        self.assertEqual(200, request.status_code)

    def test_get_admin(self):
        """
        checks whether the get request to api works well
        """
        self.client.post('/api/v1/admins', headers={"Content-Type": "application/json"},
                         data=self.test_admin)
        request = self.client.get('/api/v1/admins/1')
        self.assertEqual(200, request.status_code)

    def test_post_admin(self):
        """
        checks whether the post request to api works well
        """
        request = self.client.post('/api/v1/admins', headers={"Content-Type": "application/json"},
                                   data=self.test_admin)
        self.assertEqual(201, request.status_code)

    def test_put_admin(self):
        """
        checks whether the put request to api works well
        """
        self.client.post('/api/v1/admins', headers={"Content-Type": "application/json"},
                         data=self.test_admin)
        data_to_update = json.dumps({
            "admin_name": "TestAdminUpdated",
            "admin_password": "123456abcde"
        })
        request = self.client.put('/api/v1/admins/1',
                                  headers={"Content-Type": "application/json"},
                                  data=data_to_update)
        new_admin = self.client.get('/api/v1/admins/1')
        assert json.loads(new_admin.data)['admin_password'] == '926e27b76d9e5b7808b45dbaf6d74aa839a0a1265d014b929bf1292f1c645ee1'
        self.assertEqual(204, request.status_code)

    def test_delete_admin(self):
        """
        checks whether the delete request to api works well
        """
        self.client.post('/api/v1/admins', headers={"Content-Type": "application/json"},
                         data=self.test_admin)
        request = self.client.delete('/api/v1/admins/1')
        self.assertEqual(200, request.status_code)