from flask import Flask, Blueprint
from flask_restx import Api

from .ns_auth import auth_ns as Authentication_NS
from .ns_ride import ride_ns as Ride_NS
from .ns_requests import req_ns as RideRequests_NS


api_bp = Blueprint("api_bp", __name__, url_prefix="/api")

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }  # expexted Authorization: Bearer <JWT>
}



api = Api(api_bp, authorizations=authorizations)
api.add_namespace(Authentication_NS, path='/auth')
api.add_namespace(Ride_NS, path='/rides')
api.add_namespace(RideRequests_NS, path='/requests')


def api_init_app(app: Flask):
    """initialize the api with app configs

    Args:
        app (Flask): [description]
    """
    app.register_blueprint(api_bp)
    api.title = app.config['API_TITLE']
    api.version = app.config['API_VERSION']
    api.description = app.config["API_DESCRIPTION"]


