from datetime import datetime, timedelta
from tests.utils.helpers import DT_FORMAT


owner_data = {
    'name': 'Ride Owner', 
    'username': 'rideowner', 
    'email': 'rideowner@testing.com', 
    'password': 'rideownerpass'
}

pass_data = {
    'name': 'Ride Passenger', 
    'username': 'ridepassenger', 
    'email': 'ridepassenger@testing.com', 
    'password': 'ridepassengerpass'
}

pass2_data = {
    'name': 'Ride2 Passenger2', 
    'username': 'ride22passenger', 
    'email': 'ride22passenger@testing.com', 
    'password': 'ride22passenger22pass'
}


depart_time = (datetime.utcnow() + timedelta(days=1)).strftime(DT_FORMAT)
end_time = (datetime.utcnow() + timedelta(days=2)).strftime(DT_FORMAT)

ride_data = {
    'vehicle_plate': 'KCH DFGD',
    'seats': 3,
    'town_from': 'Nairobi',
    'town_to': 'Mau Summit',
    'depart_time': f'{depart_time}',
    'end_time': f'{end_time}'
}

pass_req_data = {'stop':"The Stretch", 'seats':2}
pass2_req_data = {'stop':"Molo Junc", 'seats':1}

pass_req_update = {'stop':"Stage_Viazi", 'seats':2}