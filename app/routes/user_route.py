from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from app.models import UserModel
from app.schemas import UserGetSchema, EventSchema, UserUpdateSchema
from ..models.db import db

blp = Blueprint("User", __name__, url_prefix="/api/v1/users", description="User operations")


@blp.route('')
class UserList(MethodView):
    @blp.response(200, UserGetSchema(many=True))
    def get(self):
        """
        Get all users
        """
        users = UserModel.query.all()
        return UserGetSchema(many=True).dump(users)


@blp.route('/<int:user_id>/events')
class UserEventsResource(MethodView):
    @jwt_required()
    @blp.response(200, EventSchema(many=True))
    def get(self, user_id):
        """
        Get all events for user by id
        """
        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(404, message="User not found.")

        events = user.attending

        return EventSchema(many=True).dump(events)


@blp.route('/<int:user_id>')
class UserEventsResource(MethodView):
    @jwt_required()
    @blp.response(200, UserGetSchema)
    def get(self, user_id):
        """
        Get user by id
        """
        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(404, message="User not found.")
        return UserGetSchema().dump(user)

    @jwt_required()
    @blp.response(200, UserGetSchema)
    @blp.arguments(UserUpdateSchema)
    def put(self, user_data, user_id):
        """
        Update user by id
        """
        #user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)

        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
        else:
            user = UserModel(id=UserModel, **user_data)
            db.session.add(user)

        db.session.commit()

        return user

    def delete(self, user_id):
        """
        Delete user by id
        """
        #user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(404, message="User not found.")

        db.session.delete(user)
        db.session.commit()

        return 204