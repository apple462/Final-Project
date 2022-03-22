from flask import current_app as app, redirect, url_for
from flask import render_template, request
from flask_login import login_required, current_user
from application.trackers.model.models import Tracker, Logs
from app import db
import datetime


@login_required
@app.route("/tracker/<tracker_id>/log", methods = ["GET", "POST"])
def tracker_log(tracker_id):
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    date_time = datetime.datetime.now()
    local_timestamp = date_time.strftime("%Y-%m-%dT%H:%M")
    print(local_timestamp)
    if request.method == "GET":
        if tracker.type == "Multiple Choice":
            return render_template("tracker-log.html", name = current_user.name, choices = tracker.settings.split(","), local_timestamp = local_timestamp)
        else:
            return render_template("tracker-log.html", name = current_user.name, tracker_type = tracker.type, local_timestamp = local_timestamp)

    elif request.method == "POST":
        when = request.form["when"]
        value = request.form["value"]
        note = request.form["note"]
        tracker_entry = Logs(timestamp=when, value=value, note=note, tracker=tracker.id)
        
        db.session.add(tracker_entry)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            print("Rolling back")
        return redirect(url_for("index"))


@login_required
@app.route("/tracker/<tracker_id>/log/<log_id>/edit", methods = ["GET", "POST"])
def tracker_log_edit(tracker_id, log_id):
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    log = Logs.query.filter_by(id=log_id).first()

    if request.method == "GET":
        if tracker.type == "Multiple Choice":
            return render_template("tracker-log-edit.html", name = current_user.name, choices = tracker.settings.split(","), log = log)
        else:
            return render_template("tracker-log-edit.html", name = current_user.name, tracker_type = tracker.type, log = log)
        
    elif request.method == "POST":
        log.timestamp = request.form["when"]
        log.value = request.form["value"]
        log.note = request.form["note"]
        
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            print("Rolling back")
        return redirect(f"/tracker/{tracker_id}")


@login_required
@app.route("/tracker/<tracker_id>/log/<log_id>/delete", methods = ["GET", "POST"])
def tracker_log_delete(tracker_id, log_id):
    log = Logs.query.filter_by(id=log_id).first()
    
    db.session.delete(log)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        print("Rolling back")
    return redirect(f"/tracker/{tracker_id}")