from http import HTTPStatus
from flask.helpers import url_for
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, current_user

from .dto_requests import request_model, r_request_parser, \
            req_update_parser, req_action_parser
from app.data.controller_ride import abort_not_ride_owner,\
    abort_ride_not_found, abort_ride_owner, abort_ride_has_departed_or_done
from app.data.controller_request import abort_request_already_accepted, \
        get_ride_requests, abort_already_made_request, make_request, \
        abort_request_not_found, abort_not_request_owner, \
        update_request, delete_request, request_action



req_ns = Namespace('requests', description="Handle Ride Request Operations")


@req_ns.route('/<int:rideID>/all')
@req_ns.doc(security="Bearer")
@req_ns.param('rideID', 'ID of a ride that exists')
@req_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR.value, "Internal Server error")
@req_ns.response(HTTPStatus.UNAUTHORIZED.value, 'Invalid or missing Authorization token')
@req_ns.response(HTTPStatus.NOT_FOUND.value, "Ride does not exists")
class AllRequestsResource(Resource):
    """Handle making and fetching requests
    """
    
    @req_ns.doc('get_all_requests')
    @req_ns.response(HTTPStatus.OK.value, 'Requests were retrieved successfully')
    @req_ns.marshal_list_with(request_model)
    @jwt_required()
    def get(self, rideID):
        """Fetch all request on a ride
        """
        abort_ride_not_found(rideID) # 404
        abort_not_ride_owner(rideID, current_user.id) # 401
        reqs = get_ride_requests(rideID)
        return reqs, HTTPStatus.OK

    @req_ns.doc('make_a_request')
    @req_ns.expect(r_request_parser)
    @req_ns.response(HTTPStatus.BAD_REQUEST.value, "Cannot make a request to join your own ride")
    @req_ns.response(HTTPStatus.CONFLICT.value, "A User has has already made a request")
    @req_ns.response(HTTPStatus.CREATED.value, "Request was made successfully")
    @jwt_required()
    def post(self, rideID):
        """Make a request to join a ride
        """
        abort_ride_not_found(rideID) # 404 
        abort_ride_owner(rideID, current_user.id) #400
        abort_already_made_request(rideID, current_user.id) #409
        reqs_args = r_request_parser.parse_args()
        stop = reqs_args['stop']
        seats = reqs_args['seats']
        passenger = current_user.id
        reqID = make_request(rideID, passenger, stop, seats)
        req_url = url_for('api_bp.requests_request_resource', rideID=rideID, reqID=reqID)
        return {
            'msg': 'Your Request was Created successfully',
            'action': 'View the request for change of status',
            'link': req_url
        }, HTTPStatus.CREATED


@req_ns.route('/<int:rideID>/all/<int:reqID>')
@req_ns.doc(security="Bearer")
@req_ns.param('rideID', 'ID of a ride that exists')
@req_ns.param('reqID', 'ID of a request that exists')
@req_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR.value, "Internal Server error")
@req_ns.response(HTTPStatus.UNAUTHORIZED.value, 'Invalid or missing Authorization token')
@req_ns.response(HTTPStatus.NOT_FOUND.value, "Ride or Request does not exists")
@req_ns.response(HTTPStatus.FORBIDDEN.value, "Ride Request details cannot be changed")
class RequestResource(Resource):
    """Handle operations on a request
    """

    @req_ns.doc("change_request_details")
    @req_ns.expect(req_update_parser)
    @req_ns.response(HTTPStatus.BAD_REQUEST.value, "Ride Request details validation error")
    @req_ns.response(HTTPStatus.OK.value, "Request details were changed successfully")
    @jwt_required()
    def put(self, rideID, reqID):
        """Change the details of a request
        """
        abort_ride_not_found(rideID) #404
        abort_request_not_found(reqID) # 404
        abort_not_request_owner(reqID, current_user.id) # 401
        
        abort_request_already_accepted(reqID) # 403 
        # TODO: allow changing accepted request if more time.

        req_update_args = req_update_parser.parse_args()
        stop = req_update_args['stop']
        seats = req_update_args['seats']
        update_request(reqID, stop, seats)
        return {
            'msg': 'Your Request has been updated',
            'action': 'View the request',
            'link': url_for('api_bp.requests_request_resource', rideID=rideID, reqID=reqID)
        }, HTTPStatus.OK
    

    @req_ns.doc("withdraw_request")
    @req_ns.response(HTTPStatus.NO_CONTENT.value, "Request was removed successfully")
    @jwt_required()
    def delete(self, rideID, reqID):
        """Remove a request to join a ride
        """
        abort_ride_not_found(rideID) # 404
        abort_request_not_found(reqID) # 404
        abort_ride_has_departed_or_done(rideID) # 403
        abort_not_request_owner(reqID, current_user.id) #401
        delete_request(reqID)
        return {
            'msg': 'Your Request has been withdrawn',
            'action': 'View more rides',
            'link': url_for('api_bp.ride_rides_resource')
        }, HTTPStatus.NO_CONTENT

    @req_ns.doc("request_action")
    @req_ns.response(HTTPStatus.OK.value, "Action on Request was successful")
    @jwt_required()
    def patch(self, rideID, reqID):
        """Accept or Reject a ride
        """
        abort_ride_not_found(rideID) # 404
        abort_request_not_found(reqID) # 404
        abort_not_ride_owner(rideID, current_user.id)
        abort_ride_has_departed_or_done(rideID) # 403
        action_arg = req_action_parser.parse_args()
        action = action_arg['action']
        request_action(reqID, action)
        return{
            'msg': f'Your have "{action}" the request',
            'action': 'View More requests on this ride',
            'link': url_for('api_bp.requests_all_requests_resource', rideID=rideID)
        }, HTTPStatus.OK
