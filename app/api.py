from flask import Flask, render_template
from config import configs

from .api_BP import api_init_app
from .utils.exts import ext_init_app


def create_api(conf):
    """Creates a Flask app instance

    Args:
        conf (str): Name of Object to load configs from.
    """

    app = Flask(__name__) # named app to avoid confusion with restplus Api
    app.config.from_object(configs[conf])
    
    api_init_app(app) # for the API
    ext_init_app(app)

    @app.route("/")
    def home():
        title = app.config["API_TITLE"]
        return render_template("home.html", title=title)
    
    return app
