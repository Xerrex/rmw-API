from unittest import main

from flask_jwt_extended import decode_token

from tests.apibasetestcase import ApiBaseTestCase
from tests.utils.helpers import create_user


class TestUserModelCase(ApiBaseTestCase):
    
    def setUp(self) -> None:
        super().setUp()
        self.u1 = create_user("Bob Developer", "bobdev", "bobdev@api.com", 'qwerty12345')


    def test_user_creation(self):
        """Assert that User data 
        is correct on creation
        """
        self.assertEqual(self.u1.name, 'Bob Developer')
        self.assertNotEqual(self.u1.password, 'qwerty12345')

    def test_saving_to_db(self):
        """Assert that a User is saved to the db
        """
        self.assertEqual(self.u1.id, None)
        self.u1.save()
        self.assertEqual(self.u1.id, 1)
    
    def test_string_representation(self):
        """Assert that the string 
        representation of a user is as defined
        """
        user_rep = self.u1.__repr__()
        def_rep = f'User-{self.u1.username}'
        self.assertTrue(user_rep == def_rep)

    def test_password_hashing(self):
        """Assert that a created token 
        contains identity of a user
        """
        self.assertTrue(self.u1.verify_password('qwerty12345'))
    
    def test_access_token_gen(self):
        """Assert a User can Create an 
        access token
        """
        access_token = self.u1.generate_access_token()
        username = decode_token(access_token)['sub']
        self.assertEqual(self.u1.username, username)



if __name__ == '__main__':
    main(verbosity=2)