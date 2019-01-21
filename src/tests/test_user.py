import unittest
import os, sys
import json
from ..app import create_app, db

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/')

class UserTest(unittest.TestCase):
    # User Test Case

    def setUp(self):
        self.app = self.app("testing")
        self.client = self.app.test_client
        self.user = {
            'name': 'Fredy',
            'email': 'mercury.freddy@mail.com',
            'password': 'somePassword'
        }

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_creation(self):
        # test user creation with valid credentials
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 201)

    def test_user_creation_with_existing_email(self):
        # test user creation with already existing email
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('error'))

    def test_user_creation_with_no_password(self):
        user1 = {
            'name': 'Greg',
            'email': 'greg_plitt@rip.com'
        }

        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)        
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('email'))

    def test_user_creation_with_empty_request(self):
        user1 = {}
        res = self.client().post('/api/v1/users/', headers={'Content-type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_user_login(self):
        res = self.client().post('/api/v1/users/', headers={'Content-type': 'application/json'}, data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/users/login', headers={'Content-type': 'application/json'}, data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 200)

    def test_user_login_with_invalid_password(self):
        user1 = {
            'password': 'zzzzzz',
            'email': 'mercury.freddy@mail.com'
        }
        res = self.client().post('/api/v1/users/', headers={'Content-type': 'application/json'}, data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/users/', headers={'Content-type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'invalid credentials')
        self.assertEqual(res.status_code, 400)
        

    def test_user_login_with_invalid_email(self):
        user1 = {
            'password': 'passw0rd',
            'email': 'www@www.com'
        }
        res = self.client().post('/api/v1/user', headers={'Content-type': 'application/json'}, data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/user', headers={'Content-type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'invalid credentials')
        self.assertEqual(res.status_code, 400)

    def test_user_get_me(self):
         res = self.client().post('/api/v1/users', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
         self.assertEqual(res.status_code, 201)
         api_token = json.loads(res.data).get('jwt_token')
         res = self.client().get('/api/v1/users/me', headers={'Content-Type': 'application/json'})
         json_data = json.loads(res.data)
         self.assertEqual(res.status_code, 200)
         self.assertEqual(json_data.get('email'), 'mercury.freddy@mail.com')
         self.assertEqual(json_data.get('name'), 'Freddy')

    def test_user_update_me(self):
        user1 = {
            'name': 'new name'
        }
        res = self.client.post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().put('/api/v1/users/me', headers={'Content-Type': 'application/json', 'api_token': api_token}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('name'), 'new name')

    def test_delete_user(self):
        res = self.client().post('api/v1/users', headers={'Content-type': 'application/json'}, data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().delete('/api/v1/users/me', headers={'Content-type': 'application/json'})
        self.assertEqual(res.status_code, 204)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    if __name__ == "__main__":
        unittest.main()














