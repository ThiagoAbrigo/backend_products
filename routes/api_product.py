from flask import Blueprint, jsonify, make_response, request, send_from_directory
from controllers.productController import ProductController
from util.utilities.errors import Errors
from controllers.authentication.auth import token_required

api_product = Blueprint("api_product", __name__)

productController = ProductController()

@api_product.route("/save/product", methods=["POST"])
@token_required
def save_product_route():
    try:
        data = request.form.to_dict()

        # Obtener el archivo de imagen
        if 'image' not in request.files:
            return make_response(
                jsonify({"msg": "ERROR", "code": 400, "data": {"error": "No se proporcionó ninguna imagen"}}),
                400,
            )
        image_file = request.files['image']

        if image_file.filename == '':
            return make_response(
                jsonify({"msg": "ERROR", "code": 400, "data": {"error": "Nombre de archivo de imagen no válido"}}),
                400,
            )

        result = productController.save_product(data, image_file)
        if result == -4:
            return make_response(
                jsonify({"msg": "ERROR", "code": 400, "data": {"error": "Error al guardar el producto"}}),
                400,
            )

        return jsonify({"msg": "OK", "code": 200, "data": result.serialize}), 200

    except Exception as e:
        return make_response(
            jsonify({"msg": "ERROR", "code": 500, "data": {"error": str(e)}}),
            500,
        )
@api_product.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@api_product.route("/listproduct/buenos", methods=["GET"])
@token_required
def list_product_unexpired():
    unexpired_products = productController.list_buenos()
    return make_response(
        jsonify({
            'message': 'OK',
            'code': 200, 
            'data': ([i.serialize for i in unexpired_products])
        }),
        200
    )

@api_product.route("/listproduct/images", methods=["GET"])
def list_product_images():
    products = productController.listar_images() 
    if products is None:
        print("No products returned from listar_images")
        products = []
    images = [{"name": p.name, "image_path": p.image_path} for p in products]
    return make_response(
        jsonify({
            'message': 'OK',
            'code': 200, 
            'data': images
        }),
        200
    )
    

@api_product.route("/listproduct/caducados", methods=["GET"])
@token_required
def list_product_expired():
    expired_products = productController.lista_de_caducados()
    return make_response(
        jsonify({
            'message': 'OK',
            'code': 200, 
            'data': ([i.serialize for i in productController.list_caducado()])
        }),
        200
    )

@api_product.route("/listproduct/expired_5days", methods=["GET"])
@token_required
def list_product_expired_5days():
    expired_products = productController.lista_de_porCaducar()
    return make_response(
        jsonify({
            'message': 'OK',
            'code': 200, 
            'data': ([i.serialize for i in productController.list_porcaducar()])
        }),
        200
    )
    
@api_product.route("/listproduct", methods=["GET"])
@token_required
def list_products():
    products = productController.list_products()
    return make_response(
        jsonify({
            'message': 'OK',
            'code': 200, 
            'data': products
        }),
        200
    )
    
@api_product.route("/list_status", methods=['GET'])
def listar_estados():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "data": productController.listar_estados()}),
        200
    )  
@api_product.route("/modify_product/<external_id>", methods=["POST"])
@token_required
def modifyPerson(external_id):
    data = request.get_json()
    result = productController.modify_product(external_id, data)
    if result:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "data": result}),
            200,
        )
    else:
        return make_response(
            jsonify({"msg" : "ERROR", "code" : 404, "datos" :{"error" : "Persona no encontrada"}}), 
            404
        )
@api_product.route("/update/product/image/<external_id>", methods=["POST"])
def update_product_image(external_id):
    try:
        image_file = request.files['image']

        if 'image' not in request.files or not image_file:
            return make_response(
                jsonify({"msg": "ERROR", "code": 400, "data": {"error": "No se proporcionó ninguna imagen"}}),
                400,
            )

        result, status_code = productController.update_product_image(external_id, image_file)
        return make_response(jsonify(result), status_code)

    except Exception as e:
        return make_response(
            jsonify({"msg": "ERROR", "code": 500, "data": {"error": str(e)}}),
            500,
        )