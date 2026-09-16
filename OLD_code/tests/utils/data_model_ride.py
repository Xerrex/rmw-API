from copy import deepcopy
from datetime import datetime, timedelta

from tests.utils.helpers import DT_FORMAT, create_user, create_ride


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


owner = create_user("Bob Developer", "bobdev", "bobdev@api.com", 'qwerty12345')


def create_test_ride(owner):
    return create_ride(owner, ride_data)
