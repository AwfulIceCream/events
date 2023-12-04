from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt
)
from passlib.hash import pbkdf2_sha256

from app.models.db import db
from app.models import UserModel
from app.schemas import RegisterUserSchema, LoginUserSchema

blp = Blueprint("Auth", __name__, url_prefix="/api/v1/auth", description="Authentication operations")

BLOCKLIST = set()


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(RegisterUserSchema)
    def post(self, user_data):
        """
        Register user
        """
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="A user with that email already exists.")

        user = UserModel(
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            name=user_data["name"],
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(LoginUserSchema)
    def post(self, user_data):
        """
        User login
        """
        user = UserModel.query.filter(UserModel.email == user_data["email"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

        abort(401, message="Invalid credentials.")


@blp.route("/logout", methods=["POST"])
@jwt_required()
def post():
    """
    Logout
    """
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return {"message": "Successfully logged out"}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        """
        Get refresh token
        """
        abort(409, massage=f"{get_jwt()}")
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200
