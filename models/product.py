from app import db
import uuid
from models.lot import Lot
from models.typestatus import TypeStatus
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    date_product = db.Column(db.Date)
    date_expiry = db.Column(db.Date)
    status = db.Column(db.Enum(TypeStatus), nullable=False)
    status_verify = db.Column(db.Boolean, default=True)
    price = db.Column(db.Double)
    stock = db.Column(db.Integer)
    image_path = db.Column(db.String(255))
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.id'), nullable=False)  # Corregido el nombre de la clave foránea
    lot = db.relationship('Lot', backref=db.backref('products', lazy=True))

    #producto tiene el id del usuario
    @property
    def serialize(self):
        return {
            'name': self.name,
            'date_product': self.date_product.strftime("%Y-%m-%d") if self.date_product else None,
            'date_expiry': self.date_expiry.strftime("%Y-%m-%d") if self.date_expiry else None,
            'status': self.status.serialize if self.status else None,
            # 'status': self.status.value,
            'stock': self.stock,
            'price': self.price,
            'image_path':self.image_path,
            'lot': self.lot.code if self.lot else None 
        }
        
    def get_lot_code(self):
        lot = Lot.query.get(self.lot_id)
        return lot.code if lot else None
            