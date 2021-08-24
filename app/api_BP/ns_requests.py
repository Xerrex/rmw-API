from http import HTTPStatus
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, current_user

from .dto_requests import request_model
from app.data.controller_ride import abort_not_ride_owner,\
        abort_ride_not_found, abort_ride_owner
from app.data.controller_request import get_ride_requests


req_ns = Namespace('requests', description="Handle Ride Request Operations")
req_ns.models[request_model.name] = request_model


@req_ns.route('/<int:rideID>/all')
@req_ns.doc(security="Bearer")
@req_ns.param('rideID', 'ID of a ride that exists')
@req_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server error")
@req_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Invalid or missing Authorization token')
@req_ns.response(int(HTTPStatus.NOT_FOUND), "Ride does not exists")
class AllRequestsResource(Resource):
    """Handle making and fetching requests
    """
    
    @req_ns.doc('get_all_requests')
    @req_ns.response(int(HTTPStatus.OK), 'Requests were retrieved successfully')
    @req_ns.marshal_list_with(request_model)
    @jwt_required()
    def get(self, rideID):
        """Fetch all request on a ride
        """
        abort_ride_not_found(rideID)
        abort_not_ride_owner(rideID, current_user.id)
        reqs = get_ride_requests(rideID)
        return reqs, HTTPStatus.OK

    @req_ns.doc('make_a_request')
    @req_ns.expect(request_model)
    @req_ns.response(int(HTTPStatus.BAD_REQUEST), "Cannot make a request to join your own ride")
    @req_ns.response(int(HTTPStatus.CONFLICT), "A Request has already been made")
    @req_ns.response(int(HTTPStatus.CREATED), "Request was made successfully")
    @jwt_required()
    def post(self, rideID):
        """Make a request to join a ride
        """
        abort_ride_not_found(rideID) # 404 
        abort_ride_owner(rideID, current_user.id) #400

        # TODO: Check if current user has a request
        # TODO: Get Request data



@req_ns.route('/<int:rideID>/all/<int:reqID>')
@req_ns.doc(security="Bearer")
@req_ns.param('rideID', 'ID of a ride that exists')
@req_ns.param('reqID', 'ID of a request that exists')
@req_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal Server error")
@req_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Invalid or missing Authorization token')
@req_ns.response(int(HTTPStatus.NOT_FOUND), "Ride or Request does not exists")
class RequestResource(Resource):
    """Handle operations on a request
    """

    @req_ns.doc("change_request_details")
    @req_ns.response(int(HTTPStatus.BAD_REQUEST), "Ride Request details validation error")
    @req_ns.response(int(HTTPStatus.OK), "Request details were changed successfully")
    def put(self, rideID, reqID):
        """Change the details of a request
        """
        # TODO: check if ride exists
        # TODO: Check if request exist
        # TODO: Check if request status is accepted.
        # TODO: check if owner of request
        # TODO: Get request data
        # TODO: Update request details
        pass
    
    @req_ns.doc("remove_request")
    @req_ns.response(int(HTTPStatus.NO_CONTENT), "Request was removed successfully")
    def delete(self, rideID, reqID):
        """Remove a request to join a ride
        """
        # TODO: Check if ride exists
        # TODO: Check if request exist
        # TODO: Check if ride has happened.
        # TODO: Check if Owner of request.
        # TODO: Remove Request
        pass

    @req_ns.doc("accept_or_reject_request")
    @req_ns.response(int(HTTPStatus.OK), "Action on Request was successful")
    def patch(self, rideID, reqID):
        """Accept or Reject a ride
        """
        # TODO: Check if ride exists
        # TODO: Check if request exist
        # TODO: Check if ride has happened.
        # TODO: Check if Owner of ride
        # TODO: Approve the request
        pass
