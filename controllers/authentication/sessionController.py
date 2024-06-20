from models.user import User
import uuid
import jwt
from models.account import Account
from datetime import datetime, timedelta, timezone
from app import db
from flask import current_app

class SessionController:
    def signUp(self, data):
        user = User()
        user.email = data["email"]
        user.password = data["password"]
        user.external_id = uuid.uuid4()
        
        db.session.add(user)
        db.session.commit()
        token = self.generate_token(user)
        return {"user": user, "token": token}
    
    def generate_token(self, user):
        payload = {
            "external_id": str(user.external_id),
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }

        token = jwt.encode(
            payload,
            key=current_app.config["SECRET_KEY"], 
            algorithm='HS512'
        )

        return token
    
    def login(self, data):
        accountA = Account.query.filter_by(email=data["email"]).first()
        if accountA:
            #decrypt password
            if accountA.password == data["password"]:
                token_payload = {
                    "external_id": accountA.external_id,
                    "expire": (datetime.now(timezone.utc) + timedelta(minutes=59)).isoformat()
                }
                print('-------------', token_payload)
                token = jwt.encode(
                    token_payload,
                    key=current_app.config["SECRET_KEY"],
                    algorithm="HS512"
                )
                account = Account()
                account.copy(accountA)    
                person = accountA.getPerson(accountA.user_id)
                user_info = {
                    "token": token,
                    "user": person.lastname + " " + person.name,
                    "expire": (datetime.now(timezone.utc) + timedelta(minutes=1)).isoformat()
                }
                return user_info
            else:
                -6
        else:
            return -6


