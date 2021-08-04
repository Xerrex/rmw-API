from copy import deepcopy
from datetime import datetime, timedelta
from app.data.models import User, Ride

DT_FORMAT = '%Y-%m-%d %H:%M:%S.%f' # 2021-08-04 05:35:08.817837
depart_time = datetime.utcnow() + timedelta(days=1)
end_time = datetime.utcnow() + timedelta(days=2)

ride_data = {
    'vehicle_plate': 'KCH 003',
    'seats': 3,
    'town_from': 'Nairobi',
    'town_to': 'Machakos',
    'depart_time': f'{depart_time.strftime(DT_FORMAT)}',
    'end_time': f'{end_time.strftime(DT_FORMAT)}'
}


ride_update = deepcopy(ride_data)
update_dtime = datetime.utcnow() + timedelta(hours=1)
update_etime = update_dtime + timedelta(days=1)
ride_update['vehicle_plate'] = 'KHH 300'
ride_update['depart_time'] = f'{update_dtime.strftime(DT_FORMAT)}'
ride_update['end_time'] = f'{update_etime.strftime(DT_FORMAT)}'

def create_user(name, username, email,password):
    """Create a user
    """
    return User(name, username, email, password)


def create_ride(owner):
    """Create a ride
    """
    return Ride(owner, **ride_data)

