from flask import request
from flask_restful import Resource, Api, fields, marshal_with
from application.trackers.model.models import Logs, Tracker
from app import db
from datetime import datetime, timedelta, date


Log_output = {
    "id": fields.Integer,
    "timestamp": fields.String,
    "tracker": fields.String,
    "value": fields.String,
    "note": fields.String,
}

class LogAPI(Resource):
    @marshal_with(Log_output)
    def get(self, tracker_id, log_id=None):
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        if tracker == None:
            return {"error": "Tracker not found"}, 404

        if log_id != None:
            log = Logs.query.filter_by(id=log_id, tracker = tracker_id).first()
            if log:
                log.tracker = tracker.name
                return log
            else:
                return {"error": "Log not found"}, 404

        else:
            logs = Logs.query.filter_by(tracker = tracker_id).all()
            for log in logs:
                log.tracker = tracker.name
            return logs

    @marshal_with(Log_output)
    def post(self, tracker_id):
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        if tracker == None:
            return {"error": "Tracker not found"}, 404

        log = request.get_json()
        print("POST", log)
        if not log:
            return {"error": "No data in request"}, 400
        else:
            if "value" not in log:
                return {"error": "No value in request"}, 400

            elif "note" not in log:
                return {"error": "No note in request"}, 400

            elif "timestamp" not in log:
                return {"erorr": "No timestamp in request"}, 400

            else:
                new_log = Logs(tracker=tracker_id, value=log["value"], note=log["note"], timestamp = log["timestamp"])
                db.session.add(new_log)
                try:
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    print("Rolling back")
                return new_log, 201

    def delete(self, tracker_id, log_id):
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        if tracker == None:
            return {"error": "Tracker not found"}, 404

        log = Logs.query.filter_by(id=log_id, tracker = tracker_id).first()
        if log == None:
            return {"error": "Log not found"}, 404

        db.session.delete(log)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            print("Rolling back")
        return log, 201

    @marshal_with(Log_output)
    def put(self, tracker_id, log_id):
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        if tracker == None:
            return {"error": "Tracker not found"}, 404

        log = Logs.query.filter_by(id=log_id, tracker = tracker_id).first()
        if log == None:
            return {"error": "Log not found"}, 404

        new_log = request.get_json()
        if "timestamp" in new_log:
            log.timestamp = new_log["timestamp"]
        if "value" in new_log:
            log.value = new_log["value"]
        if "note" in new_log:
            log.note = new_log["note"]
        
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            print("Rolling back")
        return log, 201


class LogPeriodAPI(Resource):
    def get(self, tracker_id, period):
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        if tracker == None:
            return {"error": "Tracker not found"}, 404

        logs = Logs.query.filter_by(tracker = tracker_id).all()
        value = []
        timestamp =[]
        today = date.today()
        for log in logs:
            date_str = log.timestamp[:10]
            date_time_obj = datetime.strptime(date_str, '%Y-%m-%d')
            
            if period == "0":
                value.append(log.value)
                timestamp.append(log.timestamp)

            elif period =="1":
                if date_time_obj.date() == today:
                    value.append(log.value)
                    timestamp.append(log.timestamp)

            else:
                if date_time_obj.date() >= today - timedelta(days=int(period)):
                    value.append(log.value)
                    timestamp.append(log.timestamp)

        return {"value": value, "timestamp": timestamp}, 200