from app import db
import uuid

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    account = db.relationship('Account', backref='person', lazy=True)
    lot =  db.relationship('Lot', backref='user_lot', lazy=True)
    
    @property
    def serialize(self):
        return {
            'name': self.name,
            'lastname': self.lastname,
            'external_id': self.external_id,
        } 