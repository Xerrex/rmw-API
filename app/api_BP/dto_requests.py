from flask_restx import Model, fields
from flask_restx.reqparse import RequestParser


request_model = Model(
    'RideRequest', {
        'seats': fields.Integer,
        'stop': fields.String,
        'status': fields.String,
        'made_at': fields.DateTime
    }
)

r_request_parser = RequestParser()
r_request_parser.add_argument('stop', location='json', nullable=True) # Passenger stop can be blank
r_request_parser.add_argument('seats', type=int, location='json', nullable=True) # Passenger seat can be blank


req_update_parser = r_request_parser.copy()
req_update_parser.replace_argument('stop', location='json', required=True, help='Your Stop Cannot be blank', nullable=False)
req_update_parser.replace_argument('seats', type=int, location='json', required=True, help='Your Seats cannot be blank', nullable=False)


req_action_parser = RequestParser()
req_action_parser.add_argument('action', choices=('accepted', 'rejected'), location='json', required=True, nullable=False, help="Request Action cannot be blank")