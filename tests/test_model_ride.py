from tests.apibasetestcase import ApiBaseTestCase

from tests.utils.data_model_ride import owner, ride_data
from tests.utils.data_model_ride import create_test_ride


class RideModelCase(ApiBaseTestCase):

    def test_ride_creation(self):
        """Assert creation of a ride
        """
        ride = create_test_ride(1)
        self.assertEqual(ride.vehicle_plate, ride_data['vehicle_plate'])
        self.assertEqual(ride.seats, ride_data['seats'])
        self.assertEqual(ride.town_from, ride_data['town_from'])
        self.assertEqual(ride.town_to, ride_data['town_to'])
        self.assertEqual(ride.created_by, 1)

    def test_saving_to_db(self):
        """Assert that a ride can be 
        saved to db
        """
        owner.save()
        ride = create_test_ride(owner.id)

        self.assertEqual(ride.id, None)
        self.assertEqual(ride.created_at, None)
        
        ride.save()
        self.assertEqual(ride.id, 1)
        self.assertNotEqual(ride.created_at, None)

    def test_string_representation(self):
        """Assert the string representation 
        of a ride
        """
        ride = create_test_ride(1)
        r1_rep = ride.__repr__()
        r_time = ride.depart_time
        r_from = ride.town_from
        r_to = ride.town_to
        def_rep = f'Ride at {r_time}: {r_from} - {r_to}'
        self.assertEqual(r1_rep, def_rep)
