from app import db
import uuid

class InvoiceDetail(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_invoice = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False, unique=True)
    id_prodcut = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, unique=True)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    