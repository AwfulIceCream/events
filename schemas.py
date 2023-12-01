from marshmallow import Schema, fields, post_load
from models import UserModel, EventModel


class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    date = fields.DateTime()
    creator = fields.Nested(lambda: UserSchema(only=('id', 'name')))

    @post_load
    def make_event(self, data, **kwargs):
        return EventModel(**data)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Str()
    password = fields.Str(load_only=True)
    created_events = fields.Nested(EventSchema(), many=True, exclude=('creator',))
    attending = fields.Nested(EventSchema(), many=True)

    @post_load
    def make_user(self, data, **kwargs):
        return UserModel(**data)
