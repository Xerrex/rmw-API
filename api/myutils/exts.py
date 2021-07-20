from flask_restplus import Api

api = Api()

def ext_init_app(app):
    """Initialize apps with the Flask App

    Args:
        app (Flask): Instance of a Flask app
    """
    api.init_app(app)