from flask import request
from flask_restful import Resource, Api, fields, marshal_with
from application.trackers.model.models import Tracker
from app import db

Tracker_output = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "type": fields.String,
    "settings": fields.String,
}

class TrackerAPI(Resource):
    @marshal_with(Tracker_output)
    def get(self, tracker_id=None):
        if tracker_id == None:
            return Tracker.query.all()
        else:
            tracker = Tracker.query.filter_by(id=tracker_id).first()
            if tracker:
                return tracker  
            else:
                return {"error": "Tracker not found"}, 404
    
    @marshal_with(Tracker_output)
    def post(self):
        tracker = request.get_json()
        print("POST", tracker)
        if not tracker:
            return {"error": "No data in request"}, 400
        else:
            if "name" not in tracker:
                return {"error": "No name in request"}, 400
            
            if "description" not in tracker:
                return {"error": "No description in request"}, 400
            
            if "type" not in tracker:
                return {"error": "No type in request"}, 400
            elif tracker["type"] not in ["Numerical", "Multiple Choice", "Time Duration", "Boolean"]:
                return {"error": "Invalid type in request"}, 400
            
            if tracker["type"] == "Mutliple Choice":
                if "settings" not in tracker:
                    return {"error": "No settings in request"}, 400

            if "settings" not in tracker:
                new_tracker = Tracker(name=tracker["name"], description=tracker["description"], type=tracker["type"])
            else:
                new_tracker = Tracker(name=tracker["name"], description=tracker["description"], type=tracker["type"], settings=tracker["settings"])

            db.session.add(new_tracker)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                print("Rolling back")
            return new_tracker, 201


    def delete(self, tracker_id):
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        if tracker:
            db.session.delete(tracker)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                print("Rolling back")
        else:
            return {"error": "Tracker not found"}, 404

    
    @marshal_with(Tracker_output)
    def put(self, tracker_id):
        tracker = Tracker.query.filter_by(id=tracker_id).first()
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
            return {"error": "Tracker not found"}, 404