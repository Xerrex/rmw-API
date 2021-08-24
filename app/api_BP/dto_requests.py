from flask_restx import Model, fields
from flask_restx.reqparse import RequestParser


request_model = Model(
    'RideRequest', {
        'id': fields.Integer,
        'seats': fields.Integer,
        'stop': fields.String,
        'status': fields.String,
        'made_at': fields.DateTime
    }
)

r_request_parser = RequestParser()
r_request_parser.add_argument('stop', location='json', nullable=True) # Passenger stop can be blank
r_request_parser.add_argument('seat', type=int, location='json', nullable=True) # Passenger seat can be blank