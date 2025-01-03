from functools import wraps

import jwt
from flask import current_app, jsonify, request

from server import db
from server.models.user import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = db.session.get(User, data["id"])
            if not current_user:
                return jsonify({"error": "Invalid token!"}), 401
        except Exception as e:
            print(f"Error decoding token: {e}")
            return jsonify({"error": "Token is invalid!"}), 401
        return f(current_user=current_user, *args, **kwargs)

    return decorated
