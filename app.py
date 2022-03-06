import os
from flask import Flask
from application.config import LocalDevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

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
api = Api(app)
app.app_context().push()
db.init_app(app)


# Controllers 
from application.authentication.controller import *
from application.trackers.controller.tracker_controller import *
from application.trackers.controller.log_controller import *


# Views 
from application.trackers.view.tracker_view import *
from application.trackers.view.log_view import *


# API 
api.add_resource(TrackerAPI, "/api/tracker", "/api/tracker/<int:tracker_id>")
api.add_resource(LogAPI, "/api/tracker/<int:tracker_id>/log", "/api/tracker/<int:tracker_id>/log/<int:log_id>")
api.add_resource(LogPeriodAPI, "/api/tracker/<int:tracker_id>/logs/<int:period>")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
