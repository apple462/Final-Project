from main import db

class Tracker(db.Model):
    __tablename__ = "tracker"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    type = db.Column(db.String)
    settings = db.Column(db.String)
    user = db.Column(db.Integer, db.ForeignKey("profile.id", ondelete="CASCADE"), nullable = False)
    logs = db.relationship('Logs', backref='log', cascade="all, delete")


class Logs(db.Model):
    __tablename__ = "log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.String, nullable=False)
    tracker = db.Column(db.Integer, db.ForeignKey("tracker.id", ondelete="CASCADE"), nullable = False)
    value = db.Column(db.String)
    note = db.Column(db.String)
