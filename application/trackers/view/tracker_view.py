from flask import request
from flask_restful import Resource, Api, fields, marshal_with
from application.trackers.model.models import Tracker
from main import db
from .error import *

Tracker_output = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "type": fields.String,
    "settings": fields.String,
}

class TrackerAPI(Resource):
    @marshal_with(Tracker_output)
    def get(self, user_id, tracker_id=None):

        if tracker_id == None:
            trackers = Tracker.query.filter_by(user=user_id).all()
            if trackers:
                return trackers
            else:
                raise NotFoundError( item = 'Tracker/User')
        else:
            tracker = Tracker.query.filter_by(id=tracker_id, user = user_id).first()
            if tracker:
                return tracker  
            else:
                print("Tracker not found")
                raise NotFoundError( item = 'Tracker/User')
    
    @marshal_with(Tracker_output)
    def post(self, user_id):
        tracker = request.get_json()
        print("POST", tracker)
        if not tracker:
            raise BadRequestError(message = 'No data in request')
        else:
            if "name" not in tracker:
                raise BadRequestError(message = 'No name in request')
            
            if "description" not in tracker:
                raise BadRequestError(message = 'No description in request')
            
            if "type" not in tracker:
                raise BadRequestError(message = 'No type in request')
            elif tracker["type"] not in ["Numerical", "Multiple Choice", "Time Duration", "Boolean"]:
                raise BadRequestError(message = 'Invalid type in request')
            
            if tracker["type"] == "Mutliple Choice":
                if "settings" not in tracker:
                    raise BadRequestError(message = 'No settings in request')

            if "settings" not in tracker:
                new_tracker = Tracker(name=tracker["name"], description=tracker["description"], type=tracker["type"], user=user_id)
            else:
                new_tracker = Tracker(name=tracker["name"], description=tracker["description"], type=tracker["type"], settings=tracker["settings"], user=user_id)

            db.session.add(new_tracker)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                print("Rolling back")
            return new_tracker, 201


    def delete(self, tracker_id, user_id):
        tracker = Tracker.query.filter_by(id=tracker_id, user=user_id).first()
        if tracker:
            db.session.delete(tracker)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                print("Rolling back")
        else:
            raise NotFoundError( item = 'Tracker/User')

    
    @marshal_with(Tracker_output)
    def put(self, tracker_id, user_id):
        tracker = Tracker.query.filter_by(id=tracker_id, user=user_id).first()
        if tracker:
            new_tracker = request.get_json()
            if "name" in new_tracker:
                tracker.name = new_tracker["name"]
            if "description" in new_tracker:
                tracker.description = new_tracker["description"]
            if "type" in new_tracker:
                tracker.type = new_tracker["type"]
            if "settings" in new_tracker:
                tracker.settings = new_tracker["settings"]
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                print("Rolling back")
            return tracker
        else:
            raise NotFoundError( item = 'Tracker/User')