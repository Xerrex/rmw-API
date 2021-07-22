from unittest import main

from .apibasetestcase import ApiBaseTestCase


class DefaultRouteCase(ApiBaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.dr_response = self.client.get('/')
    

    
    def test_default_route_status_code(self):
        """Assert that request to '/'
        
        returns the API landing Page html content
        """
        self.assertEqual(self.dr_response.status_code, 200)
    
    def test_default_route_content(self):
        """Assert that a request to '/'

        the API_TITLE is in the response contents
        """
        title = bytes(self.api.config['API_TITLE'], 'utf-8')
        self.assertIn(title, self.dr_response.data)

if __name__ = '__main__':
    main(verbosity=2)