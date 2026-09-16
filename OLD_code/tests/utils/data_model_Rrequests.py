from datetime import datetime, timedelta
from tests.utils.helpers import create_ride, create_user
from tests.utils.helpers import create_ride_request
from tests.utils.helpers import DT_FORMAT


depart_time = datetime.utcnow() + timedelta(days=1)
end_time = datetime.utcnow() + timedelta(days=2)

ride_data = {
    'vehicle_plate': 'KCH 003RR',
    'seats': 3,
    'town_from': 'Nairobi',
    'town_to': 'Londian',
    'depart_time': f'{depart_time.strftime(DT_FORMAT)}',
    'end_time': f'{end_time.strftime(DT_FORMAT)}'
}

ride_owner = create_user('ride owner', 'owner', 'owner@api.com', 'rideownerpass')
passenger = create_user('ride pass1', 'pass1', 'pass1@api.com', 'pass1pass')

passenger_req_data = {'stop':"Nakuru", 'seats':1}


def create_test_ride(owner):
    return create_ride(owner, ride_data)


def create_request(ride, passenger, request_data):
    stop = request_data['stop']
    seats = request_data['seats']
    return create_ride_request(ride, passenger, stop, seats)

