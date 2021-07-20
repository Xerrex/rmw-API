from flask import Flask, render_template
from config import configs


def create_api(conf):
    """Creates a Flask app instance

    Args:
        conf (str): Name of Object to load configs from.
    """

    app = Flask(__name__) # named app to avoid confusion with restplus Api
    app.config.from_object(configs[conf])

    @app.route("/")
    def home():
        title = app.config["API_TITLE"]
        return render_template("home.html", title=title)
    
    return app
