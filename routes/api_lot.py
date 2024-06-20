from flask import Blueprint, jsonify, make_response, request
from controllers.lotController import LotController
from util.utilities.errors import Errors
from controllers.authentication.auth import token_required
api_lot = Blueprint("api_lot", __name__)

controllerlot = LotController()

@api_lot.route('/save/lot', methods=['POST'])
def save():
    data = request.get_json()
    lote_id = controllerlot.save_lot(data)
    lots_data = controllerlot.list_all_lot()
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": lots_data}),
        200
    )

@api_lot.route('/lot', methods=['Get'])
def listlots():
    lots_data = controllerlot.list_all_lot()
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": lots_data}),
        200
    )