from models.db import db


class EventModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    description = db.Column(db.String(120), index=True)
    date = db.Column(db.DateTime, index=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))