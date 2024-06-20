from app import db
import uuid

class Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    @property
    def serialize(self):
        return {
            'code': self.code,
            'quantity': self.quantity,
            'external_id': self.external_id,
            'user_name': self.user_lot.name
        }