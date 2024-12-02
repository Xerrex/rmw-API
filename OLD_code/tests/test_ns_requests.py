from http import HTTPStatus
from json import dumps

from werkzeug.datastructures import Headers

from tests.apibasetestcase import ApiBaseTestCase
from tests.utils.data_ns_Rrequests import owner_data, pass_data, pass2_data, \
                ride_data, pass_req_data, pass2_req_data, pass_req_update


class RequestsNSTestCase(ApiBaseTestCase):
    """Ride Requests NameSpace Tests

    Endpoints:
    GET, POST           /api/requests/<int:rideID>/all
    DELETE, PATCH, PUT  /api/requests/<int:rideID>/all/<int:reqID>
    """
    
    def register_user(self, user_data):
        """Sign up a user
        """
        self.client.post(self.signup_url, content_type='application/json',
                                        data=dumps(user_data))

    def login_user(self, user_data):
        """login a User
        """
        credentials = {
            'username': user_data['username'],
            'password': user_data['password']
        }

        response = self.client.post(self.login_url, content_type='application/json', 
                                    data=dumps(credentials))
        response_data = response .get_json()
        return response_data['access_token']

    def create_ride(self, header, ride_data):
        """Create ride
        """
        response = self.client.post(self.rides_url, headers=header, 
                        data=dumps(ride_data))
        return response
    
    def make_request(self, rideID, header, req_data):
        """Create request to join a ride
        """
        reqs_url = f'/api/requests/{rideID}/all'
        response = self.client.post(reqs_url, headers=header, 
                        data=dumps(req_data))
        return response

    def setUp(self):
        super().setUp()
        self.signup_url = '/api/auth/signup'
        self.login_url = '/api/auth/login'
        self.rides_url = '/api/rides/'
        
        self.register_user(owner_data)
        token = self.login_user(owner_data)
        self.owner_header = {
            'Authorization': token,
            "Accept": 'application/json',
            "Content-Type": 'application/json',  
        }

        self.register_user(pass_data)
        token = self.login_user(pass_data)
        self.pass_header = {
            'Authorization': token,
            "Accept": 'application/json',
            "Content-Type": 'application/json',  
        }

    def tearDown(self):
        super().tearDown()
        self.owner_header = None
        self.pass_header = None

    def test_viewing_requests(self):
        """Test that the ride owner can view 
        requests on a ride
        """
        self.create_ride(self.owner_header, ride_data)

        self.register_user(pass2_data)

        pass2_header = {
            'Authorization': self.login_user(pass2_data),
            "Accept": 'application/json',
            "Content-Type": 'application/json',  
        }

        self.make_request(1, self.pass_header, pass_req_data)
        self.make_request(1, pass2_header, pass2_req_data)
        response = self.client.get('/api/requests/1/all', headers=self.owner_header)
        
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(2, len(response.get_json()))

    def test_only_owner_can_view_requests(self):
        """Test that only the owner of the ride can 
        view a ride's requests
        """
        self.create_ride(self.owner_header, ride_data)
        self.make_request(1, self.pass_header, pass_req_data)
        response = self.client.get('/api/requests/1/all', headers=self.pass_header)

        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
        self.assertIn('Your are not authorized to view requests', response.get_json()['message'])

    def test_passenger_can_make_request(self):
        """Test that a passenger can make 
        request to join a ride
        """
        self.create_ride(self.owner_header, ride_data)
        response = self.make_request(1, self.pass_header, pass_req_data)

        self.assertEqual(HTTPStatus.CREATED, response.status_code)

    def test_passenger_cannot_request_twice(self):
        """Test that a passenger cannot make 
        two requests to join the same ride
        """
        self.create_ride(self.owner_header, ride_data)
        self.make_request(1, self.pass_header, pass_req_data)
        response = self.make_request(1, self.pass_header, pass_req_data)

        self.assertEqual(HTTPStatus.CONFLICT, response.status_code)

    def test_owner_cannot_make_request(self):
        """Test that a ride owner cannot 
        make a request to join their own ride.
        """
        self.create_ride(self.owner_header, ride_data)
        response = self.make_request(1, self.owner_header, pass_req_data)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_passenger_can_retract_request(self):
        """ Test that a user can remove 
        their request to join ride
        """
        self.create_ride(self.owner_header, ride_data)
        first_response = self.make_request(1, self.pass_header, pass_req_data)
        self.assertEqual(HTTPStatus.CREATED, first_response.status_code)

        second_response = self.client.delete('/api/requests/1/all/1', 
                            headers=self.pass_header)
        self.assertEqual(HTTPStatus.NO_CONTENT, second_response.status_code)

    def test_request_removed_by_owner(self):
        """Test that a request can only be removed 
        by the person who made the request
        """
        self.create_ride(self.owner_header, ride_data)
        self.make_request(1, self.pass_header, pass_req_data)

        second_response = self.client.delete('/api/requests/1/all/1', 
                            headers=self.owner_header)
        self.assertEqual(HTTPStatus.UNAUTHORIZED, second_response.status_code)
    
    def test_passenger_can_update_request(self):
        """Test that a passenger can update 
        their request details
        """
        self.create_ride(self.owner_header, ride_data)
        first_response = self.make_request(1, self.pass_header, pass_req_data)
        self.assertEqual(HTTPStatus.CREATED, first_response.status_code)

        second_response = self.client.put('/api/requests/1/all/1', 
                            headers=self.pass_header, data=dumps(pass_req_update))
        self.assertEqual(HTTPStatus.OK, second_response.status_code)

    def test_request_update_by_owner(self):
        """Test that only a request's owner 
        can update
        """
        self.create_ride(self.owner_header, ride_data)
        first_response = self.make_request(1, self.pass_header, pass_req_data)
        self.assertEqual(HTTPStatus.CREATED, first_response.status_code)

        second_response = self.client.put('/api/requests/1/all/1', 
                            headers=self.owner_header, data=dumps(pass_req_update))
        self.assertEqual(HTTPStatus.UNAUTHORIZED, second_response.status_code)

    def test_cannot_update_accepted_request(self):
        """Test that a passenger cannot 
        change details of an accepted request
        """
        self.create_ride(self.owner_header, ride_data)
        self.make_request(1, self.pass_header, pass_req_data)
        action_response = self.client.patch('/api/requests/1/all/1', 
                    headers=self.owner_header, data=dumps({'action':"accepted"}))
        self.assertEqual(HTTPStatus.OK, action_response.status_code)

        update_response = self.client.put('/api/requests/1/all/1', 
                            headers=self.pass_header, data=dumps(pass_req_update))
        self.assertEqual(HTTPStatus.FORBIDDEN, update_response.status_code)

    def test_accepting_a_passenger_request(self):
        """Test that a ride owner can accept 
        a request to join the ride
        """
        self.create_ride(self.owner_header, ride_data)
        self.make_request(1, self.pass_header, pass_req_data)
        action_response = self.client.patch('/api/requests/1/all/1', 
                    headers=self.owner_header, data=dumps({'action':"accepted"}))
        self.assertEqual(HTTPStatus.OK, action_response.status_code)

        get_response = self.client.get('/api/requests/1/all', headers=self.owner_header)
        request_status =get_response.get_json()[0]['status']

        self.assertEqual(HTTPStatus.OK, get_response.status_code)
        self.assertEqual(request_status, 'Accepted')

    def test_rejecting_a_passenger_request(self):
        """Test that a ride owner can accept
        a request to join the ride
        """
        self.create_ride(self.owner_header, ride_data)
        self.make_request(1, self.pass_header, pass_req_data)
        action_response = self.client.patch('/api/requests/1/all/1', 
                    headers=self.owner_header, data=dumps({'action':"rejected"}))
        self.assertEqual(HTTPStatus.OK, action_response.status_code)

        get_response = self.client.get('/api/requests/1/all', headers=self.owner_header)
        request_status =get_response.get_json()[0]['status']

        self.assertEqual(HTTPStatus.OK, get_response.status_code)
        self.assertEqual(request_status, 'Rejected')

    def test_request_status_change_by_ride_owner(self):
        """Test that only the ride owner 
        can change the status of a request
        """
        self.create_ride(self.owner_header, ride_data)
        self.make_request(1, self.pass_header, pass_req_data)
        action_response = self.client.patch('/api/requests/1/all/1', 
                    headers=self.pass_header, data=dumps({'action':"rejected"}))
        self.assertEqual(HTTPStatus.UNAUTHORIZED, action_response.status_code)
