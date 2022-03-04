import os
from flask import Flask, redirect, request, url_for
from application.config import LocalDevelopmentConfig
# from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

app = None
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = "internaluseonly"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quantifiedself.sqlite3"
    if os.getenv("ENV", "development") == "production":
        raise Exception("Currently no production config is setup")
    else:
        print("Starting local development server")
        app.config.from_object(LocalDevelopmentConfig)
        return app


app = create_app()
app.app_context().push()
db.init_app(app)


from application.authentication.controller import *
from application.trackers.tracker_controller import *
from application.trackers.log_controller import *


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
