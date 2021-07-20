from unittest import TestCase


from api.api import create_api


class DefaultRouteCase(TestCase):

    def setUp(self) -> None:
        self. api = create_api("testing")
        self.api_context = self.api.app_context()
        self.api_context.push()
        self.client  = self.api.test_client()
        self.dr_response = self.client.get('/')
    
    def tearDown(self) -> None:
        self.api_context.pop()

    
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
