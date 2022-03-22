from flask import current_app as app, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from application.trackers.model.models import Tracker, Logs
from application.trackers.utils import create_graph
from app import db
from datetime import datetime, date, timedelta

@login_required
@app.route("/index", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        tracker_list = []
        trackers = Tracker.query.filter_by(user = current_user.id).all()
        for tracker in trackers:
            recent_log = Logs.query.filter_by(tracker=tracker.id).order_by(Logs.timestamp.desc()).first()
            if recent_log:
                recent_timestamp = recent_log.timestamp
            else:
                recent_timestamp = "NA"
            tracker_list.append({"id": tracker.id, "name": tracker.name, "timestamp": recent_timestamp})
        return render_template("index.html", name=current_user.name, trackers=tracker_list)


@login_required
@app.route("/tracker/<int:tracker_id>", methods = ["GET", "POST"])
def tracker(tracker_id):
    if request.method == "GET":
        logs = Logs.query.filter_by(tracker=tracker_id).all() 
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        value = []
        timestamp = []
        for log in logs:
            value.append(log.value)
            timestamp.append(log.timestamp)
        create_graph(value, timestamp)

        return render_template("tracker-detail.html", logs=logs, name=current_user.name, tracker=tracker)

    elif request.method == "POST":
        period = request.form["period"]
        print(period)
        logs = Logs.query.filter_by(tracker=tracker_id).all() 
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        value = []
        timestamp = []
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

        create_graph(value, timestamp)
        return render_template("tracker-detail.html", logs=logs, name=current_user.name, tracker=tracker, period = period)


@login_required
@app.route("/tracker-add", methods = ["GET", "POST"])
def tracker_add():
    if request.method == "GET":
        return render_template("tracker-add.html", name = current_user.name)

    elif request.method == "POST":
        name = request.form["name"].capitalize()
        desc = request.form["desc"]
        tracker_type = request.form["type"]

        if tracker_type == "Multiple Choice":
            settings = request.form["settings"]
            tracker = Tracker(name=name, description=desc, type=tracker_type, settings=settings, user=current_user.id)
        else:
            tracker = Tracker(name=name, description=desc, type=tracker_type, user=current_user.id)
        
        db.session.add(tracker)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            print("Rolling back")
        return redirect(url_for("index"))


@login_required
@app.route("/tracker/<tracker_id>/edit", methods = ["GET", "POST"])
def tracker_edit(tracker_id):
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    
    if request.method == "GET":
        return render_template("tracker-edit.html", name = current_user.name, tracker_name = tracker.name, desc = tracker.description, tracker_type = tracker.type, settings = tracker.settings)

    elif request.method == "POST":
        tracker.name = request.form["name"]
        tracker.description = request.form["desc"]
        tracker.type = request.form["type"]
        if tracker.type == "Multiple Choice":
            tracker.settings = request.form["settings"]
            
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            print("Rolling back")
        return redirect(url_for("index"))


@login_required
@app.route("/tracker/<tracker_id>/delete", methods = ["GET", "POST"])
def tracker_delete(tracker_id):
    tracker = Tracker.query.filter_by(id=tracker_id).first()
 
    db.session.delete(tracker)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        print("Rolling back")
    return redirect(url_for("index"))