from datetime import timedelta
from flask import Flask

def create_app():
    app = Flask(__name__)
    # [ KEYS AND CONSTRUCTORS ]
    app = Flask(
        __name__
    )  # Flask constructor takes the name of current module (__name__) as argument.
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:yash1234@localhost/tupi"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "hello123"
    app.permanent_session_lifetime = timedelta(minutes=5)
    return app