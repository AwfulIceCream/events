from datetime import datetime

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.db import db
from app.models import EventModel
from app.models import UserModel
from app.schemas import EventSchema, UpdateEventSchema, UserGetSchema

blp = Blueprint('Events', __name__, url_prefix='/events', description='Operations on events')


@blp.route('')
class EventsList(MethodView):
    @blp.response(200, EventSchema(many=True))
    def get(self):
        """
        Get all events
        """
        events = EventModel.query.all()
        return EventSchema(many=True).dump(events)

    @jwt_required()
    @blp.arguments(EventSchema)
    @blp.response(201, EventSchema)
    def post(self, new_data):
        """
        Add an event
        """
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        datetime_object = datetime.strptime(new_data["date"], "%Y-%m-%dT%H:%M:%S")
        if not user:
            abort(404, message="User not found.")
        event = EventModel(title=new_data["title"], description=new_data["description"], date=datetime_object,
                           creator=user)
        db.session.add(event)
        db.session.commit()
        return EventSchema().dump(event), 201


@blp.route('/<int:event_id>')
class EventResource(MethodView):
    @jwt_required()
    @blp.response(200, EventSchema)
    def get(self, event_id):
        """
        Get event by id
        """
        event = EventModel.query.get_or_404(event_id)
        if not event:
            abort(404, message="Event not found.")
        return EventSchema().dump(event)

    @blp.arguments(UpdateEventSchema)
    @blp.response(200, UpdateEventSchema)
    @jwt_required()
    def put(self, update_data, event_id):
        """
        Update event by id
        """
        event = EventModel.query.get_or_404(event_id)
        if not event:
            abort(404, message="Event not found.")
        if event.creator.id != get_jwt_identity():
            abort(403, message="User not authorized to edit this event.")

        for key, value in update_data.items():
            setattr(event, key, value)
        db.session.add(event)
        db.session.commit()
        return EventSchema().dump(event)

    @jwt_required()
    @blp.response(204)
    def delete(self, event_id):
        """
        Delete event by id
        """
        event = EventModel.query.get_or_404(event_id)
        if not event:
            abort(404, message="Event not found.")
        if event.creator.id != get_jwt_identity():
            abort(403, message="User not authorized to delete this event.")
        db.session.delete(event)
        db.session.commit()
        return '', 204


@blp.route('/<int:event_id>/attend/<int:user_id>')
class AttendEventResource(MethodView):
    @jwt_required()
    @blp.response(200, EventSchema)
    def post(self, event_id, user_id):
        """
        Attend user to event by id
        """
        event = EventModel.query.get_or_404(event_id)
        if not event:
            abort(404, message="Event not found.")

        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(404, message="User not found.")

        if event.creator != get_jwt_identity():
            abort(404, message="This user has no permission on this event.")

        event.attendees.append(user)

        db.session.add(event)
        db.session.commit()

        return EventSchema().dump(event)


@blp.route('/<int:event_id>/attendees')
class EventAttendeesResource(MethodView):
    @jwt_required()
    @blp.response(200, UserGetSchema(many=True))
    def get(self, event_id):
        """
        Get all attendees by event id
        """
        event = EventModel.query.get(event_id)
        if not event:
            abort(404, message="Event not found.")

        attendees = event.attendees

        return UserGetSchema(many=True).dump(attendees)
