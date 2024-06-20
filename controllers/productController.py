from models.product import Product
from app import db
from datetime import datetime, timezone, timedelta
from freezegun import freeze_time
from models.lot import Lot
import uuid
from models.typestatus import TypeStatus
import os
from flask import request, current_app
from werkzeug.utils import secure_filename 
from flask import jsonify
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'

class ProductController:
    def list_products(self):
        products = Product.query.all()
        product_List = []
        for product in products:
            lot = product.lot
            data = {
                "external_id": product.external_id,
                "name": product.name,
                "date_expiry": product.date_expiry,
                "price": product.price,
                "image_path": product.image_path,
                "status": product.status.serialize if product.status else None,
                "stock": product.stock,
                "lot": lot.code if lot else None
            }
            product_List.append(data)
        return product_List
    
    def list_buenos(self):
        return Product.query.filter_by(status="BUENO").all()
        
    def list_caducado(self):
        return Product.query.filter_by(status="CADUCADO").all()
    
    def list_porcaducar(self):
        return Product.query.filter_by(status="POR_CADUCAR").all()
    
    def listar_estados(self):
        return [e.value for e in TypeStatus]
    
    def listar_images(self):
        products = Product.query.all()
        if not products:
            print("No products found")
            return []
        print(f"Found {len(products)} products")
        return products
    
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            
    def save_product(self, data, image_file):
        print("**********Received data:", data)
        try:
            lot = Lot.query.filter_by(external_id=data.get("external_id")).first()
            if not lot:
                return -4        
            product = Product()  
            product.external_id = str(uuid.uuid4())
            product.name= data.get("name")
            product.date_product = data.get("date_product")
            product.date_expiry = data.get("date_expiry")
            product.status = data.get("status")
            product.lot_id= lot.id
            product.stock=data.get('stock')
            product.price = data.get("price")
            product.status_verify = True
            
            if image_file and self.allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image_file.save(image_path)
                product.image_path = filename
            
            db.session.add(product)
            db.session.commit() 
            return product
        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar el producto: {str(e)}")
            return -4
        
    def update_status(self):
        with freeze_time("2025-05-18"):
            today = datetime.now().date()
            products = Product.query.all()
            for product in products:
                days_until_expiry = (product.date_expiry - today).days
                if days_until_expiry < 0:
                    product.status = "caducado"
                    product.stock = 0
                elif days_until_expiry <= 5:
                    product.status = "a punto de caducar"
                else:
                    product.status = "bueno"
                db.session.commit()
    
    def unexpiredProduct(self):
        self.update_status()
        products = Product.query.join(Lot).filter(Product.status == "bueno").all()
        unexpired_products = [product.serialize for product in products]
        return unexpired_products
    
    def expired_product(self):
        self.update_status()
        products = Product.query.join(Lot).filter(Product.status == "caducado").all()
        expired_products = [product.serialize for product in products]
        return expired_products
    
    def expired_product_5days(self):
        self.update_status()
        products = Product.query.join(Lot).filter(Product.status == "a punto de caducar").all()
        expired_products = [product.serialize for product in products]
        return expired_products
    
    def search_external(self, external_id):
        return Product.query.filter_by(external_id=external_id).first() 
    
    def modify_product(self, external_id, data):
        producto = Product.query.filter_by(external_id=external_id).first()
        if producto:
            producto.name = data.get("name")
            producto.date_expiry = data.get("date_expiry")
            producto.status = data.get("status").get('name')
            producto.price = data.get("price")
            producto.stock = data.get("stock")
            db.session.merge(producto)
            db.session.commit()
            return producto.id
        else:
            return None
    
    @staticmethod
    def update_product_image(external_id, image_file):
        try:
            product = Product.query.filter_by(external_id=external_id).first()
            if not product:
                return {"msg": "ERROR", "code": 400, "data": {"error": "Producto no encontrado"}}, 400

            if not image_file:
                return {"msg": "ERROR", "code": 400, "data": {"error": "No se proporcionó ninguna imagen"}}, 400

            if image_file.filename == '':
                return {"msg": "ERROR", "code": 400, "data": {"error": "Nombre de archivo de imagen no válido"}}, 400

            if ProductController.allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image_file.save(image_path)
                product.image_path = filename
                db.session.commit()
                return {"msg": "OK", "code": 200, "data": product.serialize()}, 200

            return {"msg": "ERROR", "code": 400, "data": {"error": "Tipo de archivo no permitido"}}, 400

        except Exception as e:
            db.session.rollback()
            return {"msg": "ERROR", "code": 500, "data": {"error": str(e)}}, 500
        
    def lista_de_caducados(self):
        fecha_actual = datetime.now(timezone.utc).date()
        products_pornombre = {}
        productos = Product.query.all()
        for producto in productos:
            if producto.date_expiry < fecha_actual or producto.status == "POR_CADUCAR":
                if producto.name not in products_pornombre:
                    products_pornombre[producto.name] = []
                    
                    products_pornombre[producto.name].append({
                    'id': producto.id,
                    'name': producto.name,
                    'status': producto.status,
                    'stock': producto.stock,
                    'date_expiry': producto.date_expiry
                })
                producto.status = "CADUCADO"
                if producto.status_verify:
                    producto.stock -= 1
                    producto.status_verify = False
        db.session.commit()
        return products_pornombre
    
    def lista_de_porCaducar(self):
        fecha_caducar = datetime.now(timezone.utc).date() + timedelta(days=5)
        productos = Product.query.all()
        productos_por_caducar_por_nombre = {}

        for producto in productos:
            if producto.date_expiry <= fecha_caducar or producto.status == "POR_CADUCAR":
                if producto.name not in productos_por_caducar_por_nombre:
                    productos_por_caducar_por_nombre[producto.name] = []
                    
                productos_por_caducar_por_nombre[producto.name].append({
                    'id': producto.id,
                    'name': producto.name,
                    'status': producto.status.name,
                    'stock': producto.stock,
                    'date_expiry': producto.date_expiry
                })
                if producto.status_verify == True:
                    producto.status = "POR_CADUCAR"
                    producto.stock -= 1  
                    producto.status_verify = False
                else:
                    producto.status = "POR_CADUCAR"
        db.session.commit()
        return productos_por_caducar_por_nombre