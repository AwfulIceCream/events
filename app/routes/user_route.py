from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from app.models import UserModel
from schemas import UserGetSchema, EventSchema

blp = Blueprint("User", __name__, url_prefix="/users", description="User operations")


@blp.route('/')
class UserList(MethodView):
    @blp.response(200, UserGetSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return UserGetSchema(many=True).dump(users)


@blp.route('/<int:user_id>/events')
class UserEventsResource(MethodView):
    @jwt_required()
    @blp.response(200, EventSchema(many=True))
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(404, message="User not found.")

        events = user.attending

        return EventSchema(many=True).dump(events)
