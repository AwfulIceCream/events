from .db import db

attendees = db.Table('attendees',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
                     )


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String())

    # Correctly define the many-to-many relationship

    attending = db.relationship('EventModel', secondary=attendees, back_populates='attendees')

    created_events = db.relationship('EventModel', back_populates='creator', lazy='dynamic')
