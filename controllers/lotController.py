from models.lot import Lot
from models.user import User
import uuid
from app import db
class LotController:
    def list_all_lot(self):
        try:
            lots = Lot.query.all()

            lot_data = []

            for lot in lots:
                lot_info = {
                    "external_id":lot.external_id,
                    'code': lot.code,
                    'quantity': lot.quantity,
                    'user_name': lot.user_lot.name,
                    'products': [] 
                }
                for product in lot.products:
                    product_info = {
                        'product_name': product.name,
                    }
                    lot_info['products'].append(product_info)

                lot_data.append(lot_info)

            return lot_data

        except Exception as e:
            print(f"Error fetching lots: {str(e)}")
            return []
    
    def save_lot(self, data):
        print("+++", data)
        # person = User.query.filter_by(external_id=data.get("user_id")).first()
        # if person :
        try:
                lot = Lot(
                    code = data["code"],
                    quantity = data["quantity"],
                    external_id = str(uuid.uuid4()),
                    user_id = int(data["user_id"]) 
                )
                db.session.add(lot)
                db.session.commit()
                return lot.id
        except Exception as e:
                db.session.rollback()
                print(f"Error al guardar el lote: {str(e)}")
                return -2
        # else:
        #     return -3