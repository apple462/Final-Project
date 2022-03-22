from flask_login import UserMixin
from app import db
from application.trackers.model.models import Tracker 

class Profile(UserMixin, db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    trackers = db.relationship('Tracker', backref='tracker', cascade="all, delete")