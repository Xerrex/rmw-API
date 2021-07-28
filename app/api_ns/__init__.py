from flask import Flask, Blueprint
from flask_restx import Api

from .auth_ns import auth_ns as Authentication_NS


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


def api_init_app(app: Flask):
    """initialize the api with app configs

    Args:
        app (Flask): [description]
    """
    app.register_blueprint(api_bp)
    api.title = app.config['API_TITLE']
    api.version = app.config['API_VERSION']
    api.description = app.config["API_DESCRIPTION"]


