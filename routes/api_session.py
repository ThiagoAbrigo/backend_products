from flask import Blueprint, jsonify, make_response, request
from controllers.authentication.sessionController import SessionController
from util.utilities.errors import Errors

# from flask_expects_json import expects_json
from controllers.authentication.auth import token_required

api_session = Blueprint("api_session", __name__)

sessionController = SessionController()


@api_session.route("/signUp", methods=["POST"])
# @expects_json(schema_session)
def signUp():
    data = request.json
    response = sessionController.signUp(data)
    if "user" in response and "token" in response:
        user = response["user"].serialize
        token = response["token"]
        return make_response (
            jsonify(
                {"message": "User signed up successfully", "user": user, "token": token}
            ),
            200,
        )
    else:
        return make_response(
            jsonify(
                {"error": "Failed to sign up user"}
            )
            , 400,
        ) 
        
@api_session.route("/login", methods=['POST'])
# @token_required
def session():
    data = request.json
    id = sessionController.login(data)

    if type(id) == int:
        return make_response(
            jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Errors.error.get(str(id))}}), 
            400
        )
    else:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": id}),
            200
        )
