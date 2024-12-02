from flask_restx import Model, fields
from flask_restx.reqparse import RequestParser

ride_model = Model(
    'Ride',{
        'id': fields.Integer(),
        'vehicle_plate': fields.String(),
        'seats': fields.Integer(),
        'town_from': fields.String(),
        'town_to': fields.String(),
        'depart_time': fields.DateTime(),
        'end_time': fields.DateTime(),
        'created_at': fields.DateTime()
    }
)

vplate_help = 'vehicle plate cannot be blank'
seat_help = 'Seats cannot be blank'
t_from_help = 'Town from cannot be blank'
t_to_help = 'Town to cannot be blank'
dtime_help = 'Depart time cannot be blank'
etime_help = 'End time cannot be blank'

ride_parser = RequestParser()
ride_parser.add_argument('vehicle_plate', required=True, location='json', help=vplate_help, nullable=False)
ride_parser.add_argument('seats', type=int, required=True, location='json', help=seat_help, nullable=False)
ride_parser.add_argument('town_from', required=True, location='json', help=t_from_help, nullable=False)
ride_parser.add_argument('town_to', required=True, location='json', help=t_to_help, nullable=False)
ride_parser.add_argument('depart_time', required=True, location='json', help=dtime_help, nullable=False)
ride_parser.add_argument('end_time', required=True, location='json', help=etime_help, nullable=False)

