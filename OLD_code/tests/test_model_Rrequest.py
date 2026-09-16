from app.data.models import Ride
from tests.apibasetestcase import ApiBaseTestCase

from tests.utils.data_model_Rrequests import ride_owner, passenger
from tests.utils.data_model_Rrequests import passenger_req_data
from tests.utils.data_model_Rrequests import create_test_ride, create_request

class RideRequestModelCase(ApiBaseTestCase):


    def test_request_creation(self):
        """test creation
        """
        ride_request = create_request(1, 1, passenger_req_data) # dummy data
        self.assertEqual(ride_request.ride_id, 1)
        self.assertEqual(ride_request.user_id, 1)
        self.assertEqual(ride_request.stop, passenger_req_data['stop'])
        self.assertEqual(ride_request.seats, passenger_req_data['seats'])

    def test_saving_to_db(self):
        """test saving to db
        """
        ride_owner.save() # ride owner
        passenger.save() # ride passenger
        ride = create_test_ride(ride_owner.id) # Create ride
        ride.save()
        
        ride_request = create_request(ride.id, passenger.id, passenger_req_data)
        self.assertEqual(ride_request.id, None)
    
        ride_request.save()
        self.assertEqual(ride_request.id, 1)



    def test_string_representation(self):
        """test string representation
        """
        
        ride_request = create_request(1, 1, passenger_req_data)

        made_at = ride_request.made_at
        stop = ride_request.stop

        def_rep = f'RideRequest-{made_at}-{stop}'

        self.assertEqual(def_rep, ride_request.__repr__())


