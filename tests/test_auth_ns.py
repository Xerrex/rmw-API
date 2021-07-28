import json
import unittest

from werkzeug.wrappers.response import Response

from .apibasetestcase import ApiBaseTestCase

from app.data.user_controller import create_user, \
        get_user_by_id


class TestAuthNameSpaceCase(ApiBaseTestCase):
    """Test for the Authenication Namespace
    """

    def register_user(self):
        response = self.client.post(self.signup_url, data=json.dumps(self.test_user), 
                        content_type='application/json')
        return response
    
    def login_user(self, credentials=None):
        if credentials is None:
            credentials = {
                'username': self.test_user['username'],
                'password': self.test_user['password']
            }
        response = self.client.post(self.login_url, data=json.dumps(credentials), 
                        content_type='application/json')
        return response

    def setUp(self) -> None:
        super().setUp()
        self.test_user = {
            'name': 'test user', 
            'username': 'testuser', 
            'email': 'testuser@testing.com', 
            'password': 'testuserpassword'
        }

        self.signup_url = '/api/auth/signup'
        self.login_url = '/api/auth/login'
        self.logout_url = '/api/auth/logout'

    def test_user_signup(self):
        """Assert that a user can register
        """
        res = self.register_user()
        res_data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.test_user['name'], res_data)

    def test_user_double_registration(self):
        """Assert that a User cannot register twice
        """
        res = self.register_user()
        res = self.register_user()
        self.assertEqual(res.status_code, 409)

    def test_user_login(self):
        """Assert that a User can login
        """
        res = self.register_user()
        res = self.login_user()

        res_data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertIn('Bearer', res_data['access_token'])
        self.assertIn(self.test_user['name'], res_data['msg'])
    
    def test_user_login_with_wrong_credentials(self):
        """Assert that login with a wrong credentials fails
        """
        credentials = {
            'username': 'test1',
            'password': 'testuserpassword'
        }
        res = self.login_user(credentials)
        res_data = json.loads(res.get_data(as_text=True))
        msg =  'Your Username or Password is wrong'
        
        self.assertEqual(res.status_code, 401)
        self.assertIn(msg, res_data['msg'])


    def test_user_double_login(self):
        """Assert that a User cannot Login twice
        """
        # TODO: Test Multiple login
        pass
    
    def test_user_logout(self):
        """Assert that a User can logout
        """
        res = self.register_user()
        res = self.login_user()
        res_data = json.loads(res.get_data(as_text=True))

        headers = {
            'Authorization': res_data['access_token'],
            "Accept": 'application/json',
            "Content-Type": 'application/json',  
        }
        
        res = self.client.delete(self.logout_url, headers=headers)

        self.assertEqual(res.status_code, 200)


    def test_logout_for_user_not_logged_in(self):
        """Assert that Logout is allowed only 
        for logged in users only
        """
        res = self.register_user()
        res = self.client.delete(self.logout_url, content_type='application/json')

        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main(verbosity=2)