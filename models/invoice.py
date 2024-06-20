from app import db
import uuid

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    date = db.Column(db.Date)
    total = db.Column(db.Float)
    # id_detail = db.Column(db.Integer, db.ForeignKey('invoiceDetail.id', nullable=False, unique=True))
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    