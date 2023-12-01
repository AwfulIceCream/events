from app.models.db import db
from .user import attendees


class EventModel(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    description = db.Column(db.String(120))
    date = db.Column(db.DateTime, index=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Define the many-to-one relationship with UserModel
    creator = db.relationship('UserModel', back_populates='created_events')

    # Define the many-to-many relationship with UserModel
    attendees = db.relationship('UserModel', secondary=attendees, back_populates='attending')