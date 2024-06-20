from flask import Flask, request, jsonify, make_response, current_app
from flask_sqlalchemy import SQLAlchemy
import jwt
from functools import wraps
from models.user import User
from util.utilities.errors import Errors

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']

        if not token:
            return make_response(
                jsonify({"msg": "ERROR", "code": 400, "data": {"error": "first, generate your token"}}),
                401
            )

        try:
            data = jwt.decode(token, key=current_app.config['SECRET_KEY'], algorithms=["HS512"])
            user = User.query.filter_by(external_id=data["external_id"]).first()
            if not user:
                return make_response(
                    jsonify({"msg": "ERROR", "code": 401, "data": {"error": "Unauthorized"}}),
                    401
                )

        except jwt.ExpiredSignatureError:
            return make_response(
                jsonify({"msg": "ERROR", "code": 401, "data": {"error": "Token has expired"}}),
                401
            )
        except jwt.InvalidTokenError:
            return make_response(
                jsonify({"msg": "ERROR", "code": 401, "data": {"error": "Invalid token"}}),
                401
            )

        return f(*args, **kwargs)

    return decorated