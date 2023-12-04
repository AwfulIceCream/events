from marshmallow import Schema, fields, validate


class RegisterUserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, error="Password must be at least 8 characters long")
        ],
    )


class LoginUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=64))
    description = fields.Str(required=True, validate=validate.Length(max=120))
    date = fields.Str(required=True)
    creator_id = fields.Int(dump_only=True)

    @staticmethod
    def make_event(data, **kwargs):
        # Allow loading both single and multiple instances
        many = kwargs.get('many', False)
        return EventSchema(many=many).load(data)


class UpdateEventSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(validate=validate.Length(max=64))
    description = fields.Str(validate=validate.Length(max=120))
    date = fields.Str()
    creator_id = fields.Int()


class UserGetSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Str()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Str()
    password = fields.Str(load_only=True)
    created_events = fields.Nested(EventSchema(), many=True, exclude=('creator',))
    attending = fields.Nested(EventSchema(), many=True)
