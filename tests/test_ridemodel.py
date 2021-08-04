from datetime import datetime, timedelta

from tests.apibasetestcase import ApiBaseTestCase

from tests.data_ride import create_user, create_ride


class RideModelCase(ApiBaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.owner = create_user("Bob Developer", "bobdev", "bobdev@api.com", 'qwerty12345')
        self.owner.save()
        self.ride = create_ride(self.owner.id)


    def test_ride_creation(self):
        """Assert creation of a ride
        """
        self.assertEqual(self.ride.created_by, self.owner.id)
        self.assertEqual(self.ride.vehicle_plate, 'KCH 003')

    def test_saving_to_db(self):
        """Assert that a ride can be 
        saved to db
        """
        self.ride.save()
        self.assertEqual(self.ride.id, 1)

    def test_String_representation(self):
        """Assert the string representation 
        of a ride
        """
        r1_rep = self.ride.__repr__()
        r_time = self.ride.depart_time
        r_from = self.ride.town_from
        r_to = self.ride.town_to
        def_rep = f'Ride at {r_time}: {r_from} - {r_to}'
        self.assertEqual(r1_rep, def_rep)
