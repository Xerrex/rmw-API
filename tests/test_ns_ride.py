import json

from tests.apibasetestcase import ApiBaseTestCase

from tests.utils.data_ns_ride import ride_data, ride_update
from tests.utils.data_ns_ride import test_user, test_credentials



class RideNameSpaceCase(ApiBaseTestCase):
    """Ride Namespace tests
    """

    def login_user(self, credentials):
        """Login a User
        """
        res = self.client.post('/api/auth/login', content_type='application/json', 
                                    data=json.dumps(credentials))
        res_data = res.get_json()
        return res_data['access_token']
    
    def register_user(self, user_data):
        """Sign up a user
        """
        self.client.post('/api/auth/signup', content_type='application/json',
                                        data=json.dumps(user_data))
    
    def create_ride(self, ride_data):
        """Create a ride
        """
        response = self.client.post(self.rides_url, headers=self.headers, 
                        data=json.dumps(ride_data))
        return response


    def setUp(self):
        super().setUp()
        self.rides_url = '/api/rides/'

        self.register_user(test_user)
        token = self.login_user(test_credentials)

        self.headers = {
            'Authorization': token,
            "Accept": 'application/json',
            "Content-Type": 'application/json',  
        }

    def test_creating_a_ride(self):
        """Test creating a ride
        """
        res = self.create_ride(ride_data)
        res_json = res.get_json()
        self.assertEqual(res.status_code, 201)
        self.assertIn('Ride Offer was Created successfully', res_json['msg'])

    def test_get_all_rides(self):
        """Test fetching all rides
        """
        res = self.create_ride(ride_data)
        res = self.client.get(self.rides_url, content_type='application/json')

        res_json = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res_json)
        self.assertEqual(1, res_json[0]['id'])

    def test_get_a_ride(self):
        """Test fetching a single ride
        """
        self.create_ride(ride_data)
        res = self.client.get(f'{self.rides_url}1', content_type='application/json')
        res_json = res.get_json()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_json['id'], 1)
        self.assertEqual(res_json['vehicle_plate'], ride_data['vehicle_plate'])

    def test_updating_ride(self):
        """Test updating ride details
        """
        self.create_ride(ride_data)

        update_res = self.client.put(f'{self.rides_url}1', headers=self.headers, 
                        data=json.dumps(ride_update))
        get_res = self.client.get(f'{self.rides_url}1', content_type='application/json')
        get_res_json = get_res.get_json()

        self.assertEqual(update_res.status_code, 200)
        self.assertTrue(get_res_json['vehicle_plate'] == ride_update['vehicle_plate'])

