from datetime import datetime
from http import HTTPStatus
from flask import url_for
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user
from flask_restx import Namespace, Resource

from app.data.controller_ride import create_ride, get_all_rides
from app.data.controller_ride import check_active_ride
from app.data.controller_ride import get_ride_by_id
from app.data.controller_ride import update_ride
from .dto_ride import ride_model, ride_parser

ride_ns = Namespace('ride', description='Ride Operations')


@ride_ns.route('/')
@ride_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server error")
class RidesResource(Resource):
    """Fetch all available rides
    """
    
    @ride_ns.doc('get_rides')
    @ride_ns.response(int(HTTPStatus.OK), 'Success fetching all rides')
    @ride_ns.marshal_list_with(ride_model)
    def get(self):
        """Get all rides
        """
        rides = get_all_rides()
        return rides, HTTPStatus.OK

    @jwt_required()
    @ride_ns.doc('create_ride', security='Bearer')
    @ride_ns.expect(ride_parser)
    @ride_ns.response(int(HTTPStatus.CREATED), "Ride Created Successfully")
    @ride_ns.response(int(HTTPStatus.BAD_REQUEST), 'Ride Details validation Error')
    @ride_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Authorization token is Invalid or missing')
    @ride_ns.response(int(HTTPStatus.CONFLICT), "Ride not completed exists")
    def post(self):
        """Create a ride
        """
        # TODO POST: Create a ride offer
        ride_args = ride_parser.parse_args()
        depart_time = ride_args['depart_time']
        owner = current_user.id
        if check_active_ride(owner, depart_time):
            return {
                'msg': f'Your have an active ride that ends after {depart_time}',
                'action': f'Schedule your ride to depart after "{depart_time}"'
            }, HTTPStatus.CONFLICT # TODO: allow making multiple
        ride_id = create_ride(owner, ride_args)
        return {
            'msg': 'Ride Offer was Created successfully',
            'action': 'View the ride via the Link',
            'link': f'coming soon:{ride_id}'
        }, HTTPStatus.CREATED


@ride_ns.route('/<int:ride_id>')
@ride_ns.param('ride_id', "Identifier of a ride")
@ride_ns.response(int(HTTPStatus.NOT_FOUND), 'Ride was not found')
@ride_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal Server Error')
class RideResource(Resource):
    """Handle Operation on a ride
    """

    @ride_ns.doc('view_ride')
    @ride_ns.response(int(HTTPStatus.OK), 'Ride retrieved successfully')
    @ride_ns.marshal_with(ride_model)
    def get(self, ride_id):
        """View a ride
        """
        ride = get_ride_by_id(ride_id)
        if ride:
            return ride, HTTPStatus.OK
        return {
            'msg': f'Ride "{ride_id}" Not found',
            'action': 'View all rides',
            'link': url_for('api_bp.ride_rides_resource')
        }, HTTPStatus.NOT_FOUND


    @jwt_required()
    @ride_ns.doc('update_ride', security='Bearer')
    @ride_ns.expect(ride_parser)
    @ride_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Invalid or missing token or not ride owner')
    @ride_ns.response(int(HTTPStatus.OK), 'Ride was updated')
    def put(self, ride_id):
        """Update a ride
        """
        ride = get_ride_by_id(ride_id)

        if ride:
            if ride.created_by == current_user.id:
                update_ride_args = ride_parser.parse_args()
                # TODO: consider not editing finished rides
                update_ride(ride_id, **update_ride_args)
                return {
                    'msg': f'Ride "{ride_id}" has been updated',
                    'action': 'View the ride',
                    'link': url_for('api_bp.ride_ride_resource', ride_id=ride_id)
                }, HTTPStatus.OK
            return {
                'msg': f'Your are authorized to update the ride "{ride_id}"',
                'action': 'View the ride',
                'link': url_for('api_bp.ride_ride_resource', ride_id=ride_id)
            }, HTTPStatus.UNAUTHORIZED

        return {
            'msg': f'Ride "{ride_id}" Not found',
            'action': 'View all rides',
            'link': url_for('api_bp.ride_rides_resource')
        }, HTTPStatus.NOT_FOUND
