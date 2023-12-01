from models.attendees import attendees
from models.db import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String())
    created_events = db.relationship('Event', backref='creator', lazy='dynamic')
    attending = db.relationship('Event', secondary=attendees, backref=db.backref('attendees', lazy='dynamic'))
